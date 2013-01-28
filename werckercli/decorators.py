from werckercli.base import get_access_token


def login_required(f):
    def new_f():
        # print "Entering", f.__name__
        # print "entering"
        token = get_access_token()
        print token
        if token:
            f(valid_token=token)
        # print "Exited", f.__name__

    new_f.__name__ = f.__name__
    return new_f
