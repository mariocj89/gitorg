import gitorg
from click.testing import CliRunner
import mock
import github


def test_gitorg_help():
    runner = CliRunner()
    result = runner.invoke(gitorg.gitorg, ['--help'], obj={})
    assert result.exit_code == 0


def test_gitorg_without_auth():
    runner = CliRunner()
    result = runner.invoke(gitorg.gitorg, ['clone'], obj={})
    assert result.exit_code == 2


@mock.patch("gitorg.github.Github")
def test_gitorg_with_token_as_argument(gh):
    runner = CliRunner()
    runner.invoke(gitorg.gitorg, ['--token=1234', 'clone'], obj={})
    args, kwargs = gh.call_args
    assert '1234' == args[0]


@mock.patch("gitorg.github.Github")
def test_gitorg_with_custom_base_url(gh):
    runner = CliRunner()
    runner.invoke(gitorg.gitorg, ['--github_base_url=url', '--token=1234',
                                  'clone'], obj={})
    args, kwargs = gh.call_args
    assert '1234' == args[0]
    assert kwargs['base_url'] == 'url'


@mock.patch("gitorg.github.Github")
def test_gitorg_with_token_as_env_variable(gh):
    runner = CliRunner()
    runner.invoke(gitorg.gitorg, ['clone'], obj={},
                  env={'GITHUB_TOKEN': '1234'})
    args, kwargs = gh.call_args
    assert '1234' == args[0]


@mock.patch("click.prompt")
@mock.patch("gitorg.github.Github")
def test_gitorg_with_username(gh, prompt):
    runner = CliRunner()
    prompt.return_value = 'this_is_real_password'
    runner.invoke(gitorg.gitorg, ['clone'], obj={},
                  env={'GITHUB_USER': 'mariocj89'})
    args, kwargs = gh.call_args
    assert 'mariocj89' == args[0]
    assert 'this_is_real_password' == args[1]


def test_clone_requires_org():
    runner = CliRunner()
    result = runner.invoke(gitorg.clone, [], obj={})
    assert result.exit_code == 2
    assert "organization" in result.output


@mock.patch('gitorg.os.path')
@mock.patch("gitorg.github.Github")
def test_clone_already_cloned(_, path):
    runner = CliRunner()
    path.isdir.return_value = True
    runner.invoke(gitorg.gitorg, ['clone', 'iDontExist'], obj={},
                  env={'GITHUB_TOKEN': '1234'})
    path.isdir.assert_called_with('iDontExist')


@mock.patch('gitorg.os.path')
@mock.patch("gitorg.github.Github")
def test_clone_already_cloned_lowercase(_, path):
    runner = CliRunner()
    path.isdir.side_effect = [False, True]
    runner.invoke(gitorg.gitorg, ['clone', 'iDontExist'], obj={},
                  env={'GITHUB_TOKEN': '1234'})
    path.isdir.assert_any_call('idontexist')


@mock.patch('gitorg.os')
@mock.patch("gitorg.github.Github")
def test_clone_org_without_repos(gh, os_mock):
    runner = CliRunner()
    os_mock.path.isdir.return_value = False
    gh.return_value.get_organization.return_value.get_repos.return_value = []
    result = runner.invoke(gitorg.gitorg, ['clone', 'my_user'], obj={},
                           env={'GITHUB_TOKEN': '1234'})

    assert result.exit_code == 0
    os_mock.mkdir.assert_called_once_with('my_user')
    gh.return_value.get_organization.assert_called_once_with('my_user')


@mock.patch('gitorg.os')
@mock.patch("gitorg.github.Github")
def test_clone_user_without_repos(gh, os_mock):
    runner = CliRunner()
    gh.return_value.get_user.return_value.get_repos.return_value = []
    os_mock.path.isdir.return_value = False
    gh.return_value.get_organization.side_effect = github.GithubException(1, 1)
    result = runner.invoke(gitorg.gitorg, ['clone', 'my_user'], obj={},
                           env={'GITHUB_TOKEN': '1234'})

    assert result.exit_code == 0
    os_mock.mkdir.assert_called_once_with('my_user')
    gh.return_value.get_user.assert_called_once_with('my_user')


@mock.patch('gitorg.git.Repo.clone_from')
@mock.patch('gitorg.os')
@mock.patch("gitorg.github.Github")
def test_clone_org_repos_are_not_cloned_by_default(gh, os_mock, clone_mock):
    runner = CliRunner()
    os_mock.path.isdir.return_value = False
    fork_repo = mock.Mock(fork=True)
    get_repos_mock = gh.return_value.get_organization.return_value.get_repos
    get_repos_mock.return_value = [fork_repo]
    result = runner.invoke(gitorg.gitorg, ['clone', 'my_user'], obj={},
                           env={'GITHUB_TOKEN': '1234'})

    assert result.exit_code == 0
    clone_mock.assert_not_called()


@mock.patch('gitorg.git.Repo.clone_from')
@mock.patch('gitorg.os.path.isdir')
@mock.patch('gitorg.os.mkdir')
@mock.patch("gitorg.github.Github")
def test_clone_org_with_fork_flag(gh, _, isdir_mock, clone_mock):
    runner = CliRunner()
    isdir_mock.return_value = False
    fork_repo = mock.Mock(fork=True, git_url='fork_url')
    fork_repo.source = mock.Mock(git_url='fake_url')
    fork_repo.name = 'repofake'
    fork_repo.source.name = 'repofake'
    get_repos_mock = gh.return_value.get_organization.return_value.get_repos
    get_repos_mock.return_value = [fork_repo]
    result = runner.invoke(gitorg.gitorg, ['clone', 'my_user', '--clone_forks'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})

    assert result.exit_code == 0
    clone_mock.assert_called_once_with('fake_url', "my_user/repofake")
    clone_mock.return_value.create_remote.assert_called_once_with(
        'fork', "fork_url"
    )


@mock.patch('gitorg.git.Repo.clone_from')
@mock.patch('gitorg.os.path.isdir')
@mock.patch('gitorg.os.mkdir')
@mock.patch("gitorg.github.Github")
def test_clone_org_with_two_repos(gh, _, isdir_mock, clone_mock):
    runner = CliRunner()
    isdir_mock.return_value = False
    repo1 = mock.Mock(fork=False, git_url='repo_url')
    repo1.name = 'gitorg'
    repo2 = mock.Mock(fork=False, git_url='repo_url2')
    repo2.name = 'hubsync'
    get_repos_mock = gh.return_value.get_organization.return_value.get_repos
    get_repos_mock.return_value = [repo1, repo2]
    result = runner.invoke(gitorg.gitorg, ['clone', 'my_user'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})

    assert result.exit_code == 0
    clone_mock.assert_any_call('repo_url', "my_user/gitorg")
    clone_mock.assert_any_call('repo_url2', "my_user/hubsync")


@mock.patch('gitorg.click.echo')
@mock.patch('gitorg.os.listdir')
@mock.patch('gitorg.os.path.isdir')
@mock.patch('gitorg.os.getcwd')
@mock.patch("gitorg.github.Github")
def test_status_on_sync_org(gh, wd_mock, _, listdir_mock, echo_mock):
    runner = CliRunner()
    repo1 = mock.Mock(fork=False)
    repo1.name = 'gitorg'
    repo2 = mock.Mock(fork=False)
    repo2.name = 'hubsync'
    get_repos_mock = gh.return_value.get_organization.return_value.get_repos
    get_repos_mock.return_value = [repo1, repo2]

    wd_mock.return_value = "orgname"
    listdir_mock.return_value = ["gitorg", "hubsync"]

    result = runner.invoke(gitorg.gitorg, ['status'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})

    gh.return_value.get_organization.assert_called_with("orgname")
    assert result.exit_code == 0
    assert not echo_mock.called


@mock.patch('gitorg.click.echo')
@mock.patch('gitorg.os.listdir')
@mock.patch('gitorg.os.path.isdir')
@mock.patch('gitorg.os.getcwd')
@mock.patch("gitorg.github.Github")
def test_status_added_folder(gh, wd_mock, _, listdir_mock, echo_mock):
    runner = CliRunner()
    repo1 = mock.Mock(fork=False)
    repo1.name = 'gitorg'
    repo2 = mock.Mock(fork=False)
    repo2.name = 'hubsync'
    get_repos_mock = gh.return_value.get_organization.return_value.get_repos
    get_repos_mock.return_value = [repo1, repo2]

    wd_mock.return_value = "orgname"
    listdir_mock.return_value = ["gitorg", "hubsync", "newrepo"]

    result = runner.invoke(gitorg.gitorg, ['status'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})

    gh.return_value.get_organization.assert_called_with("orgname")
    assert result.exit_code == 0
    echo_mock.assert_called_with("? newrepo")


@mock.patch('gitorg.click.echo')
@mock.patch('gitorg.os.listdir')
@mock.patch('gitorg.os.path.isdir')
@mock.patch('gitorg.os.getcwd')
@mock.patch("gitorg.github.Github")
def test_status_missing_repo(gh, wd_mock, _, listdir_mock, echo_mock):
    runner = CliRunner()
    repo1 = mock.Mock(fork=False)
    repo1.name = 'gitorg'
    repo2 = mock.Mock(fork=False)
    repo2.name = 'hubsync'
    get_repos_mock = gh.return_value.get_organization.return_value.get_repos
    get_repos_mock.return_value = [repo1, repo2]

    wd_mock.return_value = "orgname"
    listdir_mock.return_value = ["gitorg"]

    result = runner.invoke(gitorg.gitorg, ['status'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})

    gh.return_value.get_organization.assert_called_with("orgname")
    assert result.exit_code == 0
    echo_mock.assert_called_with("D hubsync")


@mock.patch('gitorg.click.echo')
@mock.patch('gitorg.os.listdir')
@mock.patch('gitorg.os.path.isdir')
@mock.patch('gitorg.os.getcwd')
@mock.patch("gitorg.github.Github")
def test_status_of_a_user(gh, wd_mock, _, listdir_mock, echo_mock):
    runner = CliRunner()
    gh.return_value.get_organization.return_value.get_repos.return_value = []
    wd_mock.return_value = "orgname"
    listdir_mock.return_value = []

    gh.return_value.get_organization.side_effect = github.GithubException(1, 1)
    result = runner.invoke(gitorg.gitorg, ['status'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})

    gh.return_value.get_user.assert_called_with("orgname")
    assert result.exit_code == 0
    assert not echo_mock.called


@mock.patch('gitorg.click.echo')
@mock.patch('gitorg.os.listdir')
@mock.patch('gitorg.os.path.isdir')
@mock.patch('gitorg.os.getcwd')
@mock.patch("gitorg.github.Github")
def test_status_of_invalid_org(gh, wd_mock, _, listdir_mock, echo_mock):
    runner = CliRunner()
    gh.return_value.get_organization.return_value.get_repos.return_value = []
    wd_mock.return_value = "orgname"
    listdir_mock.return_value = []

    gh.return_value.get_organization.side_effect = github.GithubException(1, 1)
    gh.return_value.get_user.side_effect = github.GithubException(1, 1)
    result = runner.invoke(gitorg.gitorg, ['status'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})

    assert result.exit_code == 2


@mock.patch('gitorg.click.echo')
@mock.patch("gitorg.click.prompt")
@mock.patch("gitorg.config.Config")
def test_configure_doesnt_throw(_, _2, _3):
    runner = CliRunner()
    result = runner.invoke(gitorg.gitorg, ['configure'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})
    assert result.exit_code == 0

@mock.patch('gitorg.click.echo')
@mock.patch("gitorg.click.prompt")
@mock.patch("gitorg.config.Config")
def test_first_time_configure_doesnt_throw(_, _2, config):
    runner = CliRunner()
    config.load.side_effect = IOError
    result = runner.invoke(gitorg.gitorg, ['configure'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})
    assert result.exit_code == 0


@mock.patch("gitorg._clone_repo")
@mock.patch('gitorg.os.listdir')
@mock.patch('gitorg.os.path.isdir')
@mock.patch('gitorg.os.getcwd')
@mock.patch("gitorg.github.Github")
def test_pull_missing_repo(gh, wd_mock, _, listdir_mock, clone_mock):
    runner = CliRunner()
    repo1 = mock.Mock(fork=False)
    repo1.name = 'gitorg'
    repo2 = mock.Mock(fork=False)
    repo2.name = 'hubsync'
    get_repos_mock = gh.return_value.get_organization.return_value.get_repos
    get_repos_mock.return_value = [repo1, repo2]

    wd_mock.return_value = "orgname"
    listdir_mock.return_value = ["gitorg"]

    result = runner.invoke(gitorg.gitorg, ['pull'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})

    gh.return_value.get_organization.assert_called_with("orgname")
    assert result.exit_code == 0
    clone_mock.assert_called_once_with(repo2, "orgname/hubsync", False)


@mock.patch("gitorg._clone_repo")
@mock.patch('gitorg.os.listdir')
@mock.patch('gitorg.os.path.isdir')
@mock.patch('gitorg.os.getcwd')
@mock.patch("gitorg.github.Github")
def test_status_of_a_user(gh, wd_mock, _, listdir_mock, clone_mock):
    runner = CliRunner()
    gh.return_value.get_organization.return_value.get_repos.return_value = []
    wd_mock.return_value = "orgname"
    listdir_mock.return_value = []

    gh.return_value.get_organization.side_effect = github.GithubException(1, 1)
    result = runner.invoke(gitorg.gitorg, ['pull'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})

    gh.return_value.get_user.assert_called_with("orgname")
    assert result.exit_code == 0
    assert not clone_mock.called


@mock.patch("gitorg._clone_repo")
@mock.patch('gitorg.os.listdir')
@mock.patch('gitorg.os.path.isdir')
@mock.patch('gitorg.os.getcwd')
@mock.patch("gitorg.github.Github")
def test_status_of_invalid_org(gh, wd_mock, _, listdir_mock, clone_mock):
    runner = CliRunner()
    gh.return_value.get_organization.return_value.get_repos.return_value = []
    wd_mock.return_value = "orgname"
    listdir_mock.return_value = []

    gh.return_value.get_organization.side_effect = github.GithubException(1, 1)
    gh.return_value.get_user.side_effect = github.GithubException(1, 1)
    result = runner.invoke(gitorg.gitorg, ['pull'],
                           obj={}, env={'GITHUB_TOKEN': '1234'})

    assert result.exit_code == 2
    assert not clone_mock.called

