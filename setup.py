from setuptools import setup, find_packages


def get_requirements(filename="requirements.txt"):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name = "codex",
    version = "0.1.0",
    description = "Codex CLI Application",
    packages = find_packages(exclude = ["env", "env.*"]),
    python_requires = ">=3.12",
    install_requires = get_requirements(),
    entry_points = {
        "console_scripts": [
            "codex=codex.__main__:main",
            ],
        },
    )
