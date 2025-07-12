from .header import Subparser, Subcommand, Behaviour
from .namespace import CodexCore
from argparse import Action
from typing import Any


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


def Run(params_map: CodexCore) -> Any:
    """
    Run the function with the given parameters.
    """
    func_selected_by_user = params_map.func
    return func_selected_by_user(params_map)

