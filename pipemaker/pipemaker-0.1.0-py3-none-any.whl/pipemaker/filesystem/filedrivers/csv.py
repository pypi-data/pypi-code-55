from . import pandas
import logging

log = logging.getLogger()


def save(self, obj, fpath):
    """ save pandas dataframe """
    pandas.save(self, obj, fpath, "to_csv")


def load(self):
    """ load pandas dataframe """
    return pandas.load(self, "read_csv", index_col=0)
