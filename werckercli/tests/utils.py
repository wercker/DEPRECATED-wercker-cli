import os
import shutil
import tempfile

from dulwich.repo import Repo


def open_repo(name):
    """Open a copy of a repo in a temporary directory."""

    temp_repo_dir = duplicate_repo_folder(name)
    return Repo(temp_repo_dir)


def tear_down_repo(repo):
    """Tear down a test repository."""

    temp_dir = os.path.dirname(repo.path.rstrip(os.sep))
    remove_repo_folder(temp_dir)


def duplicate_repo_folder(name):
    """Duplicate a repo folder"""

    temp_dir = tempfile.mkdtemp()
    repo_dir = os.path.join(
        os.path.dirname(__file__),
        'data',
        'repos',
        name
    )
    temp_repo_dir = os.path.join(temp_dir, name)
    shutil.copytree(repo_dir, temp_repo_dir, symlinks=True)

    return os.path.join(temp_dir, name)


def remove_repo_folder(temp_dir):
    """Remove a duplicated
    folder"""
    shutil.rmtree(temp_dir)
