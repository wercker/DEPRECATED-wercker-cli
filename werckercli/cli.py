import os

from clint.textui import colored, puts, indent

from werckercli.git import get_priority
from werckercli import prompt


def get_intro():
    intro = 23*"-"
    intro += "\n"
    intro += colored.white('welcome to ') + colored.green('wercker-cli')
    intro += "\n"
    intro += 23*"-"
    intro += "\n"

    return intro


def handle_commands(args):
    """ Core handler for redirecting to the proper commands."""

    from werckercli.commands.create import create\
        as command_create
    from werckercli.commands.deploy import add\
        as command_add
    from werckercli.commands.clearsettings import clear_settings\
        as command_clear_settings
    from werckercli.commands.login import login\
        as command_login

    if args['app'] and args['create']:
        command_create()
    elif args['create']:
        command_create()
    elif args['deploy']:
        if args['add']:
            command_add()
    elif args['login']:
        command_login()
    elif args['logout']:
        command_clear_settings()


def enter_url(loop=True):
    """Get an url and validate it, asks confirmation for unsupported urls"""
    while True:

        url = raw_input("Enter a repository url:")

        if url != "":
            print get_priority, get_priority()
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


def pick_url(options):
    """Allows the user to pick one of the options or enter a new locaiton"""
    puts(
        "Please choose one of the following options: ")

    index = 1
    enter_custom_choice = 1
    default_choice = 1

    with indent(indent=1):
        for option in options:
            if(option.priority < 1):
                puts('(%d) %s ' % (index, colored.red(option.url)))
                if(default_choice == index):
                    default_choice += 1
            else:
                to_print = '(%d) %s ' % (index, option.url)

                if(index == default_choice):
                    to_print = colored.green(to_print)
                puts(to_print)
            index += 1

        enter_custom_choice = len(options) + 1

        puts('(%d) enter a new location' % index)

    def option_to_str(i):
        if not i == default_choice:
            return str(i)
        else:
            return str(i) + "=default"

    choices = map(
        option_to_str,
        range(1, index + 1)
    )

    while True:

        url = None

        choice = raw_input(
            "choice (%s): " % (
                ",".join(choices),
            )
        )

        selected = None

        if choice == "":
            selected = default_choice
        elif choice in choices:
            selected = choice

            try:
                selected = int(choice)
            except ValueError:
                selected = None

        elif choice == str(default_choice):
            selected = default_choice
        elif choice == str(enter_custom_choice):
            selected = enter_custom_choice

        if selected:
            if selected == enter_custom_choice:
                url = enter_url()
            else:
                url = options[selected-1].url

            if url:
                return url


def pick_project_name(url):

    project = os.path.basename(url).split(".")[0]

    puts("Detecting project name...")

    return prompt.get_value_with_default("Enter project name: ", project)
