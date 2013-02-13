from clint.textui import puts, colored

from werckercli.decorators import login_required
from werckercli.git import get_remote_options
from werckercli.cli import pick_url, pick_project_name
from werckercli.git import get_preferred_source_type
from werckercli.client import Client


@login_required
def create(path='.', valid_token=None):
    if not valid_token:
        raise ValueError("A valid token is required!")

    puts("Searching for git remote information... ")
    options = get_remote_options(path, )

    count = len(options)

    puts(
        "Found %s repository location(s)...\n"
        % colored.white(str(count))
    )

    url = pick_url(options)

    source = get_preferred_source_type(url)
    puts("\n%s repository detected..." % source)
    puts("Selected repository url is %s\n" % url)

    project = pick_project_name(url)

    client = Client()

    status, response = client.create_project(
        url,
        # user,
        project,
        source,
        valid_token
    )

    if response['success']:
        print "Project has been created"
    else:
        print "Unable to create project. Status: %d. Response: " % status
        print response
