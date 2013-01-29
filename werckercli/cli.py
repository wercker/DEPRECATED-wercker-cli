import argparse
import textwrap

from clint.textui import colored

from werckercli.commands.clearsettings import clear_settings\
    as command_clear_settings
from werckercli.commands.create import create as command_create


def get_intro():
    intro = 23*"-"
    intro += "\n"
    intro += colored.white('welcome to ') + colored.green('wercker-cli')
    intro += "\n"
    intro += 23*"-"
    intro += "\n"

    return intro


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
        command_create()

    elif base_command.lower() == 'clear-settings':
        command_clear_settings()
