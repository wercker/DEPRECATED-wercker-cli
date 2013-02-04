import re

from collections import namedtuple
from dulwich.repo import Repo

GITHUB_PATTERN = '(git@)*(github.com):(?P<name>.*)/(?P<project>.*)'
BITBUCKET_PATTERN = '(git@bitbucket.org):(?P<name>.*)/(?P<project>.*)'

PREFERRED_PATTERNS = [
    GITHUB_PATTERN,
    BITBUCKET_PATTERN
]

SOURCE_GITHUB = "github"
SOURCE_BITBUCKET = "bitbucket"

RemoteOption = namedtuple('RemoteOption', 'url remote priority')


def get_remote_options(repo_path, prio_remote="origin"):

    # from subprocess import call
    # sts = call("ls", " -la " + repo_path, shell=True)
    # print sts
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
    if get_source_type(url):
        if remote == prio_remote:
            return 2
        else:
            return 1
    return 0


def get_source_type(url):
    for pattern in PREFERRED_PATTERNS:
        if re.search(pattern, url):
            if pattern == GITHUB_PATTERN:
                return SOURCE_GITHUB
            if pattern == BITBUCKET_PATTERN:
                return SOURCE_BITBUCKET
    return


def get_username(url):
    source = get_source_type(url)

    if source == SOURCE_GITHUB:
        match = re.match(GITHUB_PATTERN, url)
        return match.groupdict()['name']
    else:
        match = re.match(BITBUCKET_PATTERN, url)
        return match.groupdict()['name']
