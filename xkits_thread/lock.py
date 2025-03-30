# coding:utf-8

from threading import Lock
from typing import Dict
from typing import Generic
from typing import Iterator
from typing import TypeVar

LKIT = TypeVar("LKIT")
LKNT = TypeVar("LKNT")


class NamedLock(Generic[LKNT]):

    class LockItem(Generic[LKIT]):
        def __init__(self, name: LKIT):
            self.__lock: Lock = Lock()
            self.__name: LKIT = name

        @property
        def name(self) -> LKIT:
            return self.__name

        @property
        def lock(self) -> Lock:
            return self.__lock

    def __init__(self):
        self.__locks: Dict[LKNT, NamedLock.LockItem[LKNT]] = {}
        self.__inter: Lock = Lock()  # internal lock

    def __len__(self) -> int:
        return len(self.__locks)

    def __iter__(self) -> Iterator[LockItem[LKNT]]:
        return iter(self.__locks.values())

    def __contains__(self, name: LKNT) -> bool:
        return name in self.__locks

    def __getitem__(self, name: LKNT) -> Lock:
        return self.lookup(name).lock

    def lookup(self, name: LKNT) -> LockItem[LKNT]:
        try:
            return self.__locks[name]
        except KeyError:
            with self.__inter:
                if name not in self.__locks:
                    lock = self.LockItem(name)
                    self.__locks.setdefault(name, lock)
                    assert self.__locks[name] is lock
                    return lock

                lock = self.__locks[name]  # pragma: no cover
                assert lock.name == name  # pragma: no cover
                return lock  # pragma: no cover
