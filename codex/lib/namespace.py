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
        _applied_args: list[str] = []
        assert isinstance(codex_params, CodexParams), FatalError
        _applied_kwargs: dict[str, str | list[str]] = dict(**codex_params)
        _applied_kwargs.pop("command", None)
        _applied_kwargs.pop("func", None)
        assert 'command' not in _applied_kwargs, FatalError
        assert 'func' not in _applied_kwargs, FatalError
        is_list = lambda _: isinstance(_, list)
        match _applied_kwargs:
            case args_case if 'args' in args_case:
                match _applied_kwargs.pop('args', None):
                    case None:                        pass
                    case str():                       pass
                    case _match if is_list(_match):   _applied_args = _match
                    case _:                           raise AssertionError(FatalError)
        return behaviour(*tuple(_applied_args), **_applied_kwargs)
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
