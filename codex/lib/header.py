from argparse import _SubParsersAction, ArgumentParser
from typing import Callable, Any
from enum import StrEnum


type Codex = ArgumentParser
type Subcommand = ArgumentParser
type Subparser  = _SubParsersAction[ArgumentParser]
type Behaviour = Callable[..., Any]


class Commands(StrEnum):
    """
    Enum for the commands
    """
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    DEPLOY = "deploy"
    PACK = "pack"
    UNPACK = "unpack"
    BUILD = "build"
