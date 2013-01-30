import mock

from werckercli.tests import (
    TestCase
)

from werckercli import cli


class PrintIntroTtests(TestCase):

    def test_get_intro(self):

        result = cli.get_intro()

        self.assertTrue(result.find('wercker') != -1)


class HanldeCommandsTest(TestCase):

    @mock.patch('werckercli.commands.create.create', mock.Mock())
    @mock.patch('werckercli.commands.clearsettings.clear_settings', mock.Mock())
    def test_implemented_base_commands(self):
        my_cli = reload(cli)
        my_cli.handle_commands({'create': True, 'logout': False})

        my_cli.handle_commands({'create': False, 'logout': True})
