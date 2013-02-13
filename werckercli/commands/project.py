from clint.textui import puts
from werckercli.decorators import login_required

from werckercli.client import Client
from werckercli.printer import print_hr, print_line, store_highest_length


@login_required
def project_list(valid_token=None):

    if not valid_token:
        raise ValueError("A valid token is required!")

    c = Client()

    # c.do_post()

    response, result = c.get_applications(valid_token)

    header = ['Author', 'name', 'status', 'followers', 'url']
    props = [
        'author',
        'name',
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

    print_hr(max_lengths, first=True)
    print_line(max_lengths, header)
    print_hr(max_lengths)

    for row in result:
        print_line(max_lengths, row, props)
    print_hr(max_lengths)
