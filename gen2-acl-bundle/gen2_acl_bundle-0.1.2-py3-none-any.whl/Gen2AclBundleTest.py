import unittest
from injecta.testing.servicesTester import testServices
from gen2aclbundle.containerInit import initContainer

class Gen2AclBundleTest(unittest.TestCase):

    def test_init(self):
        container = initContainer('test')

        testServices(container)

if __name__ == '__main__':
    unittest.main()
