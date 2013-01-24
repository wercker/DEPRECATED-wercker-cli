import os


def get_global_wercker_path():
    return os.path.join(os.environ['HOME'], '.wercker')


def get_global_wercker_filename():
    return os.path.join(get_global_wercker_path(), 'credentials')


def check_or_create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)

    return True


def find_git_root(path, folder_name=".git"):
	"""Find the nearest parent with <folder_name> folder, for locating the git root folder"""
	return find_folder_containing_folder_name(path, folder_name)

def find_folder_containing_folder_name(path, folder_name):
    """Find the nearest parent with a <folder_name> folder"""

    if path == os.path.curdir:
        path = os.path.realpath(path)

    if os.path.isdir(path):
        if os.path.isdir(os.path.join(path, folder_name)):
            return path
        else:
            parent = os.path.realpath(os.path.join(path, os.path.pardir))
            if parent == path:
                return None
            return getGitRoot(parent, folder_name)
