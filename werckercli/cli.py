from clint.textui import colored, puts

from werckercli.git import get_priority
from werckercli import prompt
from werckercli.commands.clearsettings import clear_settings\
    as command_clear_settings


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
        from werckercli.commands.create import create as command_create
        command_create()

    elif args['logout']:
        command_clear_settings()


def enter_url(loop=True):
    while True:

        url = raw_input("Enter a repository url:")

        if url != "":
            print get_priority(url, "custom")
            if get_priority(url, "custom") == 0:
                puts(
                    colored.yellow("Warning:") +
                    " This is not a valid ssh url for github/bitbucket."
                )

                sure = prompt.yn(
                    "Are you sure you want to use this url?",
                    default="n"
                )
                if not sure:
                    url = ""
                else:
                    return url
            else:
                return url

        if not loop:
            return
