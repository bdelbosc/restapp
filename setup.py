#!/usr/bin/env python
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2011 Nuxeo SA <http://nuxeo.com/>"
__version__ = '0.1.0'
"""restapp package setup"""
from setuptools import setup, find_packages


setup(
    name="restapp",
    version=__version__,
    description="Nuxeo Cloud Controller",
    long_description=''.join(open('README.txt').readlines()),
    author_email="bdelbosc@nuxeo.com",
    packages=find_packages(),
    # setuptools specific keywords
    install_requires=['iso8601',
                      'simplejson',
                      'sqlalchemy == 0.7.3',
                      'Flask_SQLAlchemy == 0.15',
                      'Flask == 0.8'],
    zip_safe=False,
    package_data={'restapp': ['restapp.conf', ]},
    test_suite='nose.collector'
)
