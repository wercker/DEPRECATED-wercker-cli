import os
# import shutil

from getpass import getpass

from clint.textui import puts, colored
from clint.textui import prompt

from client import Client


from paths import get_global_wercker_path, get_global_wercker_filename, check_or_create_path

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



