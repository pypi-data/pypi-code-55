import unittest
from injecta.testing.servicesTester import testServices
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.package.pathResolver import resolvePath
from typing import List
from pyfony.kernel.BaseKernel import BaseKernel
from pyfonybundles.Bundle import Bundle
from consolebundle.ConsoleBundle import ConsoleBundle

class ConsoleBundleTest(unittest.TestCase):

    def test_init(self):
        class Kernel(BaseKernel):

            def _registerBundles(self) -> List[Bundle]:
                return [
                    ConsoleBundle(),
                ]

        kernel = Kernel(
            'test',
            resolvePath('consolebundle') + '/ConsoleBundleTest',
            YamlConfigReader()
        )

        container = kernel.initContainer()

        testServices(container)

if __name__ == '__main__':
    unittest.main()
