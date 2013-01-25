#!/usr/bin/env python
# Setup file for wercker-bruticus
# Copyright (C) 20013 Wercker <pleasemailus@wercker.com>

try:
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False
from distutils.core import Distribution

werckercli_version_string = '0.0.1'

tests_require = ['httpretty', ]
setup_kwargs = {}

if has_setuptools:
    setup_kwargs['test_suite'] = 'werckercli.tests.test_suite'
    setup_kwargs['test_suite'] = 'werckercli.tests.test_suite'

# print has_setuptools
setup(name='wercker-bruticus',
      description='wercker command line interface',
      keywords='cli, command line',
      version=werckercli_version_string,
      url='http://beta.wercker.com/',
      # download_url='',
      license='MIT license',
      author='jacco @ wercker',
      author_email='jacco@wercker.com',
      long_description="""
      Simple command line interface for the wercker website.
      """,
      packages=['werckercli', 'werckercli.tests'],
      scripts=['bin/wercker', ],
      tests_require=tests_require,
      extras_require={'test': tests_require},
      distclass=Distribution,
      **setup_kwargs
      )
