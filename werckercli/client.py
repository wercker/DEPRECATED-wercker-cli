import json
import requests

from werckercli.cli import puts, get_term, DEBUG
from werckercli.config import get_value, VALUE_WERCKER_URL

PATH_BASIC_ACCESS_TOKEN = 'oauth/basicauthaccesstoken'
PATH_GET_TEMPLATES = 'project/gettemplates'
PATH_CREATE_PROJECT = 'project/create'
PATH_BUILD_PROJECT = 'projects/triggerbuild'
PATH_CREATE_DEPLOYTARGET = 'deploytargets/create'
PATH_DEPLOY_TARGETS_BY_PROJECT = 'deploytargets/byproject'
PATH_GET_APPLICATIONS = 'applications'
PATH_DEPLOY = 'deploy'
PATH_CHECK_PERMISSIONS = 'application/{projectId}/validateAccess'
PATH_SEARCH_BOXES = 'v2/boxes'
PATH_BOX_INFO_AT_VERSION = 'v2/boxes/{name}/{version}'
PATH_BOX_INFO_RELEASES = 'v2/boxes/{name}'
PATH_GET_BUILDS = 'project/{projectId}/builds'
PATH_GET_DEPLOYS = 'deploytarget/{deployTargetId}/deploys'
PATH_GET_PROFILE = 'profile'
# PATH_PROJECT_LIST = 'project/gettemplates'


class LegacyClient():
    wercker_url = get_value(VALUE_WERCKER_URL)
    api_version = '1.0'

    def __init__(self):
        self.wercker_url = get_value(VALUE_WERCKER_URL)

    def do_post(self, path, data):
        """Make the request to the server."""

        url = self.wercker_url + '/api/' + self.api_version + '/' + path

        data_string = json.dumps(data)

        puts("communicating with %s ..." % url, level=DEBUG)

        result = requests.post(
            url,
            data=data_string,
            headers={'Content-Type': 'application/json'})
        puts("done...", level=DEBUG)

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

    def create_project(self, git_url, source_control, token):
        return self.do_post(
            PATH_CREATE_PROJECT,
            {
                'gitUrl': git_url,
                # 'userName': user,
                # 'projectName': project,
                'sourceControl': source_control,
                'token': token,
            })

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

    def get_deploy_targets_by_project(self, token, project):
        return self.do_post(
            PATH_DEPLOY_TARGETS_BY_PROJECT,
            {
                'token': token,
                'projectId': project
            }
        )

    def trigger_build(self, token, project):
        return self.do_post(
            PATH_BUILD_PROJECT,
            {
                'token': token,
                'projectId': project
            })

    def do_deploy(self, token, build, deploy_target):
        return self.do_post(
            PATH_DEPLOY,
            {
                'token': token,
                'targetId': deploy_target,
                'buildId': build
            })


class Client(LegacyClient):
    wercker_url = get_value(VALUE_WERCKER_URL)

    def do_get(self, path, data, display_warnings=True):
        url = self.wercker_url + "/api/" + path

        # data_string = json.dumps(data)

        puts("communicating with %s ..." % url, level=DEBUG)

        result = requests.get(
            url,
            params=data)

        puts("done...", level=DEBUG)

        status = result.status_code
        result_json = {}
        try:
            result_json = result.json()
        except ValueError:
            if display_warnings:
                term = get_term()
                puts(
                    term.yellow("Warning: ") +
                    "Invalid response for api call: {url}".format(url=url)
                )

        return status, result_json

    def get_applications(self, token):
        return self.do_get(PATH_GET_APPLICATIONS, {'token': token})

    def get_builds(self, token, project):
        return self.do_get(
            PATH_GET_BUILDS.format(projectId=project),
            {'token': token}
        )

    def check_permissions(self, token, project):

        return self.do_get(
            PATH_CHECK_PERMISSIONS.format(projectId=project),
            {'token': token}
        )

    def get_deploys(self, token, deploy_target_id):

        return self.do_get(
            PATH_GET_DEPLOYS.format(deployTargetId=deploy_target_id),
            {'token': token}
        )

    def get_profile(self, token):

        return self.do_get(
            PATH_GET_PROFILE,
            {'token': token}
        )

    def get_boxes(self):
        return self.do_get(
            PATH_SEARCH_BOXES,
            {}
        )

    def get_box_releases(self, name, display_warnings=False):
        return self.do_get(
            PATH_BOX_INFO_RELEASES.format(name=name),
            {},
            display_warnings=display_warnings
        )

    def get_box(self, name, version=0, display_warnings=False):
        return self.do_get(
            PATH_BOX_INFO_AT_VERSION.format(
                name=name,
                version=version
            ),
            {},
            display_warnings=display_warnings
        )
    # def do_deploy(self, token, build, target):

    #     return self.
