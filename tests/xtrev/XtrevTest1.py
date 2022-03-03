import time

from nehushtan.xtrev.EventLoop import EventLoop


def callback_a():
    print("callback_a")


def callback_b():
    print("callback_b")


if __name__ == '__main__':
    loop = EventLoop()
    loop.start()

    loop.register_event_listener("a", callback_a)
    loop.register_event_listener(EventLoop.event_key_of_loop_ended, callback_b)

    for i in range(3):
        loop.trigger_event("a")
        time.sleep(1)

    print("let loop stop, then join")
    loop.stop()

    loop.join_thread_for_loop()
    print("end")
