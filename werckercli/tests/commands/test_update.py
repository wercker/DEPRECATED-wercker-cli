import mock

from werckercli.tests import TestCase
from werckercli.commands.update import update


class UpdateTests(TestCase):

    LOW_VERSION = '0.0.1'

    def test_newer_version(self):
        self.assertFalse(update(self.LOW_VERSION))
