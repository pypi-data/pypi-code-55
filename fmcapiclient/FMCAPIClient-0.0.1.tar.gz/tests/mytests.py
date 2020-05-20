import FMCAPIClient
import unittest
import os
import json

url = 'https://FMC-server.local'
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')


def run_full_test():
    client = FMCAPIClient.Client()

    print(f'***** Testing: Login '.ljust(60, '*'))
    client.connect(url, username, password)

    print(f'***** Testing: GET method '.ljust(60, '*'))
    response = client.get(method=f'/devicegroups/devicegrouprecords')
    print(json.dumps(response.json(), indent=4))

    response = client.post(method='/devicegroups/devicegrouprecords', data={'name': 'test_group',
                                                                            'type': 'DeviceGroup'})
    print(json.dumps(response.json(), indent=4))
    group_id = response.json()['id']

    response = client.put(method=f'/devicegroups/devicegrouprecords/{group_id}', data={'id': group_id,
                                                                                       'name': 'test_group_updated',
                                                                                       'type': 'DeviceGroup'})
    print(json.dumps(response.json(), indent=4))

    response = client.delete(method=f'/devicegroups/devicegrouprecords/{group_id}')
    print(json.dumps(response.json(), indent=4))

    print(f'***** Testing: Logout '.ljust(60, '*'))
    client.disconnect()


class TestFMCAPIWrapper(unittest.TestCase):

    def test_authentication(self):
        client = FMCAPIClient.Client()

        response = client.connect(url, username, password)
        self.assertEqual(response.status_code, 204)

        response = client.refresh_token_func()
        self.assertEqual(response.status_code, 204)

        client.disconnect()
        self.assertEqual(response.status_code, 204)

    def test_methods_get(self):
        client = FMCAPIClient.Client()

        client.connect(url, username, password)

        response = client.get(method=f'/devicegroups/devicegrouprecords')
        self.assertEqual(response.status_code, 200)

        response = client.post(method='/devicegroups/devicegrouprecords', data={'name': 'test_group',
                                                                                'type': 'DeviceGroup'})
        self.assertEqual(response.status_code, 201)
        group_id = response.json()['id']

        response = client.put(method=f'/devicegroups/devicegrouprecords/{group_id}', data={'id': group_id,
                                                                                           'name': 'test_group_updated',
                                                                                           'type': 'DeviceGroup'})
        self.assertEqual(response.status_code, 200)

        response = client.delete(method=f'/devicegroups/devicegrouprecords/{group_id}')
        self.assertEqual(response.status_code, 200)

        client.disconnect()


if __name__ == '__main__':
    unittest.main()
