#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import Any
import codex.lib as codex


def Codex_App() -> codex.Codex:
    """
    Create the main parser and subparsers for the CLI application
    """

    app = ArgumentParser(prog = "codex", description = "Codex CLI Application")
    subparsers: codex.Subparser = app.add_subparsers(title = "Commands", dest = "command", required = True)

    create_subcmd = codex.Create_Subcommand(subparsers, "create", help = "Create a new item")
    codex.Add_Argument(create_subcmd, "directory", nargs = "*", help = "Arguments to pass to the command")
    codex.Add_Argument(create_subcmd, "--outdir", "-o", help = "Output directory", default = "docs")
    
    
    update_subcmd = codex.Create_Subcommand(subparsers, "update", help = "Update an item")
    

    delete_subcmd = codex.Create_Subcommand(subparsers, "delete", help = "Delete an item")
    


    deploy_subcmd = codex.Create_Subcommand(subparsers, "deploy", help = "Deploy your project")
    codex.Add_Argument(deploy_subcmd, "directory", nargs = "*", help = "Arguments to pass to the command", default = ["docs",])
    codex.Add_Argument(deploy_subcmd, "--port", "-p", help = "Port to use", default = "8000")

    pack_subcmd = codex.Create_Subcommand(subparsers, "pack", help = "Pack resources")
    

    unpack_subcmd = codex.Create_Subcommand(subparsers, "unpack", help = "Unpack resources")
    

    build_subcmd = codex.Create_Subcommand(subparsers, "build", help = "Build your project")
    

    Behaviours_and_Subcommands: list[tuple[codex.Behaviour, codex.Subcommand]] = [
        (codex.create, create_subcmd),
        (codex.update, update_subcmd),
        (codex.delete, delete_subcmd),
        (codex.deploy, deploy_subcmd),
        (codex.pack, pack_subcmd),
        (codex.unpack, unpack_subcmd),
        (codex.build, build_subcmd)
        ]

    for behaviour, subcommand in Behaviours_and_Subcommands:
        codex.Set_Behaviour(behaviour, subcommand)

    return app


def main() -> None:
    app = Codex_App()
    params: dict[str, Any] = vars(app.parse_args())
    return codex.Run(
        codex.CodexParams(**params)
        )


if __name__ == '__main__':
    main()

