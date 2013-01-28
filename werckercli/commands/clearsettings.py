import os
import shutil

from clint.textui import puts, prompt, colored

from werckercli.paths import get_global_wercker_path


def clear_settings():
    puts(
        "About to clear the wercker settings \
        for the current user on this machine"
    )

    # sure = prompt.yn("Are you sure you want to do this?", default="n")
    sure = True

    print sure
    if sure:
        home = get_global_wercker_path()
        print home

        if os.path.isdir(home):
            shutil.rmtree(get_global_wercker_path())
            puts(colored.green("wercker settings removed succesfully."))
            return True
        else:
            puts(colored.yellow("no settings found."))
    else:
        puts(colored.yellow("No settings removed"))

    return False
