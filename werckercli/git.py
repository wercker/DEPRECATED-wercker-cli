import re

from collections import namedtuple
from dulwich.repo import Repo

GITHUB_PATTERN = '(git@)*(github.com):(?P<name>.*)/(?P<project>.*)'
BITBUCKET_PATTERN = '(git@bitbucket.org):(?P<name>.*)/(?P<project>.*)'
HEROKU_PATTERN = '(git@heroku.com):(?P<name>.*)'

PREFERRED_PATTERNS = [
    GITHUB_PATTERN,
    BITBUCKET_PATTERN
]

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
        if pattern == GITHUB_PATTERN:
            return SOURCE_GITHUB
        if pattern == BITBUCKET_PATTERN:
            return SOURCE_BITBUCKET
        if pattern == HEROKU_PATTERN:
            return SOURCE_HEROKU


def get_username(url):
    source = get_preferred_source_type(url)

    if source == SOURCE_GITHUB:
        match = re.match(GITHUB_PATTERN, url)
        return match.groupdict()['name']
    else:
        match = re.match(BITBUCKET_PATTERN, url)
        return match.groupdict()['name']


def find_heroku_sources(repo_path):

    options = get_remote_options(repo_path)

    heroku_options = []
    for option in options:
        if get_source_type(option.url) == SOURCE_HEROKU:
            heroku_options.append(option)

    return heroku_options
