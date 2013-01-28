# import os
from httpretty import HTTPretty
# from mock import MagicMock, patch, Mock, create_autospec
import json
import mock
# import getpass

from werckercli.tests import (
    BasicClientCase,
)

# from utils import (
    # open_repo,
    # tear_down_repo,
    # duplicate_repo_folder,
    # remove_repo_folder
# )

from werckercli.client import (
    PATH_BASIC_ACCESS_TOKEN
)
# from werckercli.base import (
#     # find_git_root,
#     # get_global_wercker_path,
#     # WERCKER_FOLDER_NAME,
#     # WERCKER_CREDENTIALS_FILE,
#     # get_global_wercker_filename,
#     # check_or_create_path
#     do_login,
#     # get_access_token
# )

from werckercli import base

# class DoLoginTests(TempHomeSettingsCase)

    # def


class DoLoginTests(BasicClientCase):

    @mock.patch('getpass.getpass', mock.Mock(return_value='test'))
    @mock.patch('__builtin__.raw_input', mock.Mock(return_value='test'))
    def test_do_Login(self):
        self.register_api_call(
            PATH_BASIC_ACCESS_TOKEN,
            [
                {
                    'body':
                    json.dumps(
                        {
                            "success": True,
                            "result":
                            {
                                "token": self.valid_token
                            }
                        }
                    ),
                    'status': 200
                },
                {
                    'body':
                    json.dumps(
                        {
                            "success": True,
                            "result":
                            {
                                "token": self.valid_token + "1"
                            }
                        }
                    ),
                    'status': 200
                },
            ]
        )

        my_base = reload(base)
        result = my_base.do_login()

        self.assertEqual(result, self.valid_token)

        result = my_base.do_login()

        self.assertEqual(result, self.valid_token + "1")

    @mock.patch('getpass.getpass', mock.Mock(return_value='test'))
    @mock.patch('__builtin__.raw_input', mock.Mock(return_value='test'))
    def test_do_login_retry_test(self):
        self.register_api_call(
            PATH_BASIC_ACCESS_TOKEN,
            [
                {
                    'body':
                    json.dumps(
                        {
                            "success": False,
                            "result":
                            {
                                "token": self.valid_token
                            }
                        }
                    ),
                    'status': 404
                },
                {
                    'body':
                    json.dumps(
                        {
                            "success": False,
                            "result":
                            {
                                "token": self.valid_token + "1"
                            }
                        }
                    ),
                    'status': 404
                },
                {
                    'body':
                    json.dumps(
                        {
                            "success": True,
                            "result":
                            {
                                "token": self.valid_token
                            }
                        }
                    ),
                    'status': 200
                },
            ]
        )
        my_base = reload(base)
        result = my_base.do_login()
        self.assertEqual(result, self.valid_token)
        self.assertEqual(len(HTTPretty.latest_requests), 3)
