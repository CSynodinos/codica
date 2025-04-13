from typing import Callable, Any, Self
from argparse import Namespace


class CodexParams(Namespace):
    func: Callable[[Self], Any]

    def keys(self) -> list[str]:
        return [key for key in self.__dict__.keys() if not key.startswith("_")]

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

