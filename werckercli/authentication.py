from getpass import getpass

from werckercli.cli import get_term, puts

from werckercli import client
from werckercli.config import get_value, set_value, VALUE_USER_TOKEN


def do_login(retry_count=2):
    term = get_term()

    username = raw_input("username: ")
    password = getpass("password: ")

    cl = client.Client()
    status, content = cl.request_oauth_token(username, password)

    if status == 200 and content.get('success', False):
        puts("Login successful.")
        return content['result']['token']

    elif retry_count > 0:

        puts(
            term.yellow("warning: ") +
            "login/password incorrect, please try again.\n")
        return do_login(retry_count - 1)


def get_access_token():

    term = get_term()

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
