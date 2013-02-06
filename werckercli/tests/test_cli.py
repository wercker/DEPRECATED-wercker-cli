# import os
import mock

from werckercli.tests import (
    TestCase,
)

from werckercli import cli
from werckercli.git import RemoteOption


class PrintIntroTtests(TestCase):

    def test_get_intro(self):

        result = cli.get_intro()

        self.assertTrue(result.find('wercker') != -1)


class HanldeCommandsTests(TestCase):

    @mock.patch('werckercli.authentication.get_access_token', mock.Mock())
    @mock.patch('werckercli.commands.create.create', mock.Mock())
    @mock.patch('werckercli.commands.login.login', mock.Mock())
    @mock.patch('werckercli.authentication.get_access_token', mock.Mock())
    @mock.patch(
        'werckercli.commands.clearsettings.clear_settings',
        mock.Mock()
    )
    def test_implemented_base_commands(self):
        my_cli = cli
        with mock.patch('werckercli.commands.deploy.add', mock.Mock()):
            with mock.patch(
                'werckercli.authentication.get_access_token',
                mock.Mock()
            ):

                # create
                my_cli.handle_commands(
                    {
                        'app': False,
                        'create': True,
                        'logout': False,
                        'login': False,
                        'deploy': False,
                    }
                )

                #app create
                my_cli.handle_commands(
                    {
                        'app': True,
                        'create': True,
                        'logout': False,
                        'login': False,
                        'deploy': False,
                    }
                )

                # logout
                my_cli.handle_commands(
                    {
                        'app': False,
                        'create': False,
                        'logout': True,
                        'login': False,
                        'deploy': False,
                    }
                )

                my_cli.handle_commands(
                    {
                        'add': False,
                        'app': False,
                        'create': False,
                        'logout': False,
                        'login': True,
                        'deploy': False,
                    }
                )

                # deploy add
                my_cli.handle_commands(
                    {
                        'add': True,
                        'app': False,
                        'create': False,
                        'logout': False,
                        'login': False,
                        'deploy': True,
                    }
                )


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
        my_cli = cli
        result = my_cli.enter_url(loop=False)

        self.assertEqual(result, None)

VALID_URL = "git@github.com:wercker/wercker-bruticus.git"


class PickUrlOneOptionTests(TestCase):

    repo_name = "github-ssh"

    options = [
        RemoteOption(VALID_URL,  "origin", 2),
        # RemoteOption(VALID_URL+'2',  "secondary", 1),
        # RemoteOption('VALID_URL',  "other", 0)
    ]

    @mock.patch("__builtin__.raw_input", mock.Mock(return_value=""))
    @mock.patch("werckercli.cli.enter_url", mock.Mock(return_value=""))
    @mock.patch("clint.textui.puts", mock.Mock())
    def test_create_default(self):

        my_cli = reload(cli)
        result = my_cli.pick_url(self.options)
        self.assertEqual(
            result,
            "git@github.com:wercker/wercker-bruticus.git"
        )

    @mock.patch("__builtin__.raw_input", mock.Mock(return_value="1"))
    @mock.patch("werckercli.cli.enter_url", mock.Mock(return_value=""))
    @mock.patch("clint.textui.puts", mock.Mock())
    def test_create_1(self):

        my_cli = reload(cli)
        result = my_cli.pick_url(self.options)
        self.assertEqual(
            result,
            VALID_URL
        )

    @mock.patch("__builtin__.raw_input", mock.Mock(return_value="2"))
    @mock.patch("clint.textui.puts", mock.Mock())
    def test_create_2(self):

        my_cli = reload(cli)
        with mock.patch(
            "werckercli.cli.enter_url",
            mock.Mock(return_value="VALID_URL")
        ):

            result = my_cli.pick_url(self.options)
        self.assertEqual(
            result,
            "VALID_URL"
        )
