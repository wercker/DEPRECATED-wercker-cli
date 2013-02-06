import os

from clint.textui import puts, colored, indent

from werckercli import git
from werckercli import heroku
from werckercli.decorators import login_required


@login_required
def add(valid_token=None):

    if not valid_token:
        raise ValueError("A valid token is required!")

    options = git.get_heroku_source(os.curdir)

    if len(options) == 0:
        puts(colored.red("Error: ") + "No heroku remotes found")
    elif len(options) == 1:
        _add_heroku_by_git(options[0].url)


def _add_heroku_by_git(git_url):
    token = heroku.get_token()

    if not token:
        puts(colored.red("Error: "))
        with indent(2):
            puts("Please make sure the heroku-toolbelt is installed")
            puts("and you are loged in.")
