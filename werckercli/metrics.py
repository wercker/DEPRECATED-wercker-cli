import requests
import json
import base64
import sys

mixpanel_api_url_template = "http://api.mixpanel.com/track/?data=%s&ip=1"
token = "509041bd3dd934157b1d3d00bb450ebc"
default_command_name = "help" # used when application is started without any
                              # argument

def track_command_usage(command_name, arguments=None):
    """ List a command as used """

    data = { "event": command_name,
             "properties": {
                "command_name": command_name,
                "event_source": "cli",
                "token": token,
                "arguments": arguments
            }}

    encoded_data = base64.b64encode(json.dumps(data))
    requests.get(mixpanel_api_url_template % encoded_data)


def track_application_startup():
    command = "help"
    arguments = None

    if len(sys.argv) > 2:
        command = sys.argv[1]

    if len(sys.argv) > 3:
        arguments = sys.argv[2:]

    track_command_usage(command, arguments)
