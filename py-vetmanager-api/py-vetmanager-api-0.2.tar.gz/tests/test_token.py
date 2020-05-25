import unittest
from unittest import mock
from vetmanager.token import Login, Password, AppName, Credentials
from vetmanager.token import Token
from vetmanager.url import Url, Protocol
from vetmanager.host import FakeHost
from .mock import MockResponse


class TokenTest(unittest.TestCase):
    def test_login(self):
        self.assertEqual(
            str(
                Login('test')
            ),
            'test'
        )

    def test_password(self):
        self.assertEqual(
            str(
                Password('test')
            ),
            'test'
        )

    def test_app_name(self):
        self.assertEqual(
            str(
                AppName('test')
            ),
            'test'
        )

    def test_credentials(self):
        self.assertEqual(
            Credentials(
                Login('login'),
                Password('password'),
                AppName('app_name')
            ).as_dict(),
            {
                "login": "login",
                "password": "password",
                "app_name": "app_name"
            }
        )

    @mock.patch('vetmanager.token.requests.post')
    def test_token_valid_response(self, mock):
        mock.return_value = MockResponse(
            json_data={
                "data": {
                    "token": "123"
                }
            }
        )
        self.assertEqual(
            str(
                Token(
                    Url(
                        Protocol('http'),
                        FakeHost()
                    ),
                    Credentials(
                        Login('login'),
                        Password('password'),
                        AppName('app_name')
                    )
                )
            ),
            "123"
        )

    @mock.patch('vetmanager.token.requests.post')
    def test_token_invalid_500status_code(self, mock):
        mock.return_value = MockResponse(
            json_data={
                "title": "error"
            },
            status_code=500
        )
        with self.assertRaises(Exception):
            str(
                Token(
                    Url(
                        Protocol('http'),
                        FakeHost()
                    ),
                    Credentials(
                        Login('login'),
                        Password('password'),
                        AppName('app_name')
                    )
                )
            )


if __name__ == '__main__':
    unittest.main()
