from . import pandas


def save(self, obj, fpath):
    """ save pandas dataframe """
    pandas.save(self, obj, fpath, "to_excel")


def load(self):
    """ load pandas dataframe """
    # todo remove engine once pandas bug fixed
    return pandas.load(self, "read_excel", index_col=0, engine="openpyxl")
