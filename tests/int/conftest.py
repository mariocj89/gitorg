import tempfile
import contextlib
import os

import pytest

from gitorg import git
from gitorg.cli import run


@contextlib.contextmanager
def temp_cd():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with cd(tmpdirname):
            yield tmpdirname


@contextlib.contextmanager
def cd(dirname):
    curdir = os.getcwd()
    os.chdir(dirname)
    try:
        yield
    finally:
        os.chdir(curdir)


@pytest.fixture
def temp_dir():
        with temp_cd():
            yield


@pytest.fixture
def temp_repo():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with cd(tmpdirname):
            with open("a", "w") as fp:
                fp.write("A")
            with open("b", "w") as fp:
                fp.write("B")
            git.run("init")
            git.run("add", "*")
            git.run("commit", "-am", "commit text")
        yield tmpdirname


@pytest.fixture
def init(temp_dir):
    run(["init"])
