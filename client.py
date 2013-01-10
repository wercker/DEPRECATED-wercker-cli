import base64
import httplib
import json

__version__ = '0.0.1'

class Client(object):

    def __init__(self, username=None, access_key=None):
        self.username = username
        self.access_key = access_key
        self.headers = self.make_headers()
        #self.information = Information(self)
        #self.jobs = Jobs(self)
        #self.provisioning = Provisioning(self)
        #self.usage = Usage(self)

    def make_headers(self):
        base64string = base64.encodestring(
            '%s:%s' % (self.username, self.access_key)
        )[:-1]
        headers = {
            'Authorization': 'Basic %s' % base64string,
            'Content-Type': 'application/json',
        }
        return headers

    def request(self, method, url, body=None):
        connection = httplib.HTTPSConnection('saucelabs.comz')
        connection.request(method, url, body, headers=self.headers)
        response = connection.getresponse()
        json_data = response.read()
        connection.close()
        if response.status != 200:
            raise Exception('%s: %s.\nSauce Status NOT OK' %
                            (response.status, response.reason))
        return json_data