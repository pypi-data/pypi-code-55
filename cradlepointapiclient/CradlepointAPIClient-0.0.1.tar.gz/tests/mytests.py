import CradlepointAPIClient
import unittest
import os
import json

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')


def run_full_test():
    client = CradlepointAPIClient.Client(api_version='v2', verify=True)

    print(f'***** Testing: Login '.ljust(60, '*'))
    client.connect(x_cp_api_id='', x_cp_api_key='', x_ecm_api_id='', x_ecm_api_key='')

    print(f'***** Testing: GET method '.ljust(60, '*'))
    response = client.get(method='/groups', offset=0, limit=1)
    print(json.dumps(response.json(), indent=4))

    print(f'***** Testing: Logout '.ljust(60, '*'))
    client.disconnect()


class TestCradlepointAPIWrapper(unittest.TestCase):

    def test_methods_get(self):
        client = CradlepointAPIClient.Client(api_version='v2')
        client.connect(x_cp_api_id='', x_cp_api_key='', x_ecm_api_id='', x_ecm_api_key='')

        response = client.get(method='/groups', offset=0, limit=1)
        self.assertEqual(response.status_code, 200)

        client.disconnect()


if __name__ == '__main__':
    unittest.main()
