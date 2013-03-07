from werckercli.decorators import login_required
from werckercli.git import (
    get_remote_options,
    convert_to_url,
)
from werckercli.cli import term, puts
from werckercli.cli import pick_url
from werckercli.git import (
    get_preferred_source_type,
    find_heroku_sources
)
from werckercli.config import set_value, VALUE_PROJECT_ID
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
        % term.white(str(count))
    )

    url = pick_url(options)
    url = convert_to_url(url)

    source = get_preferred_source_type(url)
    puts("\n%s repository detected..." % source)
    puts("Selected repository url is %s\n" % url)

    client = Client()

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

        from werckercli.commands.project import project_check_repo

        project_check_repo(valid_token=valid_token, failure_confirmation=True)

        puts("trying to find deploy target information (for \
platforms such as Heroku).")

        target_options = find_heroku_sources(path)

        nr_targets = len(target_options)
        puts("%s automatic supported targets found." % str(nr_targets))

        if nr_targets:
            from werckercli.commands.target import add as target_add

            target_add(valid_token=valid_token)

        from werckercli.commands.project import project_build

        puts("Triggering initial build...")
        project_build(valid_token=valid_token)

    else:
        puts(
            term.red("Error: ") +
            "Unable to create project. Status: %d. Response: " % status
        )

        # print response
