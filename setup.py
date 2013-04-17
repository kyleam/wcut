#!/usr/bin/env python
import os
from distutils.core import setup

import wcut

setup(
    name='wcut',
    version=wcut.__version__,
    author='Kyle A. Meyer',
    author_email='meyerkya@gmail.com',
    url = 'https://gitorious.org/wcut',
    packages=['wcut', 'wcut.deps'],
    scripts=['bin/wcut'],
    package_data={'wcut': ['VERSION']},
    license='GPLv3',
    description='Select fields by header keywords',
    long_description=open('README.rst').read(),
)
