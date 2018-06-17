#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

classifiers = ['Development Status :: 3 - Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.6',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(
    name            = 'ugly',
    version         = '0.0.0',
    author          = 'A. Buxton',
    author_email    = '',
    description     = 'Unified Graphics Library Yarrr',
    long_description= open('README.md').read(),
    license         = 'GPL-3.0',
    keywords        = 'Raspberry Pi',
    url             = '',
    classifiers     = classifiers,
    py_modules      = [],
    packages        = ['ugly'],
    include_package_data = True,
    install_requires= []
)
