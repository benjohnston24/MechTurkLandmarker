#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

# Imports
from setuptools import setup, find_packages
from turkmarker.__init__ import __version__ as ver

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = '09-Jun-2017 15:51:52 AEST'
__license__ = 'BSD 3-Clause'

setup(
    name='turkmarker',
    description='Image landmarking system for Amazon Mechanical Turk',
    url='https://github.com/benjohnston24/turkmarker',
    author='Ben Johnston',
    author_email='bjohnston24@gmail.com',
    version=ver,
    packages=find_packages(exclude=[
        'tests', 'docs', 'contrib',
    ]),
    package_data = {
        'turkmarker': ['data/*',
                       'data/static/*'],
    },
    entry_points = {
        'console_scripts': [
            'turk-admin = turkmarker.manage:_main',
        ]
    },
    install_requires = [
        'boto3',
        'numpy',
        'pillow',
        'xmltodict',
    ],
    license='BSD 3-Clause',
    long_description='https://github.com/benjohnston24/turkmarker',
    keywords='image, landmarking, Mechanical Turk',
    classifiers = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
    ]
)
