"""Entry point for the application"""
import click
import github
import git
import os


DEFAULT_GITHUB_BASE_URL = "https://api.github.com"


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
@click.argument("organization", required=True)
@click.argument("target", required=False)
@click.option("--use_ssh/--use_http", is_flag=True, envvar="GITORG_USE_SSH",
              help="Protocol to use to clone")
@click.option("--clone_forks", is_flag=True, envvar="GITORG_CLONE_FORKS",
              help="Clone forks as well")
@click.pass_context
def clone(ctx, organization, target, use_ssh, clone_forks):
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
    repos = [repo for repo in org.get_repos() if not repo.fork or clone_forks]
    with click.progressbar(repos) as pbar:
        for repo in pbar:
            if repo.fork:  # Fork will be cloned from source and add fork remote
                source = repo.source
                url = source.ssh_url if use_ssh else source.git_url
                r = git.Repo.clone_from(url, os.path.join(target, repo.name))
                fork_url = repo.ssh_url if use_ssh else repo.git_url
                r.create_remote('fork', fork_url)
            else:
                url = repo.ssh_url if use_ssh else repo.git_url
                git.Repo.clone_from(url, os.path.join(target, repo.name))
