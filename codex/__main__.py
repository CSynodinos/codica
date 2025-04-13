#!/usr/bin/env python3
from codex.app import *
from codex.lib import CodexParams
import argparse


def create_parser() -> argparse.ArgumentParser:
    """
    
    """

    #* Create the main parser
    parser = argparse.ArgumentParser(prog = "codex", description = "Codex CLI Application")
    subparsers = parser.add_subparsers(title = "Commands", dest = "command", required = True)

    #* Create subcommand
    parser_create = subparsers.add_parser("create", help = "Create a new item")
    parser_create.set_defaults(func = create)

    #* Update subcommand
    parser_update = subparsers.add_parser("update", help = "Update an existing item")
    parser_update.set_defaults(func = update)

    #* Delete subcommand
    parser_delete = subparsers.add_parser("delete", help = "Delete an item")
    parser_delete.set_defaults(func = delete)

    #* Deploy subcommand
    parser_deploy = subparsers.add_parser("deploy", help = "Deploy your application")
    parser_deploy.set_defaults(func = deploy)

    #* Pack subcommand
    parser_pack = subparsers.add_parser("pack", help = "Pack resources")
    parser_pack.set_defaults(func = pack)

    #* Unpack subcommand
    parser_unpack = subparsers.add_parser("unpack", help = "Unpack resources")
    parser_unpack.set_defaults(func = unpack)

    #* Build subcommand
    parser_build = subparsers.add_parser("build", help = "Build your project")
    parser_build.set_defaults(func = build)

    return parser


def main() -> None:
    parser = create_parser()
    args = CodexParams(**vars(parser.parse_args()))
    return args.func(args)


if __name__ == '__main__':
    main()

