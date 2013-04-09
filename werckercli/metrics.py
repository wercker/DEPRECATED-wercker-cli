import requests
import json
import base64

mixpanel_api_url_template = "http://api.mixpanel.com/track/?data=%s&ip=1"
token = "509041bd3dd934157b1d3d00bb450ebc"

def track_command_usage(command_name):
    """ List a command as used """

    data = { "event": "cli command executed",
             "properties": {
                "command_name": command_name,
                "token": token,
            }}

    encoded_data = base64.b64encode(json.dumps(data))
    response = requests.get(mixpanel_api_url_template % encoded_data)
    print response.json()
