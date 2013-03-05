import re

from collections import namedtuple
from dulwich.repo import Repo

GITHUB_PATTERNS = [
    '(git@)*(github.com):(?P<name>.*)/(?P<project>.*)',
    'https://github.com/(?P<name>.*)/(?P<project>.*)'
]

BITBUCKET_PATTERNS = [
    '(git@bitbucket.org):(?P<name>.*)/(?P<project>.*)',
    'https://(?P<login>.*)@bitbucket.org/(?P<name>.*)/(?P<project>.*)'
]
HEROKU_PATTERNS = ['(git@heroku.com):(?P<name>.*)']

PREFERRED_PATTERNS = GITHUB_PATTERNS + BITBUCKET_PATTERNS

SOURCE_GITHUB = "github"
SOURCE_BITBUCKET = "bitbucket"
SOURCE_HEROKU = "heroku"
SOURCE_UNKNOWN = ""
RemoteOption = namedtuple('RemoteOption', 'url remote priority')


def get_remote_options(repo_path, prio_remote="origin"):

    repo = Repo(repo_path)
    conf = repo.get_config()
    options = []

    for key in conf.keys():
        if 'remote' in key:

            url = conf.get(key, 'url')
            remote = key[1]

            option = RemoteOption(
                url,
                remote,
                get_priority(
                    url,
                    remote,
                    prio_remote=prio_remote
                )
            )

            options.append(option)

    options = sorted(options, key=lambda i: i.priority, reverse=True)
    return options


def get_priority(url, remote, prio_remote="origin"):
    if get_preferred_source_type(url):
        if remote == prio_remote:
            return 2
        else:
            return 1
    return 0


def get_preferred_source_type(url):
    for pattern in PREFERRED_PATTERNS:
        result = get_source_type(url, pattern)

        if result is not None:
            return result


def get_source_type(url, pattern):
    if re.search(pattern, url):
        if pattern in GITHUB_PATTERNS:
            return SOURCE_GITHUB
        if pattern in BITBUCKET_PATTERNS:
            return SOURCE_BITBUCKET
        if pattern in HEROKU_PATTERNS:
            return SOURCE_HEROKU


def get_username(url):
    source = get_preferred_source_type(url)

    if source == SOURCE_GITHUB:

        for pattern in GITHUB_PATTERNS:
            match = re.match(pattern, url)

            if match:
                return match.groupdict()['name']
    else:

        for pattern in BITBUCKET_PATTERNS:
            match = re.match(pattern, url)

            if match:
                return match.groupdict()['name']


def find_heroku_sources(repo_path):

    options = get_remote_options(repo_path)

    heroku_options = []
    for option in options:
        for pattern in HEROKU_PATTERNS:
            if get_source_type(option.url, pattern) == SOURCE_HEROKU:
                heroku_options.append(option)

    return heroku_options


def convert_to_url(url):
    match = None
    source_type = None

    for pattern in GITHUB_PATTERNS:
        match = re.match(pattern, url)

        if match:
            source_type = SOURCE_GITHUB
            break

    if not source_type:
        for pattern in BITBUCKET_PATTERNS:
            match = re.match(pattern, url)

            if match:
                source_type = SOURCE_BITBUCKET
                break

    if source_type == SOURCE_BITBUCKET:
        source_dict = match.groupdict()
        return "git@bitbucket.org:{owner}/{project}".format(
            owner=source_dict['name'],
            project=source_dict['project']
        )
    if source_type == SOURCE_GITHUB:
        source_dict = match.groupdict()
        return "git@github.com:{owner}/{project}".format(
            owner=source_dict['name'],
            project=source_dict['project']
        )

    return url
