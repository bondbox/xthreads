# coding:utf-8

from typing import Dict
from typing import Iterator
from typing import List
from typing import Union

from psutil import Process


class Processes():

    def __init__(self) -> None:
        self.__processes: Dict[int, Process] = {}

    def __iter__(self) -> Iterator[Process]:
        invalid: List[Process] = []

        for pid in sorted(self.__processes.keys()):
            if not (obj := self.__processes[pid]).is_running():
                invalid.append(obj)
                continue

            yield obj

        for obj in invalid:
            del self.__processes[obj.pid]  # pragma: no cover

    def __getitem__(self, pid: int):
        if pid not in self.__processes:
            obj: Process = Process(pid=pid)
            self.__processes.setdefault(pid, obj)
        return self.__processes[pid]

    def __len__(self) -> int:
        return len(self.__processes)

    def add(self, p: Union[Process, int]) -> bool:
        obj: Process = Process(pid=p) if isinstance(p, int) else p
        assert isinstance(obj, Process), f"{type(obj)} is not Process"

        if (pid := obj.pid) in self.__processes:
            if (proc := self.__processes[pid]).is_running():
                return proc == obj
            del self.__processes[pid]

        self.__processes.setdefault(pid, obj)
        return self.__processes[pid] is obj

    def select(self, name: str, exact: bool = True) -> None:
        def _name_filter(process_name: str) -> bool:
            return process_name == name if exact else name in process_name

        from psutil import process_iter  # pylint:disable=C0415
        for proc in process_iter(["name"]):
            if _name_filter(proc.name()):
                self.add(proc)

    @classmethod
    def search(cls, name: str, exact: bool = True) -> "Processes":
        instance: Processes = cls()
        instance.select(name, exact)
        return instance


if __name__ == "__main__":
    for _p in Processes.search("systemd"):
        print(f"{_p.name()} pid:{_p.pid}")
