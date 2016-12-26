"""Entry point for the application"""
import time
import click
import github
import git
import os
import getpass
import github_token

from gitorg import config

DEFAULT_GITHUB_BASE_URL = "https://api.github.com"
APP_DIR = click.get_app_dir("gitorg")
CONFIG_FILE = os.path.join(APP_DIR, 'config.json')


def load_config():
    """Returns a config object loaded from disk or an empty dict"""
    try:
        return config.Config.load(CONFIG_FILE)
    except IOError:
        if not os.path.isdir(APP_DIR):
            os.mkdir(APP_DIR)
        return initial_config()


def _clone_repo(repo, target_path, use_ssh):
    """Clones a github repo locally

    :param repo: github repo to clone as returned from the github api
    :param target_path: path to clone the repo to (full path)
    :param use_ssh: whether to use ssh protocol instead of http
    """

    if repo.fork:  # Fork will be cloned from source and add fork remote
        source = repo.source
        url = source.ssh_url if use_ssh else source.git_url
        r = git.Repo.clone_from(url, target_path)
        fork_url = repo.ssh_url if use_ssh else repo.git_url
        r.create_remote('fork', fork_url)
    else:
        url = repo.ssh_url if use_ssh else repo.git_url
        git.Repo.clone_from(url, target_path)


def initial_config():
    """Asks the user for the general configuration for the app"""
    click.echo("Configuring {}".format(CONFIG_FILE))
    conf = config.Config()
    conf["metadata"] = dict(config_time=time.time())
    user = click.prompt("What is your username? ")
    password = getpass.getpass()
    token_factory = github_token.TokenFactory(user, password, "gitorg",
                                              ["read:org", "repo", "user:email"])
    token = token_factory(tfa_token_callback=lambda: click.prompt("Insert your TFA token: "))
    conf["token"] = token

    github_url = click.prompt("What is your github instance API url? ",
                              default=DEFAULT_GITHUB_BASE_URL)
    conf["github_base_url"] = github_url

    commands = ["clone", "pull", "status"]
    use_ssh = click.confirm("Do you want have ssh keys set up? ")
    forks = click.confirm("Do you want to include forks? ")
    for c in commands:
        conf[c] = dict(forks=forks, use_ssh=use_ssh)

    conf.save(CONFIG_FILE)
    click.echo("Config saved in: '{}'".format(CONFIG_FILE))
    return conf


@click.group()
@click.option("--token", help="GitHub API token to use", envvar="GITHUB_TOKEN")
@click.option("--user", help="GitHub user to use", envvar="GITHUB_USER")
@click.option("--github_base_url", help="GitHub base api url",
              envvar="GITHUB_API_URL", default=DEFAULT_GITHUB_BASE_URL)
@click.pass_context
def gitorg(ctx, token, user, github_base_url):
    """Utility to work in a "git fashion" with github organizations.
    Allows to clone and keep in sync a local folder with a github organization
    or user"""
    if token:
        gh = github.Github(token, base_url=github_base_url)
    elif user:
        password = click.prompt("GitHub password: ", hide_input=True)
        gh = github.Github(user, password, base_url=github_base_url)
    else:
        raise click.UsageError("Provide either user or token")
    ctx.obj['github'] = gh


@gitorg.command()
def configure():
    """Runs the main configuration arguments for the tool"""
    initial_config()


@gitorg.command()
@click.argument("organization", required=True)
@click.argument("target", required=False)
@click.option("--use_ssh/--use_http", is_flag=True, envvar="GITORG_USE_SSH",
              help="Protocol to use to clone")
@click.option("--forks", is_flag=True, envvar="GITORG_FORKS",
              help="Clone forks as well")
@click.pass_context
def clone(ctx, organization, target, use_ssh, forks):
    """Clones an organization locally by cloning all repos into a folder"""
    target = target or organization
    if os.path.isdir(target) or os.path.isdir(target.lower()):
        raise click.UsageError("A folder with name {} already exists locally"
                               .format(target))

    gh = ctx.obj['github']
    try:
        org = gh.get_organization(organization)
        click.echo("<-- {}".format(organization))
    except github.GithubException:
        org = gh.get_user(organization)
        click.echo("<-- {}".format(organization))

    # Create folder and clone all repos
    os.mkdir(target)
    repos = [repo for repo in org.get_repos() if not repo.fork or forks]
    with click.progressbar(repos) as pbar:
        for repo in pbar:
            _clone_repo(repo, os.path.join(target, repo.name), use_ssh)


@gitorg.command()
@click.argument("organization", required=False)
@click.option("--use_ssh/--use_http", is_flag=True, envvar="GITORG_USE_SSH",
              help="Protocol to use to clone")
@click.option("--forks", is_flag=True, envvar="GITORG_FORKS",
              help="Clone missing forks as well")
@click.pass_context
def pull(ctx, organization, use_ssh, forks):
    """Bring all repos in the github org that are missing locally"""
    gh = ctx.obj['github']

    working_dir = os.getcwd()
    organization = organization or os.path.basename(working_dir)

    try:
        org = gh.get_organization(organization)
    except github.GithubException:
        try:
            org = gh.get_user(organization)
        except github.GithubException:
            raise click.UsageError("{} does not exist in github"
                                   .format(organization))
    local_repos = {name for name in os.listdir(working_dir) if os.path.isdir(name)}
    gh_repos = {repo for repo in org.get_repos() if not repo.fork or forks}

    missing_local = [repo for repo in gh_repos if repo.name not in local_repos]

    for repo in sorted(missing_local):
        _clone_repo(repo, os.path.join(working_dir, repo.name), use_ssh)


@gitorg.command()
@click.argument("organization", required=False)
@click.option("--forks", is_flag=True, envvar="GITORG_FORKS",
              help="Look for forks as well")
@click.pass_context
def status(ctx, organization, forks):
    """Checks if the current folder is in sync with a github org/user

    By default, the name of the org to compare to is the same as the folder name

    Looks for:
     - Repos in github not cloned locally
     - Repos locally but not in github
    """
    gh = ctx.obj['github']

    working_dir = os.getcwd()
    organization = organization or os.path.basename(working_dir)

    try:
        org = gh.get_organization(organization)
    except github.GithubException:
        try:
            org = gh.get_user(organization)
        except github.GithubException:
            raise click.UsageError("{} does not exist in github"
                                   .format(organization))
    local_repos = {name for name in os.listdir(working_dir) if os.path.isdir(name)}
    gh_repos = {repo.name for repo in org.get_repos() if not repo.fork or forks}

    missing_gh = [repo for repo in local_repos if repo not in gh_repos]
    missing_local = [repo for repo in gh_repos if repo not in local_repos]

    for repo in sorted(missing_gh + missing_local):
        if repo in missing_gh:
            click.echo("? {}".format(repo))
        elif repo in missing_local:
            click.echo("D {}".format(repo))


