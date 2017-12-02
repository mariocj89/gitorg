|PyPI version| |Build Status| |Coverage Status| |Code Health|

GitOrg
======

Organise your git repositories easily. GitOrg aims to be your git for repositories.

Install
=======

``pip install gitorg``

Concept
=======

GitOrg creates a *repository* of repositories locally. These repositories are composed of *expressions*
that translate to actual git repositories.

All expressions are composed of a *protocol* that helps gitorg understand how to retrieve a list of
repositories and a pattern to generate those.

Some valid expressions are:

- `web:https://github.com/mariocj89/gitorg.git`: Will clone locally gitorg repository
- `github:mariocj89`: All repositories belonging to mariocj89 user.
- `local:/home/mariocj89/ws/cpyhon`: Cpython repository from a local path

Both local and github protocols accept glob expressions. Allowing for patterns like: `github:orgname/*python*`
to express all repositories with python on its name in orgname.

Usage
=======

::

  usage: gitorg [-h] {init,add,status} ...

  CLI tool to interact with list of repositories

  optional arguments:
    -h, --help         show this help message and exit

  Commands:
    Commands used in various situations:

    {init,add,status}
      init             Initializes a folder to work with gitorg
      add              Adds a list to the current gitorg workspace
      status           Show the workspace status

A sample way to clone all repositories in user mariocj89 and organization python:

::

  gitorg init
  gitorg add github:mariocj89
  gitorg add github:python



.. _click here: https://help.github.com/articles/creating-an-access-token-for-command-line-use/

.. |PyPI version| image:: https://badge.fury.io/py/gitorg.svg
   :target: https://badge.fury.io/py/gitorg
.. |Build Status| image:: https://travis-ci.org/mariocj89/gitorg.svg?branch=master
   :target: https://travis-ci.org/mariocj89/gitorg
.. |Coverage Status| image:: https://coveralls.io/repos/github/mariocj89/gitorg/badge.svg?branch=master
   :target: https://coveralls.io/github/mariocj89/gitorg?branch=master
.. |Code Health| image:: https://landscape.io/github/mariocj89/gitorg/master/landscape.svg?style=flat
   :target: https://landscape.io/github/mariocj89/gitorg/master

