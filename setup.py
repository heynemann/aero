#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from setuptools import setup
from aero.version import __version__

setup(
    name = 'aero',
    version = '.'.join([str(item) for item in __version__]) + 'a',
    description = "aero adds django-like apps support to tornado and automates common actions",
    long_description = open('README.rst').read(),
    keywords = 'tornado aero app django',
    author = 'Bernardo Heynemann',
    author_email = 'heynemann@gmail.com',
    #Contributors
    #contributor = 'Rafael Carício',
    #contributor_email = 'rafael@caricio.com',
    url = 'http://heynemann.github.com/aero/',
    license = 'MIT',
    classifiers = ['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: MacOS',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.6',
    ],
    packages = ['aero'],
    package_dir = {"aero": "aero"},

    install_requires = open('requirements.txt').read().split('\n'),
    tests_require = open('test_requirements.txt').read().split('\n'),

    entry_points = {
        'console_scripts': [
            'aero = aero.console:main'
        ],
    },

)


