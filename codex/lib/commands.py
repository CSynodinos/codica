from .templates import SPHINX_CONFIG_TEMPLATE
from .utils import inputmap


@inputmap
def create(record: str, set: str) -> None:
    """asdasdsdasd"""
    print(f"Executing 'create' {record} command, setting {set}")


@inputmap
def update() -> None:
    print("Executing 'update' command")


@inputmap
def delete() -> None:
    print("Executing 'delete' command")


@inputmap
def deploy() -> None:
    print("Executing 'deploy' command")


@inputmap
def pack() -> None:
    print("Executing 'pack' command")


@inputmap
def unpack() -> None:
    print("Executing 'unpack' command")


@inputmap
def build() -> None:
    print("Executing 'build' command")


