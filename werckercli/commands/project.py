import os

from werckercli.decorators import login_required
from werckercli.git import get_remote_options, convert_to_url
from werckercli.cli import get_term, puts
from werckercli.client import Client
from werckercli.printer import (
    print_hr,
    print_line,
    store_highest_length,
    format_date
)
from werckercli.config import get_value, set_value, VALUE_PROJECT_ID
from werckercli.commands.build import get_builds, print_builds
from werckercli.commands.target import get_targets


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
            # print option.url, app['url']
            if convert_to_url(app['url']) == convert_to_url(option.url):
                set_value(VALUE_PROJECT_ID, app['id'])
                return


@login_required
def project_check_repo(valid_token=None, failure_confirmation=False):
    if not valid_token:
        raise ValueError("A valid token is required!")

    term = get_term()

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
                    puts(
                        term.yellow("Warning: ") +
                        response['data']['details']
                    )
                else:
                    puts(
                        term.yellow("Warning: ") +
                        "Werckerbot has no access to this repository."

                    )

                if failure_confirmation is True:
                    from werckercli import prompt

                    exit = not prompt.yn(
                        "Please make sure the permissions on the\
 project are correct, do you want wercker to check the permissions again?",
                        default="y"
                    )
                else:
                    exit = True

                if exit:
                    break


@login_required
def project_build(valid_token=None):
    if not valid_token:
        raise ValueError("A valid token is required!")

    term = get_term()

    puts("Triggering build")

    c = Client()
    code, response = c.trigger_build(valid_token, get_value(VALUE_PROJECT_ID))

    if response['success'] is False:
        if "errorMessage" in response:
            puts(term.red("Error: ") + response['errorMessage'])
        else:
            puts("Unable to trigger a build on the default/master branch")
    else:
        puts("A new build has been created")
    # print code, response


@login_required
def project_list_queue(valid_token=None):
    if not valid_token:
        raise ValueError("A valid token is required!")

    project_id = get_value(VALUE_PROJECT_ID)

    if not project_id:
        raise ValueError("No project id found")

    term = get_term()

    puts("Retreiving list of unfinished builds.")

    result = get_builds(valid_token, project_id)

    unknowns = filter(lambda r: r['result'] == "unknown", result)

    print_builds(unknowns)
    # print unknowns

    result = get_targets(valid_token, project_id)

    for target in result['data']:
        # print target['id']
        c = Client()
        code, deploys = c.get_deploys(valid_token, target['id'])

        # print result
        # puts("Target: " + term.yellow(target['name']))

        if 'data' in deploys:

            unknowns = filter(
                lambda d: d['result'] == 'unknown',
                deploys['data']
            )

            puts(("Found {amount} scheduled deploys for {target}").format(
                amount=len(unknowns),
                target=term.bold(target['name'])
            ))

            print_deploys(unknowns)

    # print "List of scheduled deploys:"


def print_deploys(deploys, print_index=False):

    for data in deploys:
        if 'creationDate' in data:
            data['creationDate'] = \
                format_date(data['creationDate'])

        if "progress" in data:
            data['progress'] = "{progress:.1f}%".format(
                progress=data['progress'])
        # if 'commitHash' in data:
        #     data['commitHash'] = data['commitHash'][:8]

    header = [
        # 'target',
        'result',
        'progress',
        'deploy by',
        'created',
        # 'branch',
        # 'commit',
        # 'status',
        # 'message'
    ]

    props = [
        # 'name',
        'result',
        'progress',
        'byUsername',
        'creationDate',
        # 'branch',
        # 'commitHash',
        # 'deployStatus',
        # 'commitMessage',
    ]

    if print_index:
        header = [''] + header
        props = ['index'] + props

    max_lengths = []

    for i in range(len(header)):
        max_lengths.append(0)

    store_highest_length(max_lengths, header)

    # if 'data' in result:
    # puts("Found %d result(s)...\n" % len(result['data']))
    index = 0

    for row in deploys:
        if print_index:
            row['index'] = index + 1
        index += 1
        store_highest_length(max_lengths, row, props)

    print_hr(max_lengths, first=True)
    print_line(max_lengths, header)
    print_hr(max_lengths)

    for row in deploys:
        print_line(max_lengths, row, props)
    print_hr(max_lengths)
