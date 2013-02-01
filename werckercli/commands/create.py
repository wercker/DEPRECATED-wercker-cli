import os

from clint.textui import puts, colored, indent

from werckercli.decorators import login_required
from werckercli.git import get_remote_options


@login_required
def create(valid_token=None):
    if not valid_token:
        raise ValueError("A valid token is required!")

    puts("Searching for git remote information... ")
    options = get_remote_options(os.curdir)

    count = len(options)

    if count == 0:
        raise NotImplementedError("No remotes found")
    else:
        puts(
            "Found %s repository location(s)...\n"
            % colored.white(str(count))
        )
        puts(
            "Please choose one of the following options: ")

        index = 1
        default_choice = 1

        with indent(indent=1):
            for option in options:
                if(option.priority < 1):
                    puts('(%d) %s ' % (index, colored.red(option.url)))
                    if(default_choice == index):
                        default_choice += 1
                else:
                    to_print = '(%d) %s ' % (index, option.url)

                    if(index == default_choice):
                        to_print = colored.green(to_print)
                    puts(to_print)
                index += 1

            puts('(%d) enter a new location' % index)

        def option_to_str(i):
            if not i == default_choice:
                return str(i)
            else:
                return str(i) + "=default"

        choices = map(
            option_to_str,
            range(1, index + 1)
        )


        while True:
            choice = raw_input(
                "choice: (%s)" % (
                    ",".join(choices),
                )
            )

            selected = None
            if choice in choices:
                selected = choice
                try:
                    int()
            if choice == str(default_choice):

