# -*- coding: utf-8 -*-

from os import path
import glob


def isexist(*elem):
    return path.exists(path.join(*elem))


def ls(*elem):
    return glob.glob(path.join(*elem))
