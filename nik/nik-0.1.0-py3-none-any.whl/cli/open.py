#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from nik.zettelkasten import Zettelkasten
from nik.helpers import find_path

def open_(args):

    path = find_path(args)
    z = Zettelkasten(path)

    identifier = args.id
    for ending in ('.md', '.org', '.adoc'):
        path = os.path.join(z.path, identifier + ending)
        if os.path.exists(path):
            print(f'Opening zettel: {path}')
            break
    else:
        print(f'No zettel with ID "{identifier}" found. Quitting.')
        sys.exit(1)

    os.system(f'xdg-open {path}')
