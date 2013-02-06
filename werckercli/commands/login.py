# from werckercli.decorators import login_required
from werckercli.authentication import get_access_token


def login():
    get_access_token()
