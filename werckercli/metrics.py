import requests
import json
import base64

mixpanel_api_url_template = "http://api.mixpanel.com/track/?data=%s&ip=1"
token = "509041bd3dd934157b1d3d00bb450ebc"

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
    response = requests.get(mixpanel_api_url_template % encoded_data)
    print response.json()
