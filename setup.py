#!/usr/bin/env python
from setuptools import setup
LONG_DESCRIPTION="Git helper to handle organizations"

try:
    # attempt to build a long description from README.md
    # run sudo apt-get install pandoc and pip install pypandoc first
    import pypandoc
    LONG_DESCRIPTION=pypandoc.convert('README.md', 'rst')
except (ImportError, RuntimeError, OSError):
    pass


setup(
    name='gitorg',
    packages=['gitorg'],
    version='0.1.1',
    description='Use git for organizations!',
    long_description=LONG_DESCRIPTION,
    author='Mario Corchero',
    author_email='mariocj89@gmail.com',
    url='https://github.com/Mariocj89/gitorg',
    keywords=['github', 'sync', 'workspace'],
    test_suite='nose.collector',
    use_2to3=True,
    install_requires=['six', 'PyGithub', 'GitPython'],
    entry_points={
        'console_scripts': [
            'gitorg=gitorg.__main__:main'
        ]
    }
)
