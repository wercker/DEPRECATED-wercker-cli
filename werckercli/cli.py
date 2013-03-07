from __future__ import print_function
import os

from blessings import Terminal

from werckercli.git import get_priority
from werckercli import prompt

term = Terminal()


def puts(content):
    # print_function content
    print(content)
    # pass


def get_intro():
    intro = 23*"-"
    intro += "\n"
    intro += 'welcome to ' + term.green('wercker-cli')
    intro += "\n"
    intro += 23*"-"
    intro += "\n"

    return intro


def handle_commands(args):
    """ Core handler for redirecting to the proper commands."""

    # print args

    from werckercli.commands.create import create\
        as command_create
    from werckercli.commands.project import project_list\
        as command_project_list
    from werckercli.commands.project import project_link\
        as command_project_link
    from werckercli.commands.project import project_check_repo\
        as command_project_check_repo
    from werckercli.commands.project import project_build\
        as command_project_build
    from werckercli.commands.build import build_list\
        as command_builds_list
    from werckercli.commands.build import build_deploy\
        as command_builds_deploy
    from werckercli.commands.target import add\
        as command_add
    from werckercli.commands.target import list_by_project\
        as command_list_by_project
    from werckercli.commands.target import link_to_deploy_target\
        as command_target_details
    from werckercli.commands.clearsettings import clear_settings\
        as command_clear_settings
    from werckercli.commands.login import login\
        as command_login

    try:
        if args['apps'] and args['create']:
            command_create()
        elif args['create']:
            command_create()
        elif args['status']:
            command_builds_list(limit=1)
        elif args['deploy']:
            command_builds_deploy()
        elif args['apps']:
            if args['list']:
                command_project_list()
            elif args['link']:
                command_project_link()
            elif args['checkrepo']:
                command_project_check_repo()
            elif "build" in args and args["build"]:
                command_project_build()
        elif args["builds"]:
            if args['list']:
                command_builds_list()
            if args['deploy']:
                command_builds_deploy()
        elif args['targets']:
            if args['add']:
                command_add()
            elif args['list']:
                command_list_by_project()
            elif args['details'] or args['open']:
                command_target_details()
        elif args['login']:
            command_login()
        elif args['logout']:
            command_clear_settings()
    except KeyboardInterrupt:
        puts("\nAborted...")


def enter_url(loop=True):
    """Get an url and validate it, asks confirmation for unsupported urls"""
    while True:

        url = raw_input("Enter a repository url:")

        if url != "":
            if get_priority(url, "custom") == 0:
                puts(
                    term.yellow("Warning:") +
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

    for option in options:
        if(option.priority < 1):
            puts(' (%d) %s ' % (index, term.red(option.url)))
            if(default_choice == index):
                default_choice += 1
        else:
            to_print = ' (%d) %s ' % (index, option.url)

            if(index == default_choice):
                to_print = term.green(to_print)
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
