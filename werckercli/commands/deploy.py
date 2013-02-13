import os

from clint.textui import puts, colored, indent

from werckercli import git
from werckercli import heroku
from werckercli.config import get_value, VALUE_PROJECT_ID
from werckercli.decorators import login_required
from werckercli.client import Client


@login_required
def add(valid_token=None):

    if not valid_token:
        raise ValueError("A valid token is required!")

    project_id = get_value(VALUE_PROJECT_ID)
    if not project_id:
        raise ValueError("No project id found")

    options = git.find_heroku_sources(os.curdir)

    if len(options) == 0:
        puts(colored.red("Error: ") + "No heroku remotes found")
    elif len(options) == 1:
        _add_heroku_by_git(valid_token, project_id, options[0].url)


def _add_heroku_by_git(token, project_id, git_url):
    puts("Heroku remote %s selected." % git_url)

    puts("Looking for Heroku API key...")
    heroku_token = heroku.get_token()

    if not heroku_token:
        puts(colored.red("Error: "))
        with indent(2):
            puts("Please make sure the heroku-toolbelt is installed")
            puts("and you are loged in.")
        return

    puts("API key found...")
    puts("Retreiving applications from Heroku...")

    fp = open("werckercli/tests/data/apps.response.json")
    import json
    apps = json.load(fp)
    fp.close()
    # apps = heroku.get_apps()

    preferred_app = None
    for app in apps:
        # print app
        if app['git_url'] == git_url:
            # print app['name']
            preferred_app = app

    if not preferred_app:
        raise ValueError(
            "No matching heroku remote repository found in the \
apps for current heroku user"
        )
    c = Client()

    code, result = c.create_deploy_target(
        token,
        project_id,
        preferred_app['name'],
        heroku_token
    )

    print result
    if 'success' in result and result['success'] is True:
        puts("Heroku deploy target %s \
successfully added to the wercker applicaiton" % preferred_app['name'])

    elif result['errorMessage']:
        puts(colored.red("Error: ") + result['errorMessage'])


def store_highest_length(list_lengths, row, props=None):

    if props:
        values_list = props
    else:
        values_list = row

    # print row, props

    for i in range(len(values_list)):

        if props:
            try:
                value = row[props[i]]
            except KeyError:
                value = '-'
        else:
            value = str(row[i])

        length = len(value)

        if length > list_lengths[i]:
            list_lengths[i] = length


def print_line(list_lengths, row, props=None):

    line = "| "

    if props:
        values_list = props
    else:
        values_list = row

    for i in range(len(values_list)):
        if i > 0:
            line += " | "

        if props:
            try:
                value = row[props[i]]
            except KeyError:
                value = '-'
            value = str(value)
        else:
            value = str(row[i])

        line += value.ljust(list_lengths[i])

    line += " |"

    puts(line)


def print_hr(lengths):
    line = "|" + ((sum(lengths) + (len(lengths) * 3) - 1) * "-") + "|"
    puts(line)


@login_required
def list_by_project(valid_token=None):

    if not valid_token:
        raise ValueError("A valid token is required!")

    project_id = get_value(VALUE_PROJECT_ID)

    if not project_id:
        raise ValueError("No project id found")

    c = Client()

    puts("Retreiving list of deploy targets...")
    code, result = c.get_deploy_targets_by_project(
        valid_token,
        project_id
    )

    header = ['name', 'deploy by', 'deployed on', 'status', 'result']
    props = [
        'name',
        'deployBy',
        'deployFinishedOn',
        'deployStatus',
        'deployResult'
    ]

    max_lengths = []

    for i in range(len(header)):
        max_lengths.append(0)

    store_highest_length(max_lengths, header)

    if 'data' in result:
        puts("Found %d result(s)...\n" % len(result['data']))
        for row in result['data']:
            store_highest_length(max_lengths, row, props)

        print_hr(max_lengths)
        print_line(max_lengths, header)
        print_hr(max_lengths)

        for row in result['data']:
            print_line(max_lengths, row, props)
        print_hr(max_lengths)
