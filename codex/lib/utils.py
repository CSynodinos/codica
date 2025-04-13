from .header import Subparser, Subcommand, Behaviour
from .namespace import CodexParams
from argparse import Action
from typing import Callable, Any
from functools import wraps


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
        assert isinstance(codex_params, CodexParams), RuntimeError("Invalid parameters, broken CLI")
        applied_kwargs: dict[str, str] = dict(**codex_params)
        applied_kwargs.pop("command", None)
        applied_kwargs.pop("func", None)
        return behaviour(**applied_kwargs)
    return wrapper
