#!/usr/bin/env python
# Setup file for wercker-cli
# Copyright (C) 20013 Wercker <pleasemailus@wercker.com>

try:
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False
from distutils.core import Distribution

from werckercli import __version__
werckercli_version_string = __version__

tests_require = ['httpretty', ]
setup_kwargs = {}

if has_setuptools:
    setup_kwargs['test_suite'] = 'werckercli.tests.test_suite'
    setup_kwargs['test_suite'] = 'werckercli.tests.test_suite'

# print has_setuptools
setup(name='wercker',
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
      packages=['werckercli', 'werckercli.tests', 'werckercli.commands'],
      scripts=['bin/wercker', ],
      install_requires=[
          'dulwich>=0.8.7',
          'docopt>=0.6.0',
          'blessings>=1.5',
          'humanize>=0.5',
          'requests>=1.2.0',
          'semantic_version>=2.2.0',
          'PyYAML>=3.10',
          # 'enhancedyaml>=0.1.1',
      ],
      tests_require=tests_require,
      extras_require={'test': tests_require},
      distclass=Distribution,
      classifiers=[
          "Development Status :: 4 - Beta",
          'Environment :: Console',
          'Environment :: Web Environment',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Topic :: Utilities',
          "Operating System :: MacOS :: MacOS X",
          'Operating System :: POSIX',
      ],
      **setup_kwargs
      )
