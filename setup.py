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
    version='0.7.0',
    description='Use git for organizations!',
    long_description=LONG_DESCRIPTION,
    author='Mario Corchero',
    author_email='mariocj89@gmail.com',
    url='https://github.com/Mariocj89/gitorg',
    keywords=['github', 'sync', 'workspace'],
    license='MIT',
    test_suite='nose.collector',
    use_2to3=True,
    install_requires=['six', 'PyGithub', 'GitPython', 'github_token'],
    entry_points={
        'console_scripts': [
            'gitorg=gitorg.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Version Control',
    ],
)
