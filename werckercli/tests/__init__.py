

"""Test for werckercli"""

import sys

if sys.version_info >= (2, 7):
    # If Python itself provides an exception, use that
    import unittest
    from unittest import SkipTest, TestCase as _TestCase
else:
    import unittest2 as unittest
    from unittest2 import SkipTest, TestCase as _TestCase


def test_suite():
	result = unittest.TestSuite()

 	return result


