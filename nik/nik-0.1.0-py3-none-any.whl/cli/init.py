#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from nik.helpers import find_path

def init(args):

    path = find_path(args)

    # Create necessary directories if they do not yet exist
    root = os.path.join(path, '.nik')
    os.makedirs(root, exist_ok = True)
    html = os.path.join(root, 'html')
    os.makedirs(html, exist_ok = True)
