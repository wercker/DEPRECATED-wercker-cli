import re

from collections import namedtuple
from dulwich.repo import Repo

PREFERRED_PATTERNS = [
    '(git@)*(bitbucket.org|github.com):(.*)'
]


def get_remote_options(repo_path, prio_remote="origin"):

    # from subprocess import call
    # sts = call("ls", " -la " + repo_path, shell=True)
    # print sts
    repo = Repo(repo_path)
    conf = repo.get_config()
    options = []

    RemoteOption = namedtuple('RemoteOption', 'url remote priority')

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
    for pattern in PREFERRED_PATTERNS:
        if re.search(pattern, url):
            if remote == prio_remote:
                return 2
            else:
                return 1
    return 0
