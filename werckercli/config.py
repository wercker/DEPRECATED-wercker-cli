import os
import stat
from urlparse import urlparse
import ConfigParser

# from clint.textui import puts, colored
from werckercli.cli import puts, get_term

import netrc
from werckercli.paths import find_git_root

VALUE_USER_TOKEN = "user_token"
VALUE_PROJECT_ID = "project_id"
VALUE_HEROKU_TOKEN = "heroku_netrc_password"
VALUE_WERCKER_URL = "wercker_url"

DEFAULT_WERCKER_URL = "https://app.wercker.com"
DEFAULT_DOT_WERCKER_NAME = ".wercker"


def _get_or_create_netrc_location():
    term = get_term()
    try:
        file = os.path.join(os.environ['HOME'], ".netrc")
    except KeyError:
        raise IOError("Could not find .netrc: $HOME is not set")

    if os.path.isfile(file):
        result = os.stat(file)
        mode = oct(stat.S_IMODE(result.st_mode))
        if mode != '0600':
            puts(
                term.yellow('warning:') +
                'Found permission %s, on %s. It should be 0600' %
                (mode, file)
            )

    else:
        with os.fdopen(os.open(file, os.O_APPEND | os.O_CREAT, 0o600)) as out:
            out.close()

    return file


def get_value(name, default_value=None, path=os.curdir):
    value = None
    term = get_term()

    if name == VALUE_WERCKER_URL:
        if 'wercker_url' in os.environ.keys():
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
        # from paths import find_git_root

        path = find_git_root(path)

        if not path:
            puts(
                term.red("Error:") +
                " could not find a git repository."
            )
            return

        file = os.path.join(
            path,
            DEFAULT_DOT_WERCKER_NAME
        )

        if not os.path.isfile(file):
            puts(
                term.yellow("Warning:") +
                " could not find a %s file in the application root" %
                DEFAULT_DOT_WERCKER_NAME
            )

            return

        Config = ConfigParser.ConfigParser()

        Config.read(file)

        try:
            value = Config.get('project', 'id')
        except (
            ConfigParser.NoOptionError,
            ConfigParser.NoSectionError
        ):
            value = None

    return value


def set_value(name, value):

    term = get_term()

    if name == VALUE_USER_TOKEN:

        file = _get_or_create_netrc_location()

        rc = netrc.netrc(file=file)

        wercker_url = get_value(VALUE_WERCKER_URL)
        url = urlparse(wercker_url)

        if url.hostname in rc.hosts:
            current_settings = rc.hosts[url.hostname]
        else:
            current_settings = (None, None, None)

        if value is not None:
            rc.hosts[url.hostname] = (
                current_settings[0],
                current_settings[1],
                value
            )
        else:
            rc.hosts.pop(url.hostname)

        with open(file, 'w') as fp:
            fp.write(str(rc))
            fp.close()
    elif name == VALUE_PROJECT_ID:

        path = find_git_root(os.curdir)

        if not path:
            puts(
                term.red("Error:") +
                " could not find the root repository."
            )
            return

        file = os.path.join(
            path,
            DEFAULT_DOT_WERCKER_NAME
        )

        Config = ConfigParser.ConfigParser()

        if os.path.isfile(file):

            Config.read(file)

        if not 'project' in Config.sections():
            Config.add_section('project')

        fp = open(file, 'w')
        Config.set('project', 'id', value)

        Config.write(fp)

        fp.close()
