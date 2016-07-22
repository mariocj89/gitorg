#!/usr/bin/env python
from setuptools import setup

setup(
    name='gitorg',
    packages=['gitorg'],
    version='0.0.1',
    description='Use git for organizations!',
    author='Mario Corchero',
    author_email='mariocj89@gmail.com',
    url='https://github.com/Mariocj89/gitorg',
    keywords=['github', 'sync', 'workspace'],
    scripts=['bin/gitorg'],
    test_suite='nose.collector',
    use_2to3=True,
    install_requires=['six', 'PyGithub'],
    tests_require=['mock']
)
