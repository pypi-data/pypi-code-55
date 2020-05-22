# -*-coding:utf-8-*-
import os
import hashlib
from .gui import (color, gui)
from .environment import CardEnv

color = color()
cui = gui()


def fmd5(f_name):
    hash_md5 = hashlib.md5()
    with open(f_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# scan dir 
def tree(file_path, result):
    file_or_dirs = os.listdir(file_path)
    for fi in file_or_dirs:
        fi_d = os.path.join(file_path, fi)
        if os.path.isdir(fi_d):
            tree(fi_d, result)
        else:
            result.append(fi_d)
    return result


#
def get_files(path, ft):
    results = []
    tree_result = []
    tree(path, tree_result)
    for f in tree_result:
        file_type = os.path.splitext(f)[-1]
        if file_type == ft:
            results.append(f)
        else:
            pass
    return results


def setup_env():
    # env setup
    print('\r\n')
    cui.w('start setup env...')
    env = CardEnv()
    env.card_sdk_setup(env)
    cui.w('env is ready!')
