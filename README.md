[![PyPI version](https://badge.fury.io/py/gitorg.svg)](https://badge.fury.io/py/gitorg)
[![Build Status](https://travis-ci.org/mariocj89/gitorg.svg?branch=master)](https://travis-ci.org/mariocj89/gitorg)
[![Coverage Status](https://coveralls.io/repos/github/mariocj89/gitorg/badge.svg?branch=master)](https://coveralls.io/github/mariocj89/gitorg?branch=master)
[![Requirements Status](https://requires.io/github/mariocj89/gitorg/requirements.svg?branch=master)](https://requires.io/github/mariocj89/gitorg/requirements/?branch=master)
[![Code Health](https://landscape.io/github/mariocj89/gitorg/master/landscape.svg?style=flat)](https://landscape.io/github/mariocj89/gitorg/master)

# GitOrg
Tool to organise and synchronise your organisations locally with github

# Install
```pip install gitorg```

# Usage
`gitorg` aims to be as similar as possible to your experience with `git`.

The first time that you run gitorg it will configure the required options for you

Examples:

- Clonning an organization ```gitorg clone <org_or_user_to_clone>```
- Checking for new repos ```gitorg status```

# Common parameteres
The following are parameters that are used by all commands, you can pass them as explained in the help or set a environment variable.

|option|env var|description|
|------|-------|-----------|
|token|GITHUB_TOKEN|Github api token, [click here](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) to generate one
|user|GITHUB_USER|The user to login into github|
|github_base_url|GITHUB_API_URL|Base url of your github instance (set it only for enterprise github)|

Those parameters will be asked the first time you run `gitorg` if you want the setup wizart to prompt for the config parameters again, run `gitorg configure`
