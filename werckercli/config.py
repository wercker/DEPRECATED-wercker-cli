import os
import stat
from urlparse import urlparse
import netrc

from clint.textui import puts, colored

# from .paths import (
    # get_global_wercker_path,
    # get_global_wercker_filename,
    # check_or_create_path
# )


VALUE_USER_TOKEN = "user_token"
VALUE_PROJECT_ID = "project_id"
VALUE_HEROKU_TOKEN = "heroku_netrc_password"
VALUE_WERCKER_URL = "wercker_url"

DEFAULT_WERCKER_URL = "https://app.wercker.com"


def _get_or_create_netrc_location():
    try:
        file = os.path.join(os.environ['HOME'], ".netrc")
    except KeyError:
        raise IOError("Could not find .netrc: $HOME is not set")

    if os.path.isfile(file):
        result = os.stat(file)
        mode = oct(stat.S_IMODE(result.st_mode))
        if mode != '0600':
            puts(
                colored.yellow('warning:') +
                'Found permission %s, on %s. It should be 0600' %
                (mode, file)
            )

    else:
        with os.fdopen(os.open(file, os.O_APPEND | os.O_CREAT, 0o600)) as out:
            out.close()

    return file


def get_value(name, default_value=None):
    value = None

    if name == VALUE_WERCKER_URL:
        if 'wercker_url' in os.environ:
            value = os.environ.get("wercker_url")
        else:
            value = DEFAULT_WERCKER_URL

        return value

    elif name == VALUE_USER_TOKEN:

        wercker_url = get_value(VALUE_WERCKER_URL)
        url = urlparse(wercker_url)

        file = _get_or_create_netrc_location()
        rc = netrc.netrc(file)

        if url.hostname in rc.hosts:
            value = rc.hosts[url.hostname][2]

    elif name == VALUE_HEROKU_TOKEN:

        file = _get_or_create_netrc_location()
        rc = netrc.netrc(file)

        result = rc.authenticators('api.heroku.com')
        if result and len(result) == 3:
            value = result[2]

    elif name == VALUE_PROJECT_ID:
        raise NotImplementedError("PROJECT_ID retreival not implemented yet")

    return value


def set_value(name, value):
    if name == VALUE_USER_TOKEN:

        file = _get_or_create_netrc_location()

        rc = netrc.netrc(file=file)

        wercker_url = get_value(VALUE_WERCKER_URL)
        url = urlparse(wercker_url)

        if url.hostname in rc.hosts:
            current_settings = rc.hosts[url.hostname]
        else:
            current_settings = (None, None, None)

        rc.hosts[url.hostname] = (
            current_settings[0],
            current_settings[1],
            value
        )

        with open(file, 'w') as fp:
            fp.write(str(rc))
            fp.close()
    elif name == VALUE_PROJECT_ID:
        raise NotImplementedError("PROJECT_ID storing not implemented yet")
