import os
# import shutil

from getpass import getpass

from clint.textui import puts, colored
from clint.textui import prompt

from client import Client

def get_global_wercker_path():
    return os.path.join(os.environ['HOME'], '.wercker')


def get_global_wercker_filename():
    return os.path.join(get_global_wercker_path(), 'credentials')


def check_or_create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)

    return True


def do_login(retry_count=2):
    username = raw_input("username: ")
    password = getpass("password: ")

    client = Client()
    status, content = client.request_oauth_token(username, password)

    if status == 200 and content.get('success', False) == True:
        return content['result']['token']

    elif retry_count > 0:

        puts(
            colored.yellow("warning: ") +
            "login/password incorrect, please try again.")
        do_login(retry_count - 1)


def get_access_token():

    token = None

    home = get_global_wercker_path()
    check_or_create_path(home)

    credentials = get_global_wercker_filename()

    if os.path.isfile(credentials):
        fh = open(credentials, 'r')
        token = fh.readlines()
        fh.close()

    if not token:
        token = do_login()

        if not token:
            return
        fh = open(credentials, 'w+')

        fh.write(token)
        fh.close()

    return token


def getGitRoot(path):
    """Find the nearest parent with a .git folder"""

    if path == os.path.curdir:
        path = os.path.realpath(path)

    if os.path.isdir(path):
        if os.path.isdir(os.path.join(path, '.git')):
            return path
        else:
            parent = os.path.realpath(os.path.join(path, os.path.pardir))
            if parent == path:
                return None
            return getGitRoot(parent)

