from werckercli import git
from werckercli.decorators import login_required


@login_required
def add(valid_token=None):

    if not valid_token:
        raise ValueError("A valid token is required!")
