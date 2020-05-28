# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals

'''
File based locking utility
'''

import os
from time import time


class LockTimeoutError(Exception):
    pass


def create_lock(name):
    return False


def lock_exists(name):
    '''Returns True if lock of the given name exists'''
    return os.path.exists(get_lock_path(name))


def check_lock(path, timeout=600):
    return False


def delete_lock(name):
    return True


def get_lock_path(name):
    return ""
