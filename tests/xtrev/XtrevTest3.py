import time

from nehushtan.xtrev.EventHandler import EventHandler
from nehushtan.xtrev.NehushtanXtreV import NehushtanXtreV

xtrev = NehushtanXtreV()

counter = 0


def timer_callback(timer_id: str):
    print(f'timer_callback triggered by {timer_id} on {time.time()}')

    global counter
    counter += 1

    if counter > 10:
        global xtrev
        xtrev.cancel_timer(timer_id)
        print(f"to close! counter={counter}")
        xtrev.close()


if __name__ == '__main__':
    timer_callback("INIT")
    xtrev.set_timer(3.0, EventHandler(timer_callback), False)
    xtrev.set_timer(2.0, EventHandler(timer_callback), True)

    time.sleep(4)
    timer_callback("MAIN END")

    xtrev.daemon()
