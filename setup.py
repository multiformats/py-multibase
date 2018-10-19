#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'python-baseconv==1.2.0',
    'six==1.10.0',
    'morphys==1.0',
]

setup_requirements = [
    'pytest-runner',
    # TODO(dhruvbaldawa): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='py-multibase',
    version='1.0.0',
    description="Multibase implementation for Python",
    long_description=readme + '\n\n' + history,
    author="Dhruv Baldawa",
    author_email='dhruv@dhruvb.com',
    url='https://github.com/multiformats/py-multibase',
    packages=find_packages(include=['multibase']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='multibase',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
