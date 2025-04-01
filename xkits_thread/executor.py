# coding:utf-8

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as ThreadTimeout
from threading import Thread
from threading import current_thread  # noqa:H306
from typing import Callable
from typing import Optional
from typing import Set
from typing import Tuple

from xkits_lib.meter import TimeUnit


class Executor():  # pylint: disable=too-few-public-methods
    def __init__(self, fn: Callable, *args, **kwargs) -> None:
        self.__fn = fn
        self.__args = args
        self.__kwargs = kwargs

    def countdown(self, seconds: TimeUnit):
        with ThreadPoolExecutor() as executor:
            try:
                future = executor.submit(self.__fn, *self.__args, **self.__kwargs)  # noqa:E501
                return future.result(seconds)
            except ThreadTimeout as exc:
                message: str = f"Run timeout of {seconds} seconds"
                raise TimeoutError(message) from exc


def hourglass(seconds: TimeUnit):
    def decorator(fn):
        def inner(*args, **kwargs):
            return Executor(fn, *args, **kwargs).countdown(seconds)
        return inner
    return decorator


class ThreadPool(ThreadPoolExecutor):
    """Thread Pool"""

    def __init__(self, max_workers: Optional[int] = None,
                 thread_name_prefix: str = "work_thread",
                 initializer: Optional[Callable] = None,
                 initargs: Tuple = ()):
        """Initializes an instance based on ThreadPoolExecutor."""
        if isinstance(max_workers, int):
            max_workers = max(max_workers, 2)
        super().__init__(max_workers, thread_name_prefix, initializer, initargs)  # noqa:E501

    @property
    def alive_threads(self) -> Set[Thread]:
        """alive threads"""
        return {thread for thread in self._threads if thread.is_alive()}

    @property
    def other_threads(self) -> Set[Thread]:
        """other threads"""
        current: Thread = current_thread()
        return {thread for thread in self._threads if thread is not current}

    @property
    def other_alive_threads(self) -> Set[Thread]:
        """other alive threads"""
        return {thread for thread in self.other_threads if thread.is_alive()}
