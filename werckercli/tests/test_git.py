import os

from werckercli.tests import (
    DataSetTestCase,
    TestCase
)

from werckercli.git import (
    get_priority,
    get_remote_options,
)


class GetPriorityTests(TestCase):
    BITBUCKET_URL = "git@bitbucket.org:postmodern/ronin.git"
    GITHUB_URL = "git@github.com:wercker/wercker-bruticus"
    HG_SSH_URL = "ssh://hg@bitbucket.org/pypy/pypy"
    HG_HTTPS_URL = "https://bitbucket.org/pypy/pypy"

    def test_priority_two(self):

        result = get_priority(self.BITBUCKET_URL, "origin")
        self.assertEqual(result, 2)

        result = get_priority(self.GITHUB_URL, "origin")
        self.assertEqual(result, 2)

    def test_priority_one(self):
        result = get_priority(self.BITBUCKET_URL, "some_upstream")
        self.assertEqual(result, 1)

        result = get_priority(self.GITHUB_URL, "some_upstream")
        self.assertEqual(result, 1)

        result = get_priority(
            self.GITHUB_URL,
            "origin",
            prio_remote="not_origin"
        )

        self.assertEqual(result, 1)

    def test_priority_zero(self):
        result = get_priority(self.HG_SSH_URL, "origin")
        self.assertEqual(result, 0)

        result = get_priority(self.HG_HTTPS_URL, "origin")
        self.assertEqual(result, 0)


class GetRemoteOptionsTests(DataSetTestCase):
    repo_name = "multiple-remotes"

    def test_get_remotes(self):


        print self.folder
        for r, d, f in os.walk(self.folder):
            print r, d, f
        folder = os.path.join(
            self.folder,
            self.repo_name,
            self.get_git_folder()
        )
        options = get_remote_options(folder)

        self.assertEqual(len(options), 2)
