import os
import codecs
import json
import csv
import hashlib
from pathlib import Path

def writefile(path, txt, enc='utf-8'):
    if not isinstance(txt, str):
        txt = str(txt)
    if not Path(path).parent.exists():
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    with codecs.open(path, 'w', enc) as fp:
        fp.write(txt)
        fp.flush()

def readfile(path, enc='utf-8'):
    rtn = None
    with codecs.open(path, 'r', enc) as fp:
        rtn = fp.read()
    return rtn

def writebin(path, dat):
    if not Path(path).parent.exists():
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as fp:
        fp.write(dat)
        fp.flush()

def readbin(path):
    r = None
    with open(path, 'rb') as fp:
        r = fp.read()
    return r

def writejson(path, o):
    if not Path(path).parent.exists():
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    with codecs.open(path, 'w', 'utf-8') as fp:
        json.dump(o, fp)

def readjson(path):
    rtn = None
    if os.path.exists(path):
        with codecs.open(path, 'r', 'utf-8') as fp:
            rtn = json.load(fp)
    return rtn

def writecsv(path, array2d, delimiter=','):
    if not Path(path).parent.exists():
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    with codecs.open(path, 'w', 'utf-8') as fp:
        writer = csv.writer(fp, delimiter=delimiter)
        writer.writerows(array2d)

def readcsv(path):
    rtn = None
    if os.path.exists(path):
        with codecs.open(path, 'r', 'utf-8') as fp:
            reader = csv.reader(fp)
            rtn = list(reader)
    return rtn

def file_encode_convert(src, dst, src_encode='utf-8', dst_encode='gbk'):
    src_encode = src_encode.lower()
    dst_encode = dst_encode.lower()
    with codecs.open(src, 'r', src_encode) as fp:
        new_content = fp.read()
    with codecs.open(src, 'w', dst_encode) as fp:
        fp.write(new_content)
        fp.flush()

def md5(fp):
    hash_md5 = hashlib.md5()
    with open(fp, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
