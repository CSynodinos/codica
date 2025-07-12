#!/usr/bin/env python3
from argparse import ArgumentParser
import codex.lib as codex


def Create_Codex_Arg_Parser() -> codex.CodexParser:
    """
    Create the main parser and subparsers for the CLI application
    """

    app = ArgumentParser(prog = "codex", description = "Codex CLI Application")
    subparsers: codex.Subparser = app.add_subparsers(title = "Commands", dest = "command", required = True)

    create_subcmd = codex.Create_Subcommand(subparsers, codex.Commands.CREATE, help = "Create a new codex project")
    codex.Add_Argument(create_subcmd, "directory", nargs = "*", help = "Directory to create docs for")
    codex.Add_Argument(create_subcmd, "--outdir", "-o", help = "Output directory, default docs", default = "docs")

    update_subcmd = codex.Create_Subcommand(subparsers, codex.Commands.UPDATE, help = "Update an item")
    codex.Add_Argument(update_subcmd, "directory", nargs = "*", help = "Directory to update", default = ("docs",))

    delete_subcmd = codex.Create_Subcommand(subparsers, codex.Commands.DELETE, help = "Delete an item")
    codex.Add_Argument(delete_subcmd, "directory", nargs = "*", help = "Directory to delete", default = ("docs",))

    deploy_subcmd = codex.Create_Subcommand(subparsers, codex.Commands.DEPLOY, help = "Deploy your project")
    codex.Add_Argument(deploy_subcmd, "directory", nargs = "*", help = "Arguments to pass to the command", default = ("docs",))
    codex.Add_Argument(deploy_subcmd, "--port", "-p", help = "Port to use", default = "8000")

    pack_subcmd = codex.Create_Subcommand(subparsers, codex.Commands.PACK, help = "Pack resources")
    

    unpack_subcmd = codex.Create_Subcommand(subparsers, codex.Commands.UNPACK, help = "Unpack resources")
    

    build_subcmd = codex.Create_Subcommand(subparsers, codex.Commands.BUILD, help = "Build your project")
    

    #* Associate behaviours with subcommands
    Behaviours_and_Subcommands: list[tuple[codex.Behaviour, codex.Subcommand]] = [
        (codex.create, create_subcmd),
        (codex.update, update_subcmd),
        (codex.delete, delete_subcmd),
        (codex.deploy, deploy_subcmd),
        (codex.pack, pack_subcmd),
        (codex.unpack, unpack_subcmd),
        (codex.build, build_subcmd),
        ]
    for behaviour, subcommand in Behaviours_and_Subcommands:
        codex.Set_Behaviour(behaviour, subcommand)

    return app


def main() -> None:
    APP = Create_Codex_Arg_Parser()
    INPUTS = vars(APP.parse_args())
    codex.Run(codex.CodexCore(**INPUTS))
    return


if __name__ == '__main__':
    main()

