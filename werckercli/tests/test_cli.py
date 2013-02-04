import mock

from werckercli.tests import (
    TestCase,

)

from werckercli import cli


class PrintIntroTtests(TestCase):

    def test_get_intro(self):

        result = cli.get_intro()

        self.assertTrue(result.find('wercker') != -1)


class HanldeCommandsTests(TestCase):

    @mock.patch('werckercli.commands.create.create', mock.Mock())
    @mock.patch(
        'werckercli.commands.clearsettings.clear_settings',
        mock.Mock()
    )
    def test_implemented_base_commands(self):
        my_cli = reload(cli)
        my_cli.handle_commands({'create': True, 'logout': False})

        my_cli.handle_commands({'create': False, 'logout': True})


VALID_GIT_SSH_KEY = "git@github.com:wercker/wercker-bruticus.git"


class EnterUrlTests(TestCase):

    @mock.patch('werckercli.prompt.yn', mock.Mock(return_value=True))
    @mock.patch('werckercli.git.get_priority', mock.Mock(return_value=1))
    @mock.patch(
        '__builtin__.raw_input',
        mock.Mock(return_value=VALID_GIT_SSH_KEY)
    )
    def test_valid_ssh(self):
        my_cli = reload(cli)
        result = my_cli.enter_url()

        self.assertEqual(result, VALID_GIT_SSH_KEY)

    @mock.patch('clint.textui.puts', mock.Mock(return_value=False))
    @mock.patch('werckercli.prompt.yn', mock.Mock(return_value=True))
    @mock.patch('werckercli.git.get_priority', mock.Mock(return_value=0))
    @mock.patch(
        '__builtin__.raw_input',
        mock.Mock(return_value="INVALID_GIT_SSH_KEY")
    )
    def test_force_unknown_location(self):
        my_cli = reload(cli)
        result = my_cli.enter_url(loop=False)

        self.assertEqual(result, "INVALID_GIT_SSH_KEY")

    @mock.patch('clint.textui.puts', mock.Mock(return_value=False))
    @mock.patch('werckercli.prompt.yn', mock.Mock(return_value=False))
    @mock.patch('werckercli.git.get_priority', mock.Mock(return_value=0))
    @mock.patch(
        '__builtin__.raw_input',
        mock.Mock(return_value="INVALID_GIT_SSH_KEY")
    )
    def test_invalid_location_no_loop(self):
        my_cli = reload(cli)
        result = my_cli.enter_url(loop=False)

        self.assertEqual(result, None)
