"""Version numbering setup

The version is stored in an untracked file (VERSION) in the package
directory. This file is updated after each commit with `git describe`
with the post-commit hook. Both modules and setup.py retrieve
information from here.
"""
import os

PKGDIR = os.path.dirname(__file__)
VERSION_FILE = os.path.join(PKGDIR, 'VERSION')


class VersionError(Exception):
    pass


def get_version():
    try:
        fullversion = open(VERSION_FILE).read().strip()
    except IOError:
        raise VersionError('{} does not exist. '
                           'Run post-commit to create.'.format(VERSION_FILE))
    return fullversion, fullversion.split('-')[0]
