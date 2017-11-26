"""Command line interface define"""
import argparse

from . import core


def build_parser():
    parser = argparse.ArgumentParser(
        description="CLI tool to interact with list of repositories"
    )
    subparsers = parser.add_subparsers(
        title="Commands",
        description="Commands used in various situations:",
        dest="command",
    )

    init_parser = subparsers.add_parser(
        "init", help="Initializes a folder to work with gitorg"
    )

    add_parser = subparsers.add_parser(
        "add", help="Adds a list to the current gitorg workspace"
    )

    status_parser = subparsers.add_parser(
        "status", help="Show the workspace status"
    )

    add_parser.add_argument("list", help="list to add locally")
    add_parser.add_argument("--no-clone", help="Don't automatically clone",
                            default=False, action="store_true")

    return parser


def run(argv):
    parser = build_parser()
    args = parser.parse_args(argv)

    command = args.command
    if command == "init":
        core.init()
    elif command == "add":
        core.add(
            pattern=args.list,
            clone=not args.no_clone,
        )
    elif command == "status":
        core.status()
