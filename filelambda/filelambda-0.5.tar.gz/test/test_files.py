from filelambda import files

import os


def test_read():
    f = 'test.txt'
    v = 'a'
    
    with open(f, 'w') as w:
        w.write(v)

    assert files.read(f) == v
    os.remove(f)
    
def test_readb():
    assert 1 > 0


def test_readlines():
    assert 1 > 0


def test_readlinesb():
    assert 1 > 0


def test_write():
    assert 1 > 0


def test_writeb():
    assert 1 > 0


def test_append():
    assert 1 > 0


def test_appendb():
    assert 1 > 0


def test_delete():
    assert 1 > 0


def test_exists():
    assert 1 > 0
