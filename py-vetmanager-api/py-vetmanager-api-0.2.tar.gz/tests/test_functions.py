import unittest
from vetmanager.functions import url, token_credentials, token


class TestFunctions(unittest.TestCase):
    def test_url(self):
        self.assertEqual(
            url('test').__class__.__name__,
            'Url'
        )

    def test_credentials(self):
        self.assertEqual(
            token_credentials(
                login='test',
                password='test',
                app_name='test'
            ).__class__.__name__,
            'Credentials'
        )

    def test_token(self):
        self.assertEqual(
            token(
                url(domain='domain'),
                token_credentials(
                    login='test',
                    password='test',
                    app_name='test'
                )
            ).__class__.__name__,
            'Token'
        )


if __name__ == '__main__':
    unittest.main()
