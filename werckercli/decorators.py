from werckercli.base import get_access_token


def login_required(f):
    def new_f(*args, **kwargs):
        token = get_access_token()
        if token:
            return f(valid_token=token, *args, **kwargs)

    new_f.__name__ = f.__name__
    return new_f
