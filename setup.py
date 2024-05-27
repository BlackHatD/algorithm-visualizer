# -*- coding:utf-8 -*-
# builtins
import os
import codecs
from setuptools import setup, find_packages

PACKAGE_NAME = 'visualizer'
LICENSE      = 'MIT'
VERSION      = '1.0.1'
URL          = 'https://github.com/BlackHatD/algorithm-visualizer'
AUTHOR       = 'Daichi'
AUTHOR_EMAIL = 'blackhatd0710@gmail.com'
DESCRIPTION  = 'Algorithm Visualizer'

CLASSIFIERS  = [
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development',
]


## read README.md
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = '\n' + fh.read()

setup(
    name=PACKAGE_NAME
    , version=VERSION
    , author=AUTHOR
    , author_email=AUTHOR_EMAIL
    , url=URL
    , license=LICENSE
    , packages=find_packages()
    , package_data={'': ['LICENSE']}
    , description=DESCRIPTION
    , long_description_content_type='text/markdown'
    , long_description=long_description
    , classifiers=CLASSIFIERS
)
