"""Version numbering setup

The version is stored in an untracked file (VERSION) in the package
directory. This file is updated after each commit with `git describe`
with the post-commit hook. Both modules and setup.py retrieve
information from here.
"""
import os
import subprocess

PKGDIR = os.path.dirname(__file__)
VERSION_FILE = os.path.join(PKGDIR, 'VERSION')


class VersionError(Exception):
    pass


def get_version():
    if not os.path.exists(VERSION_FILE):
        rootdir = os.path.dirname(PKGDIR)
        subprocess.call(['bash', os.path.join(rootdir, 'post-commit')])
    try:
        fullversion = open(VERSION_FILE).read().strip()
    except IOError:
        raise VersionError(
            '{} cannot be found or generated'.format(VERSION_FILE))
    return fullversion, fullversion.split('-')[0]
