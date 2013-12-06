#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from fabric.api import local

from fabric.contrib.console import confirm


def publish():
    """Publishes the package to PyPI without too much thought involved."""
    if confirm("Are you absolutely sure that you're ready to publish this package to PyPI?") and \
            confirm("I don't believe you. Are you really that certain that we should publish this package version "
                    "to PyPI?"):
        local("python setup.py sdist bdist_egg upload")
