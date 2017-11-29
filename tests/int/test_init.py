"""Validates functionality of init command"""
import os

import pytest

from gitorg.cli import run
from gitorg.file import File


def test_sanity(temp_dir):
    """Calling init raises no exception"""
    run(["init"])


def test_creates_new_file(temp_dir):
    """Calling init creates a new file"""
    assert len(os.listdir(os.getcwd())) == 0
    run(["init"])
    assert len(os.listdir(os.getcwd())) == 1


def test_content_of_new_file(temp_dir):
    """Calling creates a file with specific content"""
    run(["init"])
    with open(File.DEFAULT_FILENAME) as fp:
        content = fp.read()

    assert """lists: []\n""" == content


@pytest.mark.xfail
def test_init_fails_on_existing_girorg(temp_dir):
    """Calling init raises no exception"""
    run(["init"])
    with pytest.raises(Exception):
        run(["init"])
