"""Validates functionality of init command"""
import os
import shutil
import pytest

from gitorg.cli import run


@pytest.fixture
def add_local(temp_repo):
    """Fixture to add the repo to the current workspace"""
    def _(clone):
        commands = ["add", f"local:{temp_repo}"]
        if not clone:
            commands.append("--no-clone")
        run(commands)
        return temp_repo
    yield _  # No return, preserve the other fixture


def test_sanity(init, add_local):
    """Calling add raises no exception"""
    add_local(clone=True)
    run(["status"])


def test_status_on_cloned_is_empty(init, add_local, capfd):
    add_local(clone=True)
    run(["status"])
    out, err = capfd.readouterr()
    assert not err
    assert not out


def test_status_on_not_cloned_report_deleted(init, add_local, capfd):
    added_repo_path = add_local(clone=False)
    run(["status"])
    out, err = capfd.readouterr()
    assert not err
    assert out == "D " + os.path.split(added_repo_path)[-1] + "\n"


def test_status_on_local_missing_repo_reports_missing(init, temp_repo, capfd):
    temp_repo_name = os.path.split(temp_repo)[-1]
    try:
        shutil.move(temp_repo, ".")
        run(["status"])
        out, err = capfd.readouterr()
        assert not err
        assert out == f"? {temp_repo_name}\n"
    finally:
        shutil.move(temp_repo_name, temp_repo)


def test_status_on_missing_and_new_repo(init, add_local, capfd):
    temp_repo = add_local(clone=True)
    temp_repo_name = os.path.split(temp_repo)[-1]
    try:
        shutil.move(temp_repo_name, "new_name")
        run(["status"])
        out, err = capfd.readouterr()
        assert not err
        assert "? new_name" in out
        assert f"D {temp_repo_name}" in out
    finally:
        shutil.move("new_name", temp_repo)


def test_non_git_repos_not_reported(init, add_local, capfd):
    add_local(clone=True)
    os.mkdir("new_name")
    run(["status"])
    out, err = capfd.readouterr()
    assert not err
    assert not out

