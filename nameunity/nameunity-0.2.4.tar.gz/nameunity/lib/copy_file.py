# Author: LucasD11 <yuanzhendai@gmail.com>
#
import os
import shutil
import hashlib


def _md5(path):
    if not os.path.exists(path):
        raise ValueError

    md5_sum = hashlib.md5()
    with open(path, 'rb') as fp:
        md5_sum.update(fp.read())
    return md5_sum.hexdigest()


def copy_file(source, target, dry_run=False):
    """
    Copy file if there is no duplicate.
    """
    duplicate = 0
    if not os.path.isdir(os.path.dirname(target)):
        os.makedirs(os.path.dirname(target))

    while os.path.exists(target):
        if _md5(source) == _md5(target):
            return None
        duplicate += 1

        if duplicate == 1:
            suffix = target.split('.')[-1]
            prefix = target.replace(suffix, '')

        target = prefix + str(duplicate) + '.' + suffix

    if not dry_run:
        shutil.move(source, target)
    return target
