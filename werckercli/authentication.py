from getpass import getpass

from werckercli.cli import term, puts

from werckercli.client import Client
from werckercli.config import get_value, set_value, VALUE_USER_TOKEN


def do_login(retry_count=2):
    username = raw_input("username: ")
    password = getpass("password: ")

    client = Client()
    status, content = client.request_oauth_token(username, password)

    if status == 200 and content.get('success', False):
        puts("Login successful.")
        return content['result']['token']

    elif retry_count > 0:

        puts(
            term.yellow("warning: ") +
            "login/password incorrect, please try again.\n")
        return do_login(retry_count - 1)


def get_access_token():

    puts("Looking for login token...")

    token = get_value(VALUE_USER_TOKEN)

    if not token:
        puts(term.yellow("Token not found\n"))
        puts("Attempting to log in...")
        token = do_login()

        if not token:
            return

        # print token

        set_value(VALUE_USER_TOKEN, token)
        puts("Token saved. \n")

    return token
