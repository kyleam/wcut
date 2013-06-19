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
    license='GPLv3',
    description='Select fields by header keywords',
    long_description=open('README.rst').read(),
    tests_require=['pytest >= 2.3'],
    install_requires=['docopt >= 0.6'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
)
