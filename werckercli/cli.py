import os
import shutil

import argparse
import textwrap

from clint.textui import puts, colored
from clint.textui import prompt

from werckercli.base import get_access_token
from werckercli.paths import get_global_wercker_path


def print_intro():
    puts()

    puts(23*"-")
    puts(colored.white('welcome to ') + colored.green('wercker-cli'))
    puts(23*"-")
    puts()


def get_parser():
    command_choices = {
        "create": "Add a new project to Wercker",
        "list": "List all deploy targets",
        "deploy": "Deploy to a specific target",
        "status": "Gets the most recent build status of an application",
        "clear-settings":
        "Removes the login token for wercker from this computer",
        "help": "Displays this text and exits"
    }

    description = """wercker-cli for easy commandline access to wercker.

    Commands:"""

    max_length = 0
    for command in command_choices:
        if len(command) > max_length:
            max_length = len(command)

    for command in command_choices:
        description += \
            """\n    """ + \
            command.ljust(max_length) + \
            """ : """ + \
            command_choices[command]

    description += "\n"

    parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        'base_command',
        metavar='<command>',
        type=str,
        help='options are: ' + ', '.join(command_choices.keys()),
        choices=command_choices.keys(),
        nargs="?"
    )

    return parser


def handle_commands(parser, args):

    base_command = args.base_command

    if base_command is None:
        base_command = "help"

    if base_command.lower() == 'help':
        parser.print_help()
    if base_command.lower() == 'create':
        token = get_access_token()

        if not token:
            puts(colored.red("Fatal: could not log in"))

    elif base_command.lower() == 'clear-settings':

        puts(
            "About to clear the wercker settings \
            for the current user on this machine"
        )

        sure = prompt.yn("Are you sure you want to do this?", default="n")

        if sure:
            home = get_global_wercker_path()

            if os.path.isdir(home):
                shutil.rmtree(get_global_wercker_path())
                puts(colored.green("wercker settings removed succesfully."))
            else:
                puts(colored.yellow("no settings found."))
        else:
            puts(colored.yellow("No settings removed"))
