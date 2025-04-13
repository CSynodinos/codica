#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import Any
import codex.lib as codex


def Codex_App() -> codex.Codex:
    """
    Create the main parser and subparsers for the CLI application
    """

    #* Create the main parser & subparsers
    app = ArgumentParser(prog = "codex", description = "Codex CLI Application")
    subparsers: codex.Subparser = app.add_subparsers(title = "Commands", dest = "command", required = True)

    #* Create 'create' subcommand and add flags
    create_subcmd = codex.Create_Subcommand(subparsers, "create", help = "Create a new item")
    codex.Add_Argument(create_subcmd, "--record", required = True, help = "Record identifier")
    codex.Add_Argument(create_subcmd, "--set", required = True, help = "Name of the item")

    #* Update subcommand and add flags
    update_subcmd = codex.Create_Subcommand(subparsers, "update", help = "Update an item")
    

    #* Delete subcommand and add flags
    delete_subcmd = codex.Create_Subcommand(subparsers, "delete", help = "Delete an item")
    


    #* Deploy subcommand and add flags
    deploy_subcmd = codex.Create_Subcommand(subparsers, "deploy", help = "Deploy your project")
    

    #* Pack subcommand and add flags
    pack_subcmd = codex.Create_Subcommand(subparsers, "pack", help = "Pack resources")
    

    #* Unpack subcommand and add flags
    unpack_subcmd = codex.Create_Subcommand(subparsers, "unpack", help = "Unpack resources")
    

    #* Build subcommand and add flags
    build_subcmd = codex.Create_Subcommand(subparsers, "build", help = "Build your project")
    

    #* Bootstrap the subcommands with behaviours
    Behaviours_and_Subcommands: list[tuple[codex.Behaviour, codex.Subcommand]] = [
        (codex.create, create_subcmd),
        (codex.update, update_subcmd),
        (codex.delete, delete_subcmd),
        (codex.deploy, deploy_subcmd),
        (codex.pack, pack_subcmd),
        (codex.unpack, unpack_subcmd),
        (codex.build, build_subcmd)
        ]

    #* Set the behaviours for each subcommand
    for behaviour, subcommand in Behaviours_and_Subcommands:
        codex.Set_Behaviour(behaviour, subcommand)

    return app


def main() -> None:
    app = Codex_App()
    cli_params: dict[str, Any] = vars(app.parse_args())
    return codex.Run(codex.CodexParams(**cli_params))


if __name__ == '__main__':
    main()

