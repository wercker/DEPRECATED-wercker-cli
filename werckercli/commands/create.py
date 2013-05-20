from werckercli.decorators import login_required

from werckercli.git import (
    get_remote_options,
    convert_to_url,
)

from werckercli import prompt

from werckercli.cli import (
    get_term,
    puts,
    pick_url
)

from werckercli.git import (
    get_preferred_source_type,
    filter_heroku_sources,
    get_source_type,
    get_username,
    get_project,
    SOURCE_BITBUCKET,
    SOURCE_GITHUB,
)

from werckercli.config import (
    set_value,
    get_value,
    VALUE_PROJECT_ID,
    VALUE_WERCKER_URL
)
from werckercli.client import Client
from werckercli.paths import find_git_root

from werckercli.commands.target import add as target_add
from werckercli.commands.project import (
    project_check_repo,
    project_build,
    project_link
)


'''
Please choose one of the following options:
 (1) git@github.com:wercker/wercker-cli
Make your choice (1=default):

Creating a new application
a new application has been created.
In the root of this repository a .wercker file has been created which enables\
 the link between the source code and wercker.


Checking werckerbot permissions on the repository...
Werckerbot has access
'''


@login_required
def create(path='.', valid_token=None):
    if not valid_token:
        raise ValueError("A valid token is required!")

    term = get_term()

    if get_value(VALUE_PROJECT_ID, print_warnings=False):
        puts("A .wercker file was found.")
        run_create = prompt.yn(
            "Are you sure you want to run `wercker create`?",
            default="n")

        if run_create is False:
            puts("Aborting.")
            return
        else:
            puts("")

    if project_link(
        valid_token=valid_token,
        puts_result=False,
        auto_link=False
    ):
        puts("A matching application was found on wercker.")
        use_link = prompt.yn("Do you want to run 'wercker link' instead of\
 `wercker create`?")

        puts("")

        if use_link is True:
            project_link(valid_token=valid_token)
            return

    path = find_git_root(path)

    if path:
        options = get_remote_options(path)

        heroku_options = filter_heroku_sources(options)
    else:
        options = []
        heroku_options = []

    if not path:
        return False

    puts('''About to create an application on wercker.

This consists of the following steps:
1. Validate permissions and create an application
2. Add a deploy target ({heroku_options} heroku targets detected)
3. Trigger initial build'''.format(
        wercker_url=get_value(VALUE_WERCKER_URL),
        heroku_options=len(heroku_options))
    )

    if not path:
        puts(
            term.red("Error:") +
            " Could not find a repository." +
            " wercker create requires a git repository. Create/clone a\
 repository first."
        )
        return

    options = [o for o in options if o not in heroku_options]

    options = [o for o in options if o.priority > 1]

    count = len(options)
    puts('''
Step ''' + term.white('1') + '''.
-------------
''')
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

    code, profile = client.get_profile(valid_token)

    source_type = get_source_type(url)

    if source_type == SOURCE_BITBUCKET:
        if profile.get('hasBitbucketToken', False) is False:
            puts("No Bitbucket account linked with your profile. Wercker uses\
 this connection to linkup some events for your repository on Bitbucket to our\
  service.")
            provider_url = get_value(
                VALUE_WERCKER_URL
            ) + '/provider/add/cli/bitbucket'

            puts("Launching {url} to start linking.".format(
                url=provider_url
            ))
            from time import sleep

            sleep(5)
            import webbrowser

            webbrowser.open(provider_url)

            raw_input("Press enter to continue...")
    elif source_type == SOURCE_GITHUB:
        if profile.get('hasGithubToken', False) is False:
            puts("No GitHub account linked with your profile. Wercker uses\
 this connection to linkup some events for your repository on GitHub to our\
 service.")
            provider_url = get_value(
                VALUE_WERCKER_URL
            ) + '/provider/add/cli/github'

            puts("Launching {url} to start linking.".format(
                url=provider_url
            ))

            from time import sleep

            sleep(5)

            import webbrowser

            webbrowser.open(provider_url)

            raw_input("Press enter to continue...")

    puts("Creating a new application")
    status, response = client.create_project(
        url,
        source,
        valid_token
    )

    if response['success']:

        puts("a new application has been created.")

        set_value(VALUE_PROJECT_ID, response['projectId'])

        puts("In the root of this repository a .wercker file has been created\
 which enables the link between the source code and wercker.\n")

        site_url = None

        if source_type == SOURCE_GITHUB:

            site_url = "https://github.com/" + \
                get_username(url) + \
                "/" + \
                get_project(url)

        elif source_type == SOURCE_BITBUCKET:

            site_url = "https://bitbucket.org/" + \
                get_username(url) + \
                "/" + \
                get_project(url)

        project_check_repo(
            valid_token=valid_token,
            failure_confirmation=True,
            site_url=site_url
        )

#         puts("\nSearching for deploy target information (for \
# platforms such as Heroku).")

        puts('''
Step ''' + term.white('2') + '''.
-------------
''')

        target_options = heroku_options

        nr_targets = len(target_options)
        puts("%s automatic supported target(s) found." % str(nr_targets))

        if nr_targets:
            target_add(valid_token=valid_token)

        puts('''
Step ''' + term.white('3') + '''.
-------------
''')

        project_build(valid_token=valid_token)
        # if project_build(valid_token=valid_token):
            # puts("To trigger a build")
            # puts("")

        puts('''
Done.
-------------

You are all set up to for using wercker. You can trigger new builds by
committing and pushing your latest changes.

Happy coding!''')
    else:
        puts(
            term.red("Error: ") +
            "Unable to create project. \n\nResponse: %s\n" %
            (response.get('errorMessage'))
        )
        puts('''
Note: only repository where the wercker's user has permissions on can be added.
This is because some event hooks for wercker need to be registered on the
repository. If you want to test a public repository and don't have permissions
 on it: fork it. You can add the forked repository to wercker''')
