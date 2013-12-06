#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="deepfreeze",
    description="A simple command-line utility to upload files to Amazon Glacier.",
    version="0.1.1",
    author="Naftuli Tzvi Kay",
    author_email="rfkrocktk@gmail.com",
    url="https://github.com/rfkrocktk/deepfreeze",
    download_url="https://github.com/rfkrocktk/deepfreeze/releases",
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Systems Administration',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'setuptools',
        'boto >= 2.19.0, < 3.0.0',
    ],
    entry_points={
        'console_scripts': [
            'deepfreeze = deepfreeze:cli',
        ]
    },
)
