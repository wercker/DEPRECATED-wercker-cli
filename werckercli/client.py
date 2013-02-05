import os
import json
import requests

PATH_BASIC_ACCESS_TOKEN = 'oauth/basicauthaccesstoken'
PATH_GET_TEMPLATES = 'project/gettemplates'
PATH_CREATE_PROJECT = 'project/create'
# PATH_PROJECT_LIST = 'project/gettemplates'

DEFAULT_WERCKER_URL = "https://app.wercker.com"


class Client():
    wercker_url = os.environ.get("wercker_url")
    api_version = '1.0'

    def __init__(self):
        self.wercker_url = os.environ.get(
            "wercker_url",
        )
        if self.wercker_url == "":
            self.wercker_url = DEFAULT_WERCKER_URL

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

    def get_templates(self, project, platform, token):
        return self.do_post(
            PATH_GET_TEMPLATES,
            {
                'projectName': project,
                'platform': platform,
                'token': token
            })

    def create_project(self, git_url, user, project, source_control, token):
        return self.do_post(
            PATH_CREATE_PROJECT,
            {
                'gitUrl': git_url,
                'userName': user,
                'projectName': project,
                'sourceControl': source_control,
                'token': token
            })
    # def list_projects(self, token):
