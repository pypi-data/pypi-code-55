#!/usr/bin/env python3
from unittest import TestCase, main
from os.path import isfile, isdir, abspath, dirname, getsize


from piran import Random, build, compute

location = dirname(dirname(abspath(__file__)))
del abspath, dirname

class OSAssertions:
    def assertIsFile(self, file_path):
        if isfile(file_path) is False:
            raise AssertionError(f'File does not exist: {file_path}.')
    def assertIsNotFile(self, file_path):
        if isfile(file_path) is True:
            raise AssertionError(f'File does exist: {file_path}.')
    def assertIsDir(self, dir_path):
        if isdir(dir_path) is False:
            raise AssertionError(f'Directory does not exist: {dir_path}.')
    def assertIsNotDir(self, dir_path):
        if isdir(dir_path) is True:
            raise AssertionError(f'Directory does not exist: {dir_path}.')

class TestRandom(TestCase, OSAssertions):
    def setUp(self):
        self.STEP = self.MAX_UINT = 100
        self.TESTS = 1_000
        self.r = Random()
        self.assertIsFile(self.r._cursor_file_name)
        self.assertIsFile(self.r._pi_file_name)

    def tearDown(self):
        self.assertIsFile(self.r._cursor_file_name)
        cursor: int = self.r.get_cursor()
        self.assertIsInstance(cursor, int)
        self.assertEqual(self.r.close(), cursor)
        self.assertIsNotFile(self.r._cursor_file_name)

    def test_get_cursor(self):
        self.assertIsInstance(self.r.get_cursor(), int)
        self.assertEqual(self.r.get_cursor(), 0)

    def test_set_cursor(self):
        self.assertIsInstance(self.r.set_cursor(self.STEP), int)
        self.assertEqual(self.r.get_cursor(), self.STEP)

    def test_add_to_cursor(self):
        before: int = self.r.get_cursor()
        self.assertIsInstance(before, int)
        self.assertIsInstance(self.r.add_to_cursor(self.STEP), int)
        after: int = self.r.get_cursor()
        self.assertIsInstance(after, int)
        self.assertEqual(after, before + self.STEP)

    def test_digits(self):
        digits = self.r.digits(self.STEP)
        self.assertIsInstance(digits, str)
        self.assertEqual(len(digits), self.STEP)

    def test_get_cursor_max(self):
        self.assertIsFile(self.r._cursor_file_name)
        self.assertIsInstance(self.r.get_cursor_max(), int)

    def test_uint(self):
        for i in range(self.TESTS):
            unsigned_rand: int = self.r.uint(self.MAX_UINT)
            self.assertIsInstance(unsigned_rand, int)
            self.assertGreaterEqual(unsigned_rand, 0)
            self.assertLess(unsigned_rand, self.MAX_UINT)

    def test_uint(self):
        for i in range(self.TESTS):
            signed_rand: int = self.r.sint(-self.MAX_UINT, self.MAX_UINT)
            self.assertIsInstance(signed_rand, int)
            self.assertGreaterEqual(signed_rand, -self.MAX_UINT)
            self.assertLess(signed_rand, self.MAX_UINT)

class TestBuild(TestCase, OSAssertions):
    def setUp(self):
        self.src_dir = f'{location}/src'
        self.source_files_dir = f'{self.src_dir}/piran'
        self.c_files = ['pi.c']
        self.so_file = f'{self.source_files_dir}/pi.so'
    def test_is_src_dir(self):
        self.assertIsDir(self.src_dir)
    def test_is_source_files_dir(self):
        self.assertIsDir(self.source_files_dir)
    def test_c_files(self):
        for c_file in self.c_files:
            self.assertIsFile(f'{self.source_files_dir}/{c_file}')
    def test_build(self):
        self.assertIsNone(build())
        self.assertIsFile(self.so_file)

class TestCompute(TestCase, OSAssertions):
    def setUp(self):
        self.so_file = f'{location}/src/piran/pi.so'
        self.pi_file = f'{location}/src/piran/pi'
        self.DIGITS = 10_000
    def test_is_so(self):
        self.assertIsFile(self.so_file)
    def test_compute(self):
        self.assertIsNone(compute(self.DIGITS))
        self.assertEqual(getsize(self.pi_file), self.DIGITS)

if __name__ == '__main__':
    main()
