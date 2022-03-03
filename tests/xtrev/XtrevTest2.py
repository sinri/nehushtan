from concurrent.futures.thread import ThreadPoolExecutor

from nehushtan.xtrev.EventHandler import EventHandler


def handler_for_twice(x):
    return x * 2 / 0


def handler_for_print(x):
    print(x)


if __name__ == '__main__':
    pool_executor = ThreadPoolExecutor()
    event_handler = EventHandler(handler_for_twice)
    event_handler.set_success_handler(handler_for_print)
    event_handler.set_failure_handler(handler_for_print)
    event_handler.__set_next_event_handler(EventHandler(handler_for_print))
    event_handler.execute(pool_executor, 1)
