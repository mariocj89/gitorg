#!/usr/bin/env python
import os
from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='gitorg',
    packages=['gitorg'],
    version='0.8.0',
    description='Use git for organizations!',
    long_description=readme(),
    author='Mario Corchero',
    author_email='mariocj89@gmail.com',
    url='https://github.com/Mariocj89/gitorg',
    keywords=['github', 'sync', 'workspace'],
    license='MIT',
    test_suite='nose.collector',
    use_2to3=True,
    install_requires=['PyGithub', 'PyYAML'],
    entry_points={
        'console_scripts': [
            'gitorg=gitorg.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Version Control',
    ],
)
