"""Validates functionality of init command"""
import os

from gitorg.cli import run
from gitorg.file import File


def test_sanity(init, temp_repo):
    """Calling add raises no exception"""
    run(["add", f"local:{temp_repo}"])


def test_creates_new_folder(init, temp_repo):
    """Calling add creates a new folder"""
    num_files = len(os.listdir(os.getcwd()))
    run(["add", f"local:{temp_repo}"])
    assert len(os.listdir(os.getcwd())) == (num_files + 1)


def test_without_clone_dont_create_new_folder(init, temp_repo):
    """Calling add creates a new folder"""
    num_files = len(os.listdir(os.getcwd()))
    run(["add", f"local:{temp_repo}", "--no-clone"])
    assert len(os.listdir(os.getcwd())) == num_files


def test_content_of_gitorg_file(init, temp_repo):
    """Calling creates a file with specific content"""
    run(["add", f"local:{temp_repo}", "--no-clone"])
    with open(File.DEFAULT_FILENAME) as fp:
        content = fp.read()

    assert f"""lists:
- local:{temp_repo}
""" == content


def test_add_http(init):
    """Calling creates a file with specific content"""
    run(["add", "web:https://github.com/mariocj89/gitorg.git"])
    with open(File.DEFAULT_FILENAME) as fp:
        content = fp.read()

    assert """lists:
- web:https://github.com/mariocj89/gitorg.git
""" == content
