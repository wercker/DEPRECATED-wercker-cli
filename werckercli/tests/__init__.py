

"""Test for werckercli"""

import sys
import os

if sys.version_info >= (2, 7):
    # If Python itself provides an exception, use that
    import unittest
    from unittest import SkipTest, TestCase as _TestCase
else:
    import unittest2 as unittest
    from unittest2 import SkipTest, TestCase as _TestCase

class TestCase(_TestCase):

    def makeSafeEnv(self):
        """Create environment with homedirectory-related variables stripped.

        Modifies os.environ for the duration of a test case to avoid
        side-effects caused by the user's ~/.gitconfig and other
        files in their home directory.
        """
        old_env = os.environ
        def restore():
            os.environ = old_env
        self.addCleanup(restore)
        new_env = dict(os.environ)
        for e in ['HOME', 'HOMEPATH', 'USERPROFILE']:
            new_env[e] = '/nosuchdir'
        os.environ = new_env

    def setUp(self):
        super(TestCase, self).setUp()
        self.makeSafeEnv()


def self_test_suite():
    names = [
        'git',
        ]
    module_names = ['werckercli.tests.test_' + name for name in names]
    loader = unittest.TestLoader()
    return loader.loadTestsFromNames(module_names)


def test_suite():
	result = unittest.TestSuite()
	result.addTests(self_test_suite())

 	return result

