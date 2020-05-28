#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import random

from math import ceil

from nik.exceptions import ZettelkastenNotFound

def find_path(args):
    ''' Returns the Zettelkasten directory based on specified arguments, environment variables or guessing. '''

    # Figure out Zettelkasten path
    path = args.directory or os.getenv('ZETTELKASTEN_PATH') or ''
    # Expand environment variables
    path = os.path.expanduser(path)

    # Check if Zettelkasten directory exists
    if not path:
        raise ZettelkastenNotFound('Please provide the Zettelkasten explicitly.')
    elif not os.path.exists(path):
        raise ZettelkastenNotFound(f'No Zettelkasten found at path "{path}".')

    return path

def random_identifier(length = 5, alternating = True):

    identifier = ''
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    numbers = list('0123456789')

    if alternating:
        for i in range(ceil(length / 2)):
            identifier += random.choice(alphabet)
            identifier += random.choice(numbers)
    else:
        for i in range(length):
            identifier += random.choice(alphabet + numbers)

    return identifier[:length]
