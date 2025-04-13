from argparse import _SubParsersAction, ArgumentParser
from typing import Callable, Any


type Codex = ArgumentParser
type Subcommand = ArgumentParser
type Subparser  = _SubParsersAction[ArgumentParser]
type Behaviour = Callable[..., Any]
