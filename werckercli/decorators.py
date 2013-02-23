from werckercli.authentication import get_access_token


def login_required(f):
    def new_f(*args, **kwargs):
        if not "valid_token" in kwargs:
            token = get_access_token()
            # if token:
            kwargs['valid_token'] = token

        return f(*args, **kwargs)

    new_f.__name__ = f.__name__
    return new_f
