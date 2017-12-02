"""Available protocols the project can handle"""
import enum
import fnmatch
import re
import os

import github


class URIException(Exception):
    pass


class Repo:
    def __init__(self, name, url):
        self.name = name
        self.url = url


class Base:
    """Base protocol"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, pattern):
        raise NotImplementedError()


class Web(Base):
    """No special logic, can be fed directly to git"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, pattern):
        name = os.path.basename(pattern.rstrip("/")).rstrip(".git")  # TODO: meh
        return [Repo(name=name, url=pattern)]


class Path(Base):
    """No special logic, can be fed directly to git"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, pattern):
        name = os.path.basename(pattern.rstrip("/"))
        return [Repo(name=name, url=pattern)]


class Github(Base):
    _EXTRACT_PATTERN = re.compile(r"^(?P<org>(\w(-\w)?)+)(/(?P<repo>.+))?$")
    _DEFAULT_BASE_URL = "https://api.github.com"

    class CloneProtocol(enum.Enum):
        ssh = "ssh"
        https = "https"

    def __init__(self, *, api_url=_DEFAULT_BASE_URL, clone_protocol="ssh", **kwargs):
        super().__init__(**kwargs)
        self._clone_protocol = self.CloneProtocol(clone_protocol)
        self._gh = github.Github(
            login_or_token=os.environ.get("GITHUB_TOKEN"),
            base_url=api_url
        )

    def list(self, pattern):
        res = self._EXTRACT_PATTERN.match(pattern)
        if not res:
            raise URIException(f"Unable to match {pattern},"
                               " please use 'organization[/repo_pattern]'")
        org_name = res.group("org")
        repo_matcher = res.group("repo") or "*"

        try:
            repos = self._gh.get_organization(org_name).get_repos()
        except github.GithubException:
            repos = self._gh.get_user(org_name).get_repos()

        for repo in repos:
            if not fnmatch.fnmatch(repo.name, repo_matcher):
                continue
            if self._clone_protocol == self.CloneProtocol.ssh:
                yield Repo(name=repo.name, url=repo.ssh_url)
            elif self._clone_protocol == self.CloneProtocol.https:
                yield Repo(name=repo.name, url=repo.clone_url)
            else:
                raise RuntimeError(f"Invalid protocol selected: {self._clone_protocol}")
