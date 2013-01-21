import os
import shutil

from getpass import getpass
import argparse
import textwrap

from clint.textui import puts, colored
from clint.textui import prompt

from client import Client
puts()

puts(23*"-")
puts(colored.white('welcome to ') + colored.green('wercker-cli'))
puts(23*"-")
puts()
command_choices = {    
    "create": "Add a new project to Wercker",
    "list": "List all deploy targets", 
    "deploy": "Deploy to a specific target", 
    "status": "Gets the most recent build status of an application", 
    "clear-settings": "Removes the login token for wercker from this computer",
    "help": "Displays this text and exits"
}

description = """wercker-cli for easy commandline access to wercker.

    Commands:
    """

max_length = 0;
for command in command_choices:
    if len(command) > max_length:
        max_length = len(command)

for command in command_choices:
    description += """\n        """ + command.ljust(max_length) + """ : """ + command_choices[command]

description += "\n"

parser = argparse.ArgumentParser(
    description=textwrap.dedent(description), 
    formatter_class=argparse.RawDescriptionHelpFormatter)


parser.add_argument('base_command',
    metavar='<command>',
    type=str,
    help='options are: ' + ', '.join(command_choices.keys()),
    choices=command_choices.keys(),
    default="help",
    nargs="?")

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

        puts(
            colored.yellow("warning: ") + 
            "login/password incorrect, please try again.")
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

base_command = args.base_command

if base_command == None:
    base_command = "help"

if base_command.lower() == 'help':
    # print dir(parser)
    # print parser.print_usage()
    parser.print_help()
if base_command.lower() == 'create':
    token = get_access_token()
    pass
elif base_command.lower() == 'clear-settings':

    puts("About to clear the wercker settings for the current user on this machine")
    sure = prompt.yn("Are you sure you want to do this?", default="n")

    if sure:
        home = get_global_wercker_path()

        if os.path.isdir(home):
            shutil.rmtree(get_global_wercker_path())
            puts(colored.green("wercker settings removed succesfully."))
        else:
            puts(colored.yellow("no settings found."))
    else:
        puts(colored.yellow("No settings removed"))