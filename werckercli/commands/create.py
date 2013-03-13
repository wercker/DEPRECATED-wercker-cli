from werckercli.decorators import login_required
from werckercli.git import (
    get_remote_options,
    convert_to_url,
)
from werckercli.cli import get_term, puts
from werckercli.cli import pick_url
from werckercli.git import (
    get_preferred_source_type,
    filter_heroku_sources,
)
from werckercli.config import set_value, VALUE_PROJECT_ID
from werckercli.client import Client
from werckercli.paths import find_git_root

from werckercli.commands.target import add as target_add
from werckercli.commands.project import project_check_repo, project_build


@login_required
def create(path='.', valid_token=None):
    if not valid_token:
        raise ValueError("A valid token is required!")

    term = get_term()
    path = find_git_root(path)

    if not path:
        puts(
            term.red("Error:") +
            " could not find a repository." +
            "wercker create requires a git repository. Create/clone a\
 repository first."
        )
        return

    puts("Searching for git remote information... ")
    options = get_remote_options(path)

    heroku_options = filter_heroku_sources(options)

    options = [o for o in options if o not in heroku_options]

    count = len(options)

    puts(
        "Found %s repository location(s)...\n"
        % term.white(str(count))
    )

    url = pick_url(options)
    url = convert_to_url(url)

    source = get_preferred_source_type(url)
    puts("\n%s repository detected..." % source)
    puts("Selected repository url is %s\n" % url)

    client = Client()

    profile = client.get_profile(valid_token)

    return

    status, response = client.create_project(
        url,
        source,
        valid_token
    )

    if response['success']:

        puts("A new application has been created.")

        set_value(VALUE_PROJECT_ID, response['projectId'])

        puts("A .wercker file has been created which enables the \
link between the source code and wercker.")

        project_check_repo(valid_token=valid_token, failure_confirmation=True)

        puts("trying to find deploy target information (for \
platforms such as Heroku).")

        target_options = heroku_options

        nr_targets = len(target_options)
        puts("%s automatic supported targets found." % str(nr_targets))

        if nr_targets:
            target_add(valid_token=valid_token)

        puts("Triggering initial build...")
        project_build(valid_token=valid_token)

    else:
        puts(
            term.red("Error: ") +
            "Unable to create project. Status: %d. Response: " % status
        )
