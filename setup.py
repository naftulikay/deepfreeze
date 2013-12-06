#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "deepfreeze",
    version = "0.1.1",
    packages = find_packages('src'),
    package_dir = { '': 'src'},
    install_requires = ['setuptools',
        'boto >= 2.19.0, < 3.0.0',
    ],
    entry_points = {
        'console_scripts': [
            'deepfreeze = deepfreeze:cli',
        ]
    },
)
