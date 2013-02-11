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

    # fp = open('werckercli/tests/data/apps.response.json')
    # import json
    # apps = json.load(fp)
    # fp.close()

    # import mock
    # with mock.patch(
    #     'werckercli.heroku.get_apps',
    #     mock.Mock(return_value=apps)
    # ):
    apps = heroku.get_apps()

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

    result = c.create_deploy_target(
        token,
        project_id,
        preferred_app['name'],
        heroku_token
    )
    print result
