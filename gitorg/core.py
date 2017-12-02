"""Core functionality. All commands are defined here"""
import re
import os

from . import git
from . import file
from . import protocols

# TODO: Rename this file to commands and move the utils elsewhere


class UnknownProtocol(Exception):
    pass


_DEFAULT_PROTOCOL_MAPPING = {
    "github": protocols.Github(),
    "web": protocols.Web(),
    "local": protocols.Path(),
}

_LIST_PATTERN = re.compile(r"^(?P<protocol>github|web|local):(?P<list>.*)$")


def _expand_list(raw_list):
    res = _LIST_PATTERN.match(raw_list)
    try:
        protocol = _DEFAULT_PROTOCOL_MAPPING[res.group("protocol")]
    except (AttributeError, KeyError):
        raise UnknownProtocol(f"Unknown protocol {res.group('protocol')}")
    except TypeError:
        raise UnknownProtocol(f"Unable to parse {raw_list}")
    return list(protocol.list(res.group("list")))


def _get_repo_list(gitorg_file):
    for pattern in gitorg_file.lists:
        yield from _expand_list(pattern)


def _discover_repos(path):
    for repo_folder in os.listdir(path):
        repo_path = os.path.join(path, repo_folder)
        if git.is_repo(repo_path):
            repo_name = os.path.basename(repo_path)
            yield protocols.Repo(name=repo_name, url=repo_path)


def init():
    """Initializes a workspace"""
    gitorg_file = file.File()
    gitorg_file.sync()


def add(pattern, clone):
    gitorg_file = file.File.from_ws()
    gitorg_file.lists.append(pattern)

    if clone:
        for repo in _expand_list(pattern):
            git.run("clone", repo.url)

    gitorg_file.sync()


def status():
    gitorg_file = file.File.from_ws()
    expected_repos = [r.name for r in _get_repo_list(gitorg_file)]
    working_dir = os.getcwd()
    local_repos = [r.name for r in _discover_repos(working_dir)]

    extra_local = [repo for repo in local_repos if repo not in expected_repos]
    missing_local = [repo for repo in expected_repos if repo not in local_repos]

    for repo in extra_local:
        print(f"? {repo}")
    for repo in missing_local:
        print(f"D {repo}")

