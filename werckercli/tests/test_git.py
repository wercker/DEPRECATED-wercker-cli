
# from werckercli.base import do_login
# from werckercli.paths import find_folder_containing_folder_name
import os

from werckercli.tests import (
    DataSetTestCase
)

# from utils import (
    # open_repo,
    # tear_down_repo,
    # duplicate_repo_folder,
    # remove_repo_folder
# )

from werckercli.paths import (
    find_git_root
)


class GitFindRepoTest(DataSetTestCase):
    repo_name = 'empty'

    def test_current_root(self):
        result = find_git_root(self.folder, self.get_git_folder())
        self.assertFalse(result is None)

    def test_from_subfolder(self):
        # self.assertTrue(False)
        new_folder = os.path.join(
            self.folder,
            "multiple",
            "subfolders",
            "and",
            "it",
            "still"
        )

        result = find_git_root(new_folder, self.get_git_folder())

        self.assertFalse(result is None)
