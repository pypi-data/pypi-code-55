import PrimeAPIClient
import unittest
import os
import json

url = 'https://prime-server.local'
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')


def run_full_test():
    client = PrimeAPIClient.Client(api_version='v3')

    print(f'***** Testing: Login '.ljust(60, '*'))
    client.connect(url, username, password)

    print(f'***** Testing: GET method '.ljust(60, '*'))
    query_string = {'.full': 'true', '.sort': 'severity', 'category.value': 'AP',
                    'message': 'contains("interface")', '.maxResults': '5'}
    response = client.get(method='/data/Alarms.json', **query_string)
    print(json.dumps(response.json(), indent=4))

    print(f'***** Testing: Logout '.ljust(60, '*'))
    client.disconnect()


class TestPrimeAPIWrapper(unittest.TestCase):

    def test_authentication(self):
        client = PrimeAPIClient.Client(api_version='v3')

        client.connect(url, username, password)
        self.assertIsInstance(client.token, bytes)

        client.disconnect()
        self.assertEqual(client.token, None)

    def test_methods_get_put_post_delete(self):
        client = PrimeAPIClient.Client(api_version='v3')

        client.connect(url, username, password)

        response = client.get(method='/data/Alarms.json')
        self.assertEqual(response.status_code, 200)

        client.disconnect()


if __name__ == '__main__':
    unittest.main()
