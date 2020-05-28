#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from nik.zettelkasten import Zettelkasten
from nik.helpers import find_path

def status(args):

    path = find_path(args)
    z = Zettelkasten(path)
    files = z.index.files

    # Number of files
    N = len(files)
    # Find last modification
    modification = datetime.fromtimestamp(max([f[-1] for f in files]))

    print(f'Path: {z.path}')
    print(f'Files in Zettelkasten: {N}')
    print(f'Last modification: {modification}')
