import json
import requests

from werckercli.config import get_value, VALUE_WERCKER_URL

PATH_BASIC_ACCESS_TOKEN = 'oauth/basicauthaccesstoken'
PATH_GET_TEMPLATES = 'project/gettemplates'
PATH_CREATE_PROJECT = 'project/create'
PATH_CREATE_DEPLOYTARGET = 'deploytargets/create'
# PATH_PROJECT_LIST = 'project/gettemplates'


class Client():
    wercker_url = get_value(VALUE_WERCKER_URL)
    api_version = '1.0'

    def __init__(self):
        self.wercker_url = get_value(VALUE_WERCKER_URL)

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

    def create_project(self, git_url, user, project, source_control, token):
        return self.do_post(
            PATH_CREATE_PROJECT,
            {
                'gitUrl': git_url,
                'userName': user,
                'projectName': project,
                'sourceControl': source_control,
                'token': token,
            })
    # def list_projects(self, token):

    def create_deploy_target(self, token, project, deploy_name, heroku_token):
        return self.do_post(
            PATH_CREATE_DEPLOYTARGET,
            {
                'token': token,
                'projectId': project,
                'appName': deploy_name,
                'apiKey': heroku_token,
            }
        )
