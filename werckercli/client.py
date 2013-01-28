import os
import json
import requests

PATH_BASIC_ACCESS_TOKEN = 'oauth/basicauthaccesstoken'


class Client():
    wercker_url = os.environ.get("wercker_url", "https://app.wercker.com")
    api_version = '1.0'

    def __init__(self):
        self.wercker_url = os.environ.get(
            "wercker_url",
            "https://app.wercker.com/"
        )

    def do_post(self, path, data):
        """Make the request to the server."""

        url = self.wercker_url + '/api/' + self.api_version + '/' + path

        data_string = json.dumps(data)

        result = requests.post(
            url,
            data=data_string,
            headers={'Content-Type': 'application/json'})

        return result.status_code, json.loads(result.text)

    def request_oauth_token(self, username, password, scope='cli'):
        """Request oauth token"""

        return self.do_post(
            PATH_BASIC_ACCESS_TOKEN,
            {
                'username': username,
                'password': password,
                'oauthscope': scope
            })
