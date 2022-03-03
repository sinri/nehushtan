import time

from nehushtan.xtrev.EventHandler import EventHandler
from nehushtan.xtrev.EventLoop import EventLoop, event_key_of_loop_ended


def callback_a(x):
    print("callback_a with ", x)


def callback_b(x):
    print("callback_b with ", x)


def callback_c(x):
    print("callback_c with ", x)


if __name__ == '__main__':
    loop = EventLoop()
    loop.start()

    loop.register_event_listener("a", EventHandler(callback_a))
    loop.register_event_listener(event_key_of_loop_ended, EventHandler(callback_b))

    for i in range(3):
        loop.trigger_event("a")
        time.sleep(1)

    loop.trigger_once_event_handler(EventHandler(callback_c), "c")

    print("let loop stop, then join")
    loop.stop()

    loop.join_thread_for_loop()
    print("end")
