import random
import unittest

import client

class Client(unittest.TestCase):

    def setUp(self):
        self.sc = client.Client(
            'SAUCE_USERNAME',
            'SAUCE_ACCESS_KEY'
        )

    def test_has_instances(self):
        pass
        # self.assertIsInstance(self.sc.information, client.Information)
        # self.assertIsInstance(self.sc.jobs, client.Jobs)
        # self.assertIsInstance(self.sc.provisioning, client.Provisioning)
        # self.assertIsInstance(self.sc.usage, client.Usage)

    def test_headers(self):
        headers = self.sc.headers
        self.assertIsInstance(headers, dict)
        self.assertIn('Authorization', headers)
        self.assertIn('Content-Type', headers)
        self.assertIn('Basic', headers['Authorization'])
        self.assertEqual('application/json', headers['Content-Type'])

    def test_request_get(self):
        pass
        # url = 'rest/v1/info/status'
        # json_data = self.sc.request('GET', url)
        # self.assertIsInstance(json_data, str)

if __name__ == '__main__':
    unittest.main()