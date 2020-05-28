import fs
import os
from fs.copy import copy_file
from fs.move import move_file
import pandas as pd
from ..filepath import Filepath

import logging

log = logging.getLogger(__name__)


def save(self, obj, dest, func, **kwargs):
    """ save pandas dataframe to format defined by func e.g. csv, excel

    :param obj: data to save
    :param dest: destination filepath
    :param func: dataframe save function e.g. to_csv
    """
    # save locally
    func = getattr(obj, func)
    Filepath("").ofs.makedirs(dest.dirname(), recreate=True)
    # for pandas functions cannot be leading /
    func(dest.path.lstrip("/"), **kwargs)

    # upload to remote
    if not self.islocal:
        copy_file("", dest.path, f"{dest.fs}{dest.query}", dest.path)


def load(self, func, **kwargs):
    """ load pandas dataframe from format defined by func e.g. csv, excel
    For remote url it will download then read

    :param func: pandas function for loading e.g. read_csv
    """
    # download from remote
    if not self.islocal:
        copy_file(f"{self.fs}{self.query}", self.path, "", self.path)

    # load locally
    func = getattr(pd, func)
    return func(self.path.lstrip("/"), **kwargs)
