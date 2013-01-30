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


def handle_commands(args):

    if args['create']:
        command_create()

    elif args['logout']:
        command_clear_settings()
