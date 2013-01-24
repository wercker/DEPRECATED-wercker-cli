# from werckercli.base import do_login
# from werckercli.paths import find_folder_containing_folder_name
import os
import tempfile
import shutil


from werckercli.tests import (
    DataSetTestCase,
    TestCase
)

# from utils import (
    # open_repo,
    # tear_down_repo,
    # duplicate_repo_folder,
    # remove_repo_folder
# )

from werckercli.paths import (
    find_git_root,
    get_global_wercker_path,
    WERCKER_FOLDER_NAME
)


class GitFindRepoTest(DataSetTestCase):
    repo_name = 'empty'

    def test_find_git_root_in_same_folder(self):
        result = find_git_root(self.folder, self.get_git_folder())
        self.assertFalse(result is None)

    def test_find_git_root_from_subfolder(self):
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


class WerckerSettingsPathTest(TestCase):

    def setUp(self):
        super(WerckerSettingsPathTest, self).setUp()

        self.folder = tempfile.mkdtemp()
        os.environ['HOME'] = self.folder

    def tearDown(self):
        super(WerckerSettingsPathTest, self).tearDown()
        shutil.rmtree(self.folder)

    def test_environment_variable(self):

        result = get_global_wercker_path()

        self.assertFalse(result is None)
        self.assertTrue(result.startswith(self.folder))
        self.assertTrue(result.endswith(WERCKER_FOLDER_NAME))
        # result = find_git_root(self.folder, self.get_git_folder())
        # self.assertFalse(result is None)
