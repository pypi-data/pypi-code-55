import unittest
import rna.dialects
import rna.path


class PythonModule_Test(unittest.TestCase):
    def setUp(self):
        self._inst = rna.dialects.PythonModule('~/tmp/', 'my_project')

    def test_start_project(self):
        self._inst.start_project()
        # dir creation works
        self.assertTrue(self._inst.base_dir.exists())
        # run it again to check that nothing is copied because everything should
        # exist already
        # self._inst.start_project()

    def tearDown(self):
        rna.path.rm('~/tmp/my_project')


if __name__ == '__main__':
    # unittest.main()
    import logging
    logging.basicConfig(level=logging.INFO)

    p = PythonModule_Test()
    p.setUp()
    p.test_start_project()
