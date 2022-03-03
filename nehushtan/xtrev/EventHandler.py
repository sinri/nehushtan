from concurrent.futures import Executor, Future
from typing import Callable, Optional


class EventHandler:
    def __init__(self, callback: Callable[[any], None]):
        self.__real_callback = callback
        self.__when_success: Optional[Callable[[any], None]] = None
        self.__when_failure: Optional[Callable[[BaseException], None]] = None
        self.__next_event_handler: Optional["EventHandler"] = None
        self.__executor: Optional[Executor] = None

    def set_success_handler(self, callback: Callable[[any], None]):
        self.__when_success = callback
        return self

    def set_failure_handler(self, callback: Callable[[BaseException], None]):
        self.__when_failure = callback
        return self

    def __set_next_event_handler(self, next_event_handler: "EventHandler"):
        self.__next_event_handler = next_event_handler

    def execute(self, executor: Executor, param):
        self.__executor = executor
        f = self.__executor.submit(self.__real_callback, param)
        f.add_done_callback(self.__future_done_callback)
        return self

    def next(self, next_event_handler: "EventHandler"):
        ptr = self
        while ptr.__next_event_handler is not None:
            ptr = ptr.__next_event_handler
        ptr.__set_next_event_handler(next_event_handler)

    def __future_done_callback(self, future: Future):
        exception = future.exception()
        if exception is None:
            result = future.result()
            if self.__when_success is not None:
                self.__when_success(result)
            if self.__next_event_handler is not None:
                self.__next_event_handler.execute(self.__executor, result)
        else:
            if self.__when_failure is not None:
                self.__when_failure(exception)
