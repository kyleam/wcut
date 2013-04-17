"""Inject information about program that produced files

Some-data.txt looks like this::

    id1 feature1 meas1
    id2 feature2 meas2

Instead, make it look like this::

    # 2012-10-01
    # some-program.py --some-flag some-input-file
    # ce19976
    id1 feature1 meas1
    id2 feature2 meas2
"""

import os
import sys
import subprocess
import datetime


def add_sourceline(func, comment_char='#', source=None):
    """Add source information when open a file for writing

    Decorate ``open``:
    >>> sopen = add_sourceline(open)

    And then use as usual:
    >>> with sopen('open-info.txt', 'w') as tf:
    ...     tf.write('data line\n')
    """
    if not source:
        source = _git_commit() or ''
    infos = (_call(), _date(), source)

    lines = [' '.join([comment_char, info])
             for info in infos if info]

    sourceline = '\n'.join(lines) + '\n'

    def wrap(*args, **kwargs):
        fh = func(*args, **kwargs)
        if len(args) == 2 and args[1] == 'w':
            fh.write(sourceline)
        return fh
    return wrap


def _git_commit():
    srcfile = os.path.realpath(sys.argv[0])
    srcdir = os.path.dirname(srcfile)
    gitcmd = "cd {} && git log -n1 --oneline | cut -d' ' -f1".format(
        srcdir)
    commit, err = subprocess.Popen(gitcmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE).communicate()
    if err:
        return False
    return commit.rstrip().decode('utf-8')


def _date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


def _call():
    return ' '.join(sys.argv)

sopen = add_sourceline(open)
