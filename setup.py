#!/usr/bin/env python


from __future__ import with_statement

import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


NAME = 'devutils'


def get_long_description(filename):
    readme = os.path.join(os.path.dirname(__file__), filename)
    with open(readme) as fp:
        return fp.read()

def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as fp:
        return fp.read()

def load_version():
    '''Loads a file content'''
    filename = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "devutils", "__init__.py"))
    with open(filename, "rt") as version_file:
        conan_init = version_file.read()
        version = re.search("__version__ = '([0-9a-z.-]+)'", conan_init).group(1)
        return version
setup(
    name=NAME,
    version=load_version(),
    description='Utils to maniplute your local programs.',
    long_description=read_file('README.md'),
    keywords='devOps',
    author='Mingyi Zhang',
    author_email='mingyi.z@outlook.com',
    maintainer='Mingyi Zhang',
    url='https://github.com/mingyiz/devutils',
    license='LGPL 2.1',
    packages=[NAME,
	    'devutils/conan',
	    'devutils/conan/hacks'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)

