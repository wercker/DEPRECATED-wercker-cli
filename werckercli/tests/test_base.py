# import os
from httpretty import HTTPretty
# from mock import MagicMock, patch, Mock, create_autospec
import json
import mock

from werckercli.tests import (
    BasicClientCase,
)

from werckercli.client import (
    PATH_BASIC_ACCESS_TOKEN
)

from werckercli import base


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


class GetAccessTokenTests(BasicClientCase):
    """docstring for GetAccessTokenTests"""

    def setUp(self):
        super(GetAccessTokenTests, self).setUp()
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
                                "token": "invalid"
                            }
                        }
                    ),
                    'status': 200
                },
            ]
        )

    @mock.patch('getpass.getpass', mock.Mock(return_value='test'))
    @mock.patch('__builtin__.raw_input', mock.Mock(return_value='test'))
    def test_new_login(self):

        my_base = reload(base)
        result = my_base.get_access_token()
        self.assertEqual(result, self.valid_token)

    @mock.patch('getpass.getpass', mock.Mock(return_value='test'))
    @mock.patch('__builtin__.raw_input', mock.Mock(return_value='test'))
    def test_login_again(self):
        self.test_new_login()

        # login again
        self.test_new_login()
