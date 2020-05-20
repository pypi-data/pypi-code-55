import unittest

from d64.disk_image import D64Image

from test.mock_bam import MockD64BAM
from test.mock_block import MockBlock


class TestD64ImageBlocks(unittest.TestCase):

    def setUp(self):
        self.image = D64Image(None)
        self.image.dir_block = MockBlock()

    def test_max_sectors(self):
        self.assertEqual(self.image.max_sectors(1), 21)
        self.assertEqual(self.image.max_sectors(5), 21)
        self.assertEqual(self.image.max_sectors(10), 21)
        self.assertEqual(self.image.max_sectors(15), 21)
        self.assertEqual(self.image.max_sectors(20), 19)
        self.assertEqual(self.image.max_sectors(25), 18)
        self.assertEqual(self.image.max_sectors(30), 18)
        self.assertEqual(self.image.max_sectors(35), 17)

    def test_max_sectors_bad(self):
        with self.assertRaises(ValueError):
            self.image.max_sectors(0)
        with self.assertRaises(ValueError):
            self.image.max_sectors(36)

    def test_block_start(self):
        self.assertEqual(self.image.block_start(1, 0), 0)
        self.assertEqual(self.image.block_start(1, 1), 256)
        self.assertEqual(self.image.block_start(1, 20), 5120)
        self.assertEqual(self.image.block_start(2, 0), 5376)
        self.assertEqual(self.image.block_start(35, 16), 174592)

    def test_block_start_bad(self):
        with self.assertRaises(ValueError):
            self.image.block_start(0, 0)
        with self.assertRaises(ValueError):
            self.image.block_start(1, 21)


class TestD64ImageAlloc(unittest.TestCase):

    def setUp(self):
        self.image = D64Image(None)
        self.image.bam = MockD64BAM()

    def test_alloc_first_below(self):
        self.image.bam.fill_entry(17)
        block = self.image.alloc_first_block()
        self.assertIsNotNone(block)
        self.assertEqual(block.track, 17)
        self.assertEqual(block.sector, 0)
        block = self.image.alloc_first_block()
        self.assertIsNotNone(block)
        self.assertEqual(block.track, 17)
        self.assertEqual(block.sector, 1)

    def test_alloc_first_above(self):
        self.image.bam.clear_entry(17)
        self.image.bam.fill_entry(19)
        block = self.image.alloc_first_block()
        self.assertIsNotNone(block)
        self.assertEqual(block.track, 19)
        self.assertEqual(block.sector, 0)
        block = self.image.alloc_first_block()
        self.assertIsNotNone(block)
        self.assertEqual(block.track, 19)
        self.assertEqual(block.sector, 1)

    def test_alloc_first_full(self):
        for t in range(1, 36):
            self.image.bam.clear_entry(t)
        self.image.bam.fill_entry(18)
        self.assertIsNone(self.image.alloc_first_block())

    def test_alloc_next_interleave(self):
        self.image.bam.fill_entry(17)
        block = self.image.alloc_next_block(17, 0, 10)
        self.assertIsNotNone(block)
        self.assertEqual(block.track, 17)
        self.assertEqual(block.sector, 10)
        block = self.image.alloc_next_block(17, 0, 10)
        self.assertIsNotNone(block)
        self.assertEqual(block.track, 17)
        self.assertEqual(block.sector, 11)
        block = self.image.alloc_next_block(17, 16, 10)
        self.assertIsNotNone(block)
        self.assertEqual(block.track, 17)
        self.assertEqual(block.sector, 4)
        block = self.image.alloc_next_block(17, 11, 10)
        self.assertIsNotNone(block)
        self.assertEqual(block.track, 17)
        self.assertEqual(block.sector, 0)

    def test_alloc_diff_track(self):
        self.image.bam.clear_entry(17)
        self.image.bam.fill_entry(16)
        block = self.image.alloc_next_block(17, 0, 10)
        self.assertIsNotNone(block)
        self.assertEqual(block.track, 16)
        self.assertEqual(block.sector, 10)

    def test_alloc_above(self):
        for t in range(1, 18):
            self.image.bam.clear_entry(t)
        self.image.bam.fill_entry(19)
        block = self.image.alloc_next_block(17, 0, 10)
        self.assertIsNotNone(block)
        self.assertEqual(block.track, 19)
        self.assertEqual(block.sector, 10)

    def test_alloc_dir(self):
        for t in range(1, 36):
            self.image.bam.clear_entry(t)
        self.image.bam.fill_entry(18)
        block = self.image.alloc_next_block(17, 0, 10)
        self.assertIsNotNone(block)
        self.assertEqual(block.track, 18)
        self.assertEqual(block.sector, 10)

    def test_alloc_full(self):
        for t in range(1, 36):
            self.image.bam.clear_entry(t)
        block = self.image.alloc_next_block(17, 0, 10)
        self.assertIsNone(block)


if __name__ == '__main__':
    unittest.main()
