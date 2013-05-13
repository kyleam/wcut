#!/usr/bin/env python
from distutils.core import setup

from wcut import __version__

setup(
    name='wcut',
    version=__version__,
    author='Kyle A. Meyer',
    author_email='meyerkya@gmail.com',
    url = 'https://github.com/kyleam/wcut',
    packages=['wcut', 'wcut.deps'],
    scripts=['bin/wcut'],
    package_data={'wcut': ['VERSION']},
    license='GPLv3',
    description='Select fields by header keywords',
    long_description=open('README.rst').read(),
)
