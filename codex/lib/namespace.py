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
        applied_args: list[str] = []
        assert isinstance(codex_params, CodexParams), FatalError
        _extracted_kwargs: dict[str, str | list[str]] = dict(**codex_params)
        _extracted_kwargs.pop("command", None)
        _extracted_kwargs.pop("func", None)
        assert 'command' not in _extracted_kwargs, FatalError
        assert 'func' not in _extracted_kwargs, FatalError
        applied_kwargs: dict[str, str] = {}
        for k, v in _extracted_kwargs.items():
            match v:
                case list():
                    applied_args.extend(v)
                case _:
                    applied_kwargs[k] = v
        return behaviour(*tuple(applied_args), **applied_kwargs)
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
