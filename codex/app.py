from .lib import CodexParams, SPHINX_CONFIG_TEMPLATE


def create(self, record: CodexParams) -> None:
    print(f"Executing 'create'")


def update(self, record: CodexParams) -> None:
    print("Executing 'update' command")


def delete(self, record: CodexParams) -> None:
    print("Executing 'delete' command")


def deploy(self, record: CodexParams) -> None:
    print("Executing 'deploy' command")


def pack(self, record: CodexParams) -> None:
    print("Executing 'pack' command")


def unpack(self, record: CodexParams) -> None:
    print("Executing 'unpack' command")


def build(self, record: CodexParams) -> None:
    print("Executing 'build' command")


