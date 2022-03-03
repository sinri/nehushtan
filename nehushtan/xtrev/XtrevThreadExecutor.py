from concurrent.futures import Executor
from concurrent.futures.thread import ThreadPoolExecutor


class XtreVThreadExecutor(Executor):
    def __init__(self):
        self.__executor = ThreadPoolExecutor()
        self.__executable = True

    def submit(self, fn, *args, **kwargs):
        print(f"XtreVThreadExecutor submit {self.__executable}")
        if self.__executable:
            return self.__executor.submit(fn, *args, **kwargs)
        else:
            return ThreadPoolExecutor(1).submit(self.__handler_for_failed_future)

    def shutdown(self, wait=True, *, cancel_futures=False):
        self.__executable = False
        print("XtreVThreadExecutor shutdown")
        self.__executor.shutdown(wait, cancel_futures=cancel_futures)

    def map(self, fn, *iterables, timeout=None, chunksize=1):
        self.__executable = False
        self.__executor.map(fn, *iterables, timeout=timeout, chunksize=chunksize)

    def __handler_for_failed_future(self, exception: BaseException):
        raise Exception(exception)
