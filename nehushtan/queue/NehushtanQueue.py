import os
import time
from multiprocessing import Process

from nehushtan.queue.NehushtanQueueDelegate import NehushtanQueueDelegate
from nehushtan.queue.NehushtanQueueTask import NehushtanQueueTask
from nehushtan.queue.situation.NoNextTaskSituation import NoNextTaskSituation


class NehushtanQueue:
    def __init__(self, delegate: NehushtanQueueDelegate):
        self.delegate: NehushtanQueueDelegate = delegate
        self.current_workers = {}
        self._is_running_exclusive_task = False

    def get_logger(self):
        return self.delegate.logger

    def get_pool_capacity(self) -> int:
        """
        How many processes could run in the same time.
        Decided by the delegate
        """
        if self._is_running_exclusive_task is True:
            return 1

        return self.delegate.read_config_of_delegate((NehushtanQueueDelegate.CONFIG_KEY_POOL_CAPACITY,), 1)

    def _scan_workers(self):
        """
        Scan registered workers, and remove dead ones from dictionary.
        Finally return the total running processes count.
        """
        if len(self.current_workers.items()) > 0:
            delete_keys = []
            for task_id, task_process in self.current_workers.items():
                if not task_process.is_alive():
                    task_process_pid = task_process.pid
                    task_process_exit_code = task_process.exitcode
                    self.get_logger().warning(f'Worker Process for task [{task_id}] Dead', {'pid': task_process_pid})
                    self.delegate.when_worker_process_confirmed_dead(
                        task_id,
                        {'pid': task_process_pid, 'exitcode': task_process_exit_code}
                    )
                    delete_keys.append(task_id)
            for delete_key in delete_keys:
                del self.current_workers[delete_key]
                self.get_logger().debug('remove removable finished tasks', {'task_id': delete_key})

        return len(self.current_workers.items())

    def _terminate_worker_process_of_task(self, task_reference):
        p = self.current_workers.get(task_reference)
        if p:

            # 终止进程
            # https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Process.terminate
            #
            #   在Unix上
            #       这是使用 SIGTERM 信号完成的；
            #   在Windows上
            #       使用 TerminateProcess() 。请注意，不会执行退出处理程序和finally子句等。
            #       这个函数可以用来终止或者说杀死一个进程，它不会留给进程及其所有线程清理的时间，
            #       系统会马上终止(杀死)这个进程的所有线程，致使进程终止。
            #
            # 请注意，进程的后代进程将不会被终止 —— 它们将简单地变成孤立的。
            p.terminate()

            self.get_logger().info(
                'NehushtanQueue._terminate_worker_process_of_task executed',
                {'task': task_reference, 'pid': p.pid, 'exitcode': p.exitcode, 'is_alive': p.is_alive()}
            )
            self.delegate.when_killed_worker_process(task_reference, worker_pid=p.pid)
            self.register_news(f'Sent signal TERMINATE(15) to worker for task {task_reference}, target pid {p.pid}')
        else:
            self.get_logger().warning(
                'NehushtanQueue._terminate_worker_process_of_task target task not found amongst current workers',
                {'task': task_reference}
            )
            self.delegate.when_killed_worker_process(task_reference, not_found=True)

    def _loop_maintain(self, wait_till_processes_become_less_than: int = 0):
        self._scan_workers()

        self.delegate.handle_command_queue()
        self.register_news('Handled Command Queue')

        kill_list = self.delegate.should_kill_any_worker_processes()
        if len(kill_list) > 0:
            for kill_task_id in kill_list:
                self._terminate_worker_process_of_task(kill_task_id)

        total_alive_current_workers = self._scan_workers()

        if wait_till_processes_become_less_than > 0:
            # need to do some wait
            if total_alive_current_workers >= wait_till_processes_become_less_than:
                time.sleep(2)
                return self._loop_maintain(wait_till_processes_become_less_than)
        else:
            return total_alive_current_workers

    def register_news(self, news):
        """
        Since 0.2.8
        """
        worker_count = len(self.current_workers.items())
        busy_rate = 1.0 * worker_count / self.get_pool_capacity()
        self.delegate.register_queue_news(news, worker_count, busy_rate)

    def loop(self):
        self.delegate.when_loop_starts()
        self.register_news('Loop Started')

        while True:
            try:
                # 1. check current workers status
                total_current_workers = len(self.current_workers.items())
                self.get_logger().info('Current workers totally count', {'total': total_current_workers})

                # 2. handle command queue and kill list
                self._loop_maintain()

                # 3. check elihu command
                self.delegate.read_latest_command()
                if self.delegate.should_terminate():
                    if self.delegate.should_wait_for_all_workers_before_terminating():
                        self.register_news('Waiting for all running tasks finishing, then terminate loop')
                        self._loop_maintain(1)
                    break

                # 4. check queue if new task there
                if not self.delegate.is_runnable():
                    self.register_news('Loop is ordered to sleep for a while')
                    self.delegate.when_loop_should_not_run()
                    continue

                total_current_workers = len(self.current_workers.items())
                if total_current_workers >= self.get_pool_capacity():
                    self.register_news('All workers are busy, wait till anyone become available')
                    self._loop_maintain(self.get_pool_capacity())

                    if self._is_running_exclusive_task and len(self.current_workers.items()) <= 0:
                        self._is_running_exclusive_task = False
                        self.register_news('Exit exclusive mode as no task running now')

                try:
                    task = self.delegate.check_next_task()
                    task_id = task.get_task_reference()

                    if task.is_exclusive():
                        # now daemon should wait for the other tasks to be over
                        self.register_news(f'Task {task_id} is exclusive, waiting for all running workers finish')
                        self._loop_maintain(1)
                        self.register_news(f'Enter exclusive mode for task {task_id} as all other workers finished')
                        self._is_running_exclusive_task = True

                    if not task.before_execute():
                        self.register_news(f'Task {task_id} is not executable')
                        self.delegate.when_task_not_executable(task)

                        if self._is_running_exclusive_task:
                            self._is_running_exclusive_task = False
                            self.register_news(f'Exit exclusive mode as task {task_id} is not executable')

                        continue

                    p = Process(target=NehushtanQueue.embedded_task_execute, args=(task, self.delegate))
                    p.start()
                    self.current_workers[task.get_task_reference()] = p

                    self.register_news(f'Task [{task.get_task_reference()}] -> Process {p.name} PID is [{p.pid}]')
                    self.delegate.when_worker_process_created(
                        task.get_task_reference(),
                        f'Task [{task.get_task_reference()}] -> Process {p.name} PID is [{p.pid}]'
                    )

                except NoNextTaskSituation:
                    self.register_news('There is no task in queue able to deal now')
                    self.delegate.when_no_task_to_do()
                    continue

            except Exception as loop_round_error:
                self.register_news(f'Loop meets error: {loop_round_error}')
                self.delegate.when_loop_reports_error(loop_round_error.__str__())

        self.register_news('Loop is about to terminate')
        self.delegate.when_loop_terminates()
        self.register_news('Loop terminated')

    @staticmethod
    def embedded_task_execute(embedded_task: NehushtanQueueTask, delegate: NehushtanQueueDelegate):
        """
        This works in WORKER
        """
        delegate.when_to_execute_task(embedded_task, os.getpid())
        try:
            embedded_task.execute()
        except Exception as e:
            delegate.when_task_raised_exception(embedded_task, e)
        delegate.when_task_executed(embedded_task, os.getpid())
