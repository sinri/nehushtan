import time
from typing import Dict, Optional

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.xtrev.EventHandler import EventHandler
from nehushtan.xtrev.EventLoop import EventLoop, event_key_of_timer


class NehushtanXtreVTimerMeta:
    def __init__(self, expected_time: float, event_handler: EventHandler, periodicity: Optional[float] = None):
        self.expected_time: float = expected_time
        self.event_handler: EventHandler = event_handler
        self.periodicity: Optional[float] = periodicity


class NehushtanXtreV:
    def __init__(self):
        self.__event_loop = EventLoop()
        self.__event_loop.start()

        # timer related
        self.__timers: Dict[str, NehushtanXtreVTimerMeta] = {}
        self.__event_loop.register_event_listener(event_key_of_timer,
                                                  EventHandler(self.__timer_event_handler))

    def close(self):
        self.__timers.clear()
        self.__event_loop.stop()

    def __timer_event_handler(self, current_time):
        to_delete = []
        to_execute = {}
        for timer_id, timer_meta in self.__timers.items():
            expected_time = timer_meta.expected_time
            if expected_time is None:
                to_delete.append(timer_id)
                continue
            if expected_time <= current_time:
                handler = timer_meta.event_handler
                to_execute[timer_id] = handler
                if timer_meta.periodicity is None:
                    to_delete.append(timer_id)
                    break
                else:
                    timer_meta.expected_time = time.time() + timer_meta.periodicity
        for x in to_delete:
            del self.__timers[x]
        for timer_id, handler in to_execute.items():
            self.__event_loop.trigger_once_event_handler(handler, timer_id)

    def set_timer(self, periodicity: float, event_handler: EventHandler, periodically: bool):
        timer_id = CommonHelper.generate_random_uuid_hex()
        if periodically:
            self.__timers[timer_id] = NehushtanXtreVTimerMeta(time.time() + periodicity, event_handler, periodicity)
        else:
            self.__timers[timer_id] = NehushtanXtreVTimerMeta(time.time() + periodicity, event_handler)

    def cancel_timer(self, timer_id: str):
        if self.__timers.get(timer_id) is not None:
            del self.__timers[timer_id]
