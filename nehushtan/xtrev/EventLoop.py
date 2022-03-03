import time
from queue import SimpleQueue, Empty
from threading import Thread
from typing import Dict, Optional

from nehushtan.xtrev.EventHandler import EventHandler
from nehushtan.xtrev.XtrevThreadExecutor import XtreVThreadExecutor

event_key_of_timer: str = "event_timer"
event_key_of_loop_ended: str = "event_loop_ended"


class EventLoop:
    def __init__(self):
        self.flag_to_stop = False
        self.__event_mapping: Dict[str, EventHandler] = {}
        self.__event_queue = SimpleQueue()
        self.__thread_for_loop: Optional[Thread] = None
        self.__pool_executor = XtreVThreadExecutor()  # ThreadPoolExecutor()

        self.__timer_pointer_as_second = time.time()

    def start(self, thread_name: str = "thread_for_loop"):
        self.__thread_for_loop = Thread(target=self.__loop_while, name=thread_name, daemon=False)
        self.__thread_for_loop.start()

    def stop(self):
        self.flag_to_stop = True

    def join_thread_for_loop(self):
        self.__thread_for_loop.join()

    def register_event_listener(self, event_key: str, event_handler: EventHandler):
        self.__event_mapping[event_key] = event_handler

    def unregister_event_listener(self, event_key: str):
        del self.__event_mapping[event_key]

    def unregister_all_event_listeners(self):
        self.__event_mapping.clear()

    def trigger_event(self, event_key: str):
        self.__event_queue.put(event_key)

    def trigger_once_event_handler(self, event_handler: EventHandler, param=None):
        event_handler.execute(self.__pool_executor, param)

    def __should_stop_loop(self) -> bool:
        return self.flag_to_stop

    def __loop_while(self):
        self.flag_to_stop = False
        while not self.__should_stop_loop():
            self.__one_loop_cycle()

        # loop end callback
        event_handler_for_ending = self.__event_mapping.get(event_key_of_loop_ended)
        if event_handler_for_ending is not None:
            event_handler_for_ending.execute(self.__pool_executor, None)

    def __one_loop_cycle(self):
        try:
            event_code_triggered = self.__event_queue.get(timeout=0.01)
            self.__execute_triggered_event_handler(event_code_triggered)
        except Empty:
            pass

        delta = time.time() - self.__timer_pointer_as_second
        if delta >= 1.0:
            self.__timer_pointer_as_second = time.time()
            self.__execute_triggered_event_handler(event_key_of_timer, self.__timer_pointer_as_second)

    def __execute_triggered_event_handler(self, event_code_triggered: str, param=None):
        event_handler = self.__event_mapping.get(event_code_triggered)
        if event_handler is not None:
            event_handler.execute(self.__pool_executor, param)
