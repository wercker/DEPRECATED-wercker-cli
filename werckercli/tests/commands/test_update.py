import mock

from werckercli.tests import TestCase
from werckercli.commands import update


class UpdateTests(TestCase):

    LOW_VERSION = '0.0.1'
    HIGH_VERSION = '999.999.999'

    @mock.patch("werckercli.commands.update.puts", mock.Mock())
    def test_newer_version(self):
        self.assertTrue(update.update(self.LOW_VERSION))

    @mock.patch("werckercli.commands.update.puts", mock.Mock())
    def test_not_newer_version(self):
        self.assertFalse(update.update(self.HIGH_VERSION))
