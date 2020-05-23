import unittest
from xComfortMQTT.config import load_config, ConfigError
import io


class TestCongig(unittest.TestCase):

    def test_default(self):
        fd = io.StringIO("""
shc:
  host: 192.168.0.2
  username: utest
  password: ptest
""")

        config = load_config(fd)

        self.assertEqual(config['mqtt']['host'], '127.0.0.1')
        self.assertEqual(config['mqtt']['port'], 1883)
        self.assertEqual(config['mqtt']['prefix'], 'xcomfort')

    def test_custom(self):
        fd = io.StringIO("""
mqtt:
  host: 192.168.0.1
  port: 1990
  prefix: aaa

shc:
  host: 192.168.0.2
  username: utest
  password: ptest
""")

        config = load_config(fd)

        self.assertEqual(config['mqtt']['host'], '192.168.0.1')
        self.assertEqual(config['mqtt']['port'], 1990)
        self.assertEqual(config['mqtt']['prefix'], 'aaa')

        self.assertEqual(config['shc']['host'], '192.168.0.2')
        self.assertEqual(config['shc']['username'], 'utest')
        self.assertEqual(config['shc']['password'], 'ptest')

    def test_missing_shc_key(self):
        fd = io.StringIO("""
mqtt:
  host: 192.168.0.1
""")
        with self.assertRaises(ConfigError) as cm:
            load_config(fd)
        self.assertEqual(cm.exception.args[0], "Missing key: 'shc'")


if __name__ == '__main__':
    unittest.main()
