import subprocess
# import netrc
from config import get_value, VALUE_HEROKU_TOKEN


def is_toolbelt_installed(
    default_command=["heroku", "--version"],
    default_test_string="heroku-toolbelt"
):

    try:
        p = subprocess.Popen(default_command, stdout=subprocess.PIPE)
    except OSError:
        return False

    version_info = p.stdout.readlines()
    p.kill()

    if len(version_info):
        return version_info[0].startswith(default_test_string)

    return False


def get_token():
    return get_value(VALUE_HEROKU_TOKEN)
