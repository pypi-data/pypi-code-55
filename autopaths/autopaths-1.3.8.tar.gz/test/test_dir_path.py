#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Some simple tests for the autopaths package.

You can run this file like this:

  ipython -i -- ~/repos/autopaths/test/test_symlink.py

"""

# Built-in modules #
import os, inspect

# Get current directory (works always) #
file_name = os.path.abspath((inspect.stack()[0])[1])
this_dir  = os.path.dirname(os.path.abspath(file_name)) + '/'

# All our example file system #
dummy_files = this_dir + 'dummy_file_system/'

# Internal modules #
from autopaths.dir_path import DirectoryPath

###############################################################################
def test_list_files():
    d = DirectoryPath(dummy_files)
    print(list((f.name, str(f.size)) for f in d.files))

def test_symlink():
    d = DirectoryPath(dummy_files)
    source = d['lorem']
    destin = d + 'ipsum/'
    print(source, destin)
    source.link_to(destin)

###############################################################################
if __name__ == '__main__':
    test_list_files()
    test_symlink()