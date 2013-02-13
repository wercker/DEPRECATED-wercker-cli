# import os
# import shutil

from clint.textui import puts, colored

from werckercli import prompt
# from werckercli.paths import get_global_wercker_path
from werckercli import config


def clear_settings():

    # home = get_global_wercker_path()
    # print home

    if config.get_value(config.VALUE_USER_TOKEN):
        puts(
            """About to clear the wercker settings \
for the current user on this machine"""
        )
        sure = prompt.yn("Are you sure you want to do this?", default="n")
        if sure:
            # shutil.rmtree(get_global_wercker_path())
            config.set_value(config.VALUE_USER_TOKEN, None)
            puts(colored.green("wercker settings removed succesfully."))
            return True
        else:
            puts(colored.yellow("cancelled."))
    else:
        puts(colored.yellow("no settings found."))

    # return False
