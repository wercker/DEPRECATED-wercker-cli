from clint.textui import puts, colored

from werckercli.decorators import login_required
from werckercli.git import get_remote_options
from werckercli.cli import pick_url


@login_required
def create(path='.', valid_token=None):
    if not valid_token:
        raise ValueError("A valid token is required!")

    puts("Searching for git remote information... ")
    options = get_remote_options(path, )

    count = len(options)

    if count == 0:
        raise NotImplementedError("No remotes found")
    else:
        puts(
            "Found %s repository location(s)...\n"
            % colored.white(str(count))
        )

        url = pick_url()

        return url
