from concurrent.futures.thread import ThreadPoolExecutor
from queue import SimpleQueue, Empty
from threading import Thread
from typing import Dict, Callable, Optional

from nehushtan.xtrev.EventHandler import EventHandler


class EventLoop:
    event_key_of_loop_ended: str = "loop_ended"

    def __init__(self):
        self.flag_to_stop = False
        self.__event_mapping: Dict[str, Callable] = {}
        self.__event_queue = SimpleQueue()
        self.__thread_for_loop: Optional[Thread] = None
        self.__pool_executor = ThreadPoolExecutor()

    def start(self, thread_name: str = "thread_for_loop"):
        self.__thread_for_loop = Thread(target=self.__loop_while, name=thread_name, daemon=True)
        self.__thread_for_loop.start()

    def stop(self):
        self.flag_to_stop = True

    def join_thread_for_loop(self):
        self.__thread_for_loop.join()

    def register_event_listener(self, event_key: str, callback: Callable):
        self.__event_mapping[event_key] = callback

    def unregister_event_listener(self, event_key: str):
        del self.__event_mapping[event_key]

    def trigger_event(self, event_key: str):
        self.__event_queue.put(event_key)

    def trigger_once_event_handler(self, event_handler: EventHandler):
        """
        TODO
        """
        pass

    def __should_stop_loop(self) -> bool:
        return self.flag_to_stop

    def __loop_while(self):
        self.flag_to_stop = False
        while not self.__should_stop_loop():
            self.__one_loop_cycle()

        # loop end callback
        callback = self.__event_mapping.get(EventLoop.event_key_of_loop_ended)
        if callback is not None:
            callback()

    def __one_loop_cycle(self):
        try:
            event_code_triggered = self.__event_queue.get(timeout=0.5)
        except Empty:
            return
        callback = self.__event_mapping.get(event_code_triggered)
        if callback is not None:
            future = self.__pool_executor.submit(callback)
