#!/usr/bin/env python
from setuptools import setup

from wcut import __version__

setup(
    name='wcut',
    version=__version__,
    author='Kyle A. Meyer',
    author_email='meyerkya@gmail.com',
    url = 'https://github.com/kyleam/wcut',
    packages=['wcut'],
    scripts=['bin/wcut'],
    package_data={'wcut': ['VERSION']},
    license='GPLv3',
    description='Select fields by header keywords',
    long_description=open('README.rst').read(),
    install_requires=['docopt >= 0.6'],
)
