import os

from clint.textui import puts
from werckercli.decorators import login_required
from werckercli.git import get_remote_options

from werckercli.client import Client
from werckercli.printer import print_hr, print_line, store_highest_length
from werckercli.config import get_value, set_value, VALUE_PROJECT_ID


@login_required
def project_list(valid_token=None):

    if not valid_token:
        raise ValueError("A valid token is required!")

    c = Client()

    response, result = c.get_applications(valid_token)

    header = ['name', 'author', 'status', 'followers', 'url']
    props = [
        'name',
        'author',
        'status',
        'totalFollowers',
        'url'
    ]

    max_lengths = []

    for i in range(len(header)):
        max_lengths.append(0)

    store_highest_length(max_lengths, header)

    puts("Found %d result(s)...\n" % len(result))
    for row in result:
        store_highest_length(max_lengths, row, props)

    result = sorted(result, key=lambda k: k['name'])
    print_hr(max_lengths, first=True)
    print_line(max_lengths, header)
    print_hr(max_lengths)

    for row in result:
        print_line(max_lengths, row, props)
    print_hr(max_lengths)


@login_required
def project_link(valid_token=None):
    if not valid_token:
        raise ValueError("A valid token is required!")

    puts("Searching for git remote information... ")
    options = get_remote_options(os.curdir)

    puts("Retreiving list of applications...")
    c = Client()

    response, result = c.get_applications(valid_token)

    for option in options:
        for app in result:
            if app['url'] == option.url:
                set_value(VALUE_PROJECT_ID, app['id'])
                return


@login_required
def project_check_repo(valid_token=None, failure_confirmation=False):
    if not valid_token:
        raise ValueError("A valid token is required!")

    puts("Checking permissions...")

    while(True):

        c = Client()
        code, response = c.check_permissions(
            valid_token,
            get_value(VALUE_PROJECT_ID)
        )

        if response['success'] is True:
            if response['data']['hasAccess'] is True:
                puts("Werckerbot has access")
                break
            else:
                if "details" in response['data']:
                    # puts
                    puts(response['data']['details'])
                else:
                    puts("Werckerbot has no access")
                from werckercli import prompt
                exit = prompt.yn("wercker might not be able to access\
 your repository, are you sure you want to continue?", default="n")
                if exit:
                    break


@login_required
def project_build(valid_token=None):
    if not valid_token:
        raise ValueError("A valid token is required!")

    puts("Triggering build")

    c = Client()
    code, response = c.trigger_build(valid_token, get_value(VALUE_PROJECT_ID))

    # print code, response
