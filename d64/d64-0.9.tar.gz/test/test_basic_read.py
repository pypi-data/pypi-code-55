import io
import unittest

from d64.basic_file import BASICFile


class TestBASICRead(unittest.TestCase):

    def setUp(self):
        data = b'\x14\x12\x0a\x00\x99\x22\x48\x45\x4c\x4c\x4f\x20\x57\x4f\x52\x4c\x44\x22\x00\x1d\x12\x14\x00\x89\x20\x31\x30\x00\x00\x00'
        self.buf = io.BytesIO(data)
        self.line_nums = (10, 20)
        self.line_tokens = (b'\x99"HELLO WORLD"', b'\x89 10')
        self.line_text = ('10 PRINT"HELLO WORLD"', '20 GOTO 10')

    def test_basic_raw(self):
        self.buf.seek(0)
        f = BASICFile(self.buf, 0x1201)

        for line, line_no, tokens in zip(f.dump(), self.line_nums, self.line_tokens):
            self.assertEqual(line[0], line_no)
            self.assertEqual(line[1], tokens)

    def test_basic_text(self):
        self.buf.seek(0)
        f = BASICFile(self.buf, 0x1201)

        for text, text2 in zip(f.list(), self.line_text):
            self.assertEqual(text, text2)
        self.assertEqual([l for l in f.list(start=20)][0], self.line_text[1])
        self.assertEqual([l for l in f.list(end=15)][-1], self.line_text[0])


if __name__ == '__main__':
    unittest.main()
