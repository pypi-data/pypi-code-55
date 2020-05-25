import unittest
from unittest import mock
from vetmanager.host import Domain, HostGatewayUrl, BillingApiUrl
from vetmanager.host import HostName, FakeHost, HostNameFromHostGateway
from .mock import MockResponse


class HostTestCase(unittest.TestCase):

    def test_domain(self):
        self.assertEqual(
            str(
                Domain('test')
            ),
            'test'
        )

    def test_billing_api_url(self):
        self.assertEqual(
            str(
                BillingApiUrl('http://some.test')
            ),
            'http://some.test'
        )

    def test_host_gateway_url(self):
        gateway_url = str(
            HostGatewayUrl(
                BillingApiUrl("http://test.url"),
                Domain('test')
            )
        )
        self.assertTrue(
            "http://test.url" in gateway_url
        )
        self.assertTrue(
            "test" in gateway_url
        )

    @mock.patch('vetmanager.host.requests.get')
    def test_host_name_from_gateway_url_valid_response(self, mock):
        mock.return_value = MockResponse({
            "success": True,
            "host": ".testhost.test",
            "url": "test.testhost.test"
        })

        host_name = HostNameFromHostGateway(
            HostGatewayUrl(
                'http://fake.url',
                Domain('domain')
            )
        )
        self.assertEqual(str(host_name), 'test.testhost.test')

    @mock.patch('vetmanager.host.requests.get')
    def test_host_name_from_gateway_url_invalid_response(self, mock):
        mock.return_value = MockResponse({
            "fake": "response"
        })
        with self.assertRaises(Exception):
            str(
                HostNameFromHostGateway(
                    HostGatewayUrl(
                        'http://fake.url',
                        Domain('domain')
                    )
                )
            )

    @mock.patch('vetmanager.host.requests.get')
    def test_host_name_from_gateway_url_invalid_response2(self, mock):
        mock.return_value = MockResponse({
            "success": False,
            "url": "test"
        })
        with self.assertRaises(Exception):
            str(
                HostNameFromHostGateway(
                    HostGatewayUrl(
                        'http://fake.url',
                        Domain('domain')
                    )
                )
            )

    def test_init_host_name_raise_error(self):
        with self.assertRaises(NotImplementedError):
            HostName()

    def test_fake_host(self):
        self.assertEqual(
            str(
                FakeHost()
            ),
            'fake.host'
        )


if __name__ == '__main__':
    unittest.main()
