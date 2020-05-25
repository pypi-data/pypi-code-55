# -*- coding: utf-8 -*-

import unittest
import os, shutil

import exiv2


this_path = os.path.dirname(__file__)
if this_path:
    this_path += os.sep
    
def path(x):
    return this_path + x

TEST_PNG = path("test.png")
TEST_JPG = path("test.jpg")
UNICODE_JPG = path("蛙飛び込む.jpg")

shutil.copy(TEST_JPG,UNICODE_JPG)
        
def from_buffer(path):
    with open(path, "rb") as f:
        imdata = f.read()
    return exiv2.ImageFactory.open(imdata)

class test_exiv2(unittest.TestCase):
    
    def test1(self):
        im = from_buffer(TEST_PNG)
        xmpdata = im.xmpData()
    
        
if __name__ == '__main__':
    unittest.main()
    
    