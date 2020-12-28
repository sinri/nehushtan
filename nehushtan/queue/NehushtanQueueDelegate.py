import time
from abc import abstractmethod

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.logger.NehushtanLogger import NehushtanLogger
from nehushtan.queue.NehushtanQueueTask import NehushtanQueueTask


class NehushtanQueueDelegate:
    QUEUE_RUNTIME_COMMAND_PAUSE = "PAUSE"
    QUEUE_RUNTIME_COMMAND_CONTINUE = "CONTINUE"
    QUEUE_RUNTIME_COMMAND_STOP = "STOP"
    QUEUE_RUNTIME_COMMAND_FORCE_STOP = "FORCE-STOP"
    QUEUE_RUNTIME_COMMAND_RESTART = "RESTART"
    QUEUE_RUNTIME_COMMAND_FORCE_RESTART = "FORCE-RESTART"

    CONFIG_KEY_POOL_CAPACITY = 'POOL_CAPACITY'

    def __init__(self, config_dictionary: dict = None, logger: NehushtanLogger = None):
        if config_dictionary is None:
            config_dictionary = {}
        self.config_dictionary = config_dictionary

        if logger is None:
            logger = NehushtanLogger(
                f"{self.__class__.__name__}-DefaultLogger",
                [NehushtanLogger.make_stdout_handler()],
                with_process_info=True,
                with_thread_info=True
            )
        self.logger = logger

    def read_config_of_delegate(self, keychain: tuple, default):
        return CommonHelper.read_dictionary(self.config_dictionary, keychain, default)

    def get_configured_pool_capacity(self) -> int:
        return self.read_config_of_delegate((NehushtanQueueDelegate.CONFIG_KEY_POOL_CAPACITY,), 1)

    def when_loop_starts(self):
        """
        To be executed before loop cycle starts
        """
        pass

    @abstractmethod
    def when_loop_reports_error(self, error_message: str):
        pass

    @abstractmethod
    def is_runnable(self):
        """
        If not runnable, the daemon loop would sleep.
        """
        pass

    @abstractmethod
    def should_terminate(self):
        """
        Tell daemon loop to exit.
        """
        pass

    @abstractmethod
    def when_loop_terminates(self):
        """
        When the loop gets ready to terminate by shouldTerminate instructed, execute this
        """
        pass

    @abstractmethod
    def when_loop_should_not_run(self):
        """
        Sleep for a certain while.
        """
        pass

    @abstractmethod
    def check_next_task(self) -> NehushtanQueueTask:
        pass

    @abstractmethod
    def when_no_task_to_do(self):
        """
        When the loop cannot check for a task to do next, execute this
        """
        pass

    @abstractmethod
    def when_task_not_executable(self, task: NehushtanQueueTask):
        """
        this is done before fork in pooled style
        """
        pass

    @abstractmethod
    def when_to_execute_task(self, task: NehushtanQueueTask):
        """
        Note: Any exceptions should be caught inside.
        """
        pass

    @abstractmethod
    def when_task_executed(self, task: NehushtanQueueTask):
        """
        Note: Any exceptions should be caught inside.
        """
        pass

    @abstractmethod
    def when_task_raised_exception(self, task: NehushtanQueueTask, exception: Exception):
        pass

    def when_pool_is_full(self):
        self.logger.warning('Pool is full, sleep for a while', {'size': self.get_configured_pool_capacity()})
        # self.beat('whenPoolIsFull', 'Pool Full Wait')
        time.sleep(30)

    def when_worker_process_created(self, task_reference, note: str = ''):
        pass

    def when_worker_process_confirmed_dead(self, task_reference, detail=None):
        pass

    def should_wait_when_pool_is_full(self):
        return True

    def should_wait_for_all_workers_before_terminating(self):
        return True
