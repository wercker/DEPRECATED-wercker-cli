import os

from werckercli.tests import (
    DataSetTestCase,
    TempHomeSettingsCase,
)

from werckercli.paths import (
    find_git_root,
    get_global_wercker_path,
    WERCKER_FOLDER_NAME,
    WERCKER_CREDENTIALS_FILE,
    get_global_wercker_filename,
    check_or_create_path
)


class GitFindRepoTests(DataSetTestCase):
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

    def test_find_git_root_from_curdir(self):
        current_dir = os.getcwd()

        os.chdir(self.get_home_folder())
        os.mkdir('.git')
        result = find_git_root(os.curdir)

        self.assertTrue(result)

        os.chdir(current_dir)


class WerckerSettingsPathTests(TempHomeSettingsCase):

    def test_get_global_wercker_path(self):

        result = get_global_wercker_path()

        self.assertFalse(result is None)
        self.assertTrue(result.startswith(self.get_home_folder()))
        self.assertTrue(result.endswith(WERCKER_FOLDER_NAME))


class WerckerGlobalFilenameTests(TempHomeSettingsCase):

    def test_get_global_filename(self):

        result = get_global_wercker_filename()

        self.assertTrue(result.endswith(WERCKER_CREDENTIALS_FILE))


class WerckerGetOrCreateTests(TempHomeSettingsCase):

    def test_create(self):

        result = check_or_create_path(
            os.path.join(
                self.get_home_folder(),
                'test-folder'
            )
        )

        self.assertTrue(result)

    def test_create_multiple_levels(self):

        result = check_or_create_path(
            os.path.join(
                self.get_home_folder(),
                'test-folder',
                'subfolder'
            )
        )

        self.assertTrue(result)
