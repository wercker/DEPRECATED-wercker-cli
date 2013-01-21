import os
import shutil

from getpass import getpass
import argparse

from clint.textui import puts, colored
from clint.textui import prompt

from client import Client


puts('welcome to ' + colored.white('wercker-cli'))
command_choices = ("create", "list", "deploy", "status", "clear-settings")
parser = argparse.ArgumentParser(description='wercker-cli for handling.')
parser.add_argument('base_command', metavar='<command>', type=str,
                   help='options are: ' + ', '.join(command_choices),
                   choices=command_choices)

args = parser.parse_args()


def get_global_wercker_path():
    return os.path.join(os.environ['HOME'], '.wercker')


def get_global_wercker_filename():
    return os.path.join(get_global_wercker_path(), 'credentials')


def check_or_create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)

    return True


def do_login(retry_count=3):
    username = raw_input("username: ")
    password = getpass("password: ")

    client = Client()
    status, content = client.request_oauth_token(username, password)

    if status == 200 and content.get('success', False) == True:
        return content['result']['token']
    elif retry_count > 0:
        puts(colored.yellow("warning: ") + "login/password incorrect, please try again.")
        do_login()


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

        fh = open(credentials, 'w+')

        fh.write(token)
        fh.close()

    return token

if args.base_command.lower() == 'create':
    # print do_login()
    print get_access_token()
elif args.base_command.lower() == 'clear-settings':

    puts("About to clear the wercker settings for the current user on this machine")
    sure = prompt.yn("Are you sure you want to do this?", default="n")

    print sure
    if sure:
        home = get_global_wercker_path()

        if os.path.isdir(home):
            shutil.rmtree(get_global_wercker_path())
            puts(colored.green("wercker settings removed succesfully."))
        else:
            puts(colored.yellow("no settings found."))
    else:
        puts("No settings removed")