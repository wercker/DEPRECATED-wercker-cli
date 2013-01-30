
from werckercli.decorators import login_required


@login_required
def create(valid_token=None):
    return unprotected_create(valid_token=None)


def unprotected_create(valid_token=None):

    print valid_token
    if not valid_token:
        raise ValueError("A valid token is required!")
