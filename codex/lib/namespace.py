from .templates import FatalError
from typing import Callable, Any, Self
from argparse import Namespace
from functools import wraps


def _inputmap[R, **Params](behaviour: Callable[Params, R]) -> Callable[Params, R]:
    """
    Decorator to match the type of the function
    """
    @wraps(behaviour)
    def wrapper(*args: Params.args, **_: Params.kwargs) -> R:
        codex_params: CodexParams = args[0]
        _args: list[str] = []
        assert isinstance(codex_params, CodexParams), FatalError
        _kwargs: dict[str, str | list[str]] = dict(**codex_params)
        _kwargs.pop("command", None)
        _kwargs.pop("func", None)
        assert 'command' not in _kwargs, FatalError
        assert 'func' not in _kwargs, FatalError
        check = lambda _: type(_) == list
        match _kwargs:
            case args_case if 'args' in args_case:
                match _kwargs.pop('args', None):
                    case None:                      pass
                    case str():                     pass
                    case _match if check(_match):   _args = _match      #? Modify the args to the match
                    case _:                         raise AssertionError(FatalError)
            case _:
                pass
        return behaviour(*tuple(_args), **_kwargs)
    return wrapper


class CodexParams(Namespace):
    func: Callable[[Self], Any]

    def keys(self) -> list[str]:
        return [key for key in self.__dict__.keys() if not key.startswith("_")]

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __getattribute__(self, name: str) -> Any:
        match name:
            case "func":
                return _inputmap(super().__getattribute__(name))
            case _:
                return super().__getattribute__(name)
