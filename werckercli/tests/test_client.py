import os
import json

# from httpretty import HTTPretty
from werckercli.tests import (
    BasicClientCase,
)

from werckercli.client import (
    Client,
    PATH_BASIC_ACCESS_TOKEN
)


class BasicClientTests(BasicClientCase):
    wercker_url = "http://localhost:3000"

    TOKEN_VALUE = '50ffd4a6b4e145006c0000031359019219496'

    def setUp(self):
        super(BasicClientTests, self).setUp()

        os.environ['wercker_url'] = self.wercker_url

    def test_core_and_environ_settings(self):

        c = Client()

        self.assertEqual(c.wercker_url, self.wercker_url)
        self.assertTrue(c.api_version, '1.0')

        del os.environ['wercker_url']

        c = Client()

        self.assertFalse(c.wercker_url == self.wercker_url)

    def test_do_post(self):

        asserted_return = {"status_code": "200"}
        asserted_return_string = json.dumps(asserted_return)

        self.register_api_call(
            'test',
            [
                {
                    'body': asserted_return_string,
                    'status': 200
                },
            ]
        )

        c = Client()

        code, result = c.do_post('test', {})

        self.assertEqual(code, 200)
        self.assertEqual(result, asserted_return)
        self.assertEqual(json.dumps(result), asserted_return_string)

    def test_request_oauth_token(self):

        expected_response = {'all_good': 'true'}

        self.register_api_call(
            PATH_BASIC_ACCESS_TOKEN,
            [
                {
                    'body': '{"all_good":"true"}',
                    'status': 200
                },
            ]
        )

        c = Client()

        code, result = c.request_oauth_token('jacco', 'flenter')

        self.assertEqual(expected_response, result)
