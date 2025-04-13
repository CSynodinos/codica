from .header import Subparser, Subcommand, Behaviour
from .namespace import CodexParams
from argparse import Action
from typing import Callable, Any
from functools import wraps


FatalError = "Fatal Error -> Invalid parameters, broken CLI"


def Create_Subcommand(subparser: Subparser, name: str, /, **kwargs: Any) -> Subcommand:
    """
    Create a subcommand parser.
    """
    return subparser.add_parser(name, **kwargs) 


def Add_Argument[**Params](subcommand: Subcommand, *args: Params.args, **kwargs: Params.kwargs) -> Action:
    """
    Create an argument parser with a default value.
    """
    return subcommand.add_argument(*args, **kwargs)


def Set_Behaviour(behaviour: Behaviour, to_subcommand: Subcommand) -> None:
    """
    Add a behaviour to the parser.
    """
    return to_subcommand.set_defaults(func = behaviour)


def Run(params_table: CodexParams) -> None:
    """
    Run the function with the given parameters.
    """
    return params_table.func(params_table)


def inputmap[R, **Params](behaviour: Callable[Params, R]) -> Callable[Params, R]:
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
