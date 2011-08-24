#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from os.path import exists
from setuptools import setup, find_packages

from aero.version import __version__

read_file = lambda filename: exists(filename) and open(filename).read() or ''

setup(
    name = 'aero',
    version = '.'.join([str(item) for item in __version__]) + 'a',
    description = "aero adds django-like apps support to tornado and automates common actions",
    long_description = read_file('README.rst'),
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
    packages = find_packages(),
    include_package_data = True,

    install_requires = ['tornado',
                        'cyrusbus==0.1.0'],

    tests_require = ['coverage',
                     'tornado-pyvows==0.3.0'],

    entry_points = {
        'console_scripts': [
            'aero = aero.console:main'
        ],
    },

)
