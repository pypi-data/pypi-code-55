import pytest
import os
import struct
import shutil

from zwutils import comm
from zwutils import fileutils

class TestFileUtils:
    def test_binfile(self):
        p = 'data/binfile'
        arr = [10, 20, 30, 40, 92]
        dat = struct.pack('5B', *arr)
        fileutils.writebin(p, dat)
        s = os.path.getsize(p)
        d = fileutils.readbin(p)
        a = struct.unpack('5B', d)
        shutil.rmtree('data', ignore_errors=True)
        assert s == len(arr) and len(comm.list_intersection(arr, a)) == 5
    
    def test_md5(self):
        md5 = fileutils.md5('docs/pytest.pdf')
        assert md5 == 'd2e81dddfd92aa86233be7c18bf3b5d8'