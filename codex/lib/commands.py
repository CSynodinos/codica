from .templates import SPHINX_CONFIG_TEMPLATE


def create(*x, record: str, set: str) -> None:
    """asdasdsdasd"""
    print(f"Executing 'create' {record} command, setting {set} to {x}")


def update() -> None:
    print("Executing 'update' command")


def delete() -> None:
    print("Executing 'delete' command")


def deploy() -> None:
    print("Executing 'deploy' command")


def pack() -> None:
    print("Executing 'pack' command")


def unpack() -> None:
    print("Executing 'unpack' command")


def build() -> None:
    print("Executing 'build' command")


