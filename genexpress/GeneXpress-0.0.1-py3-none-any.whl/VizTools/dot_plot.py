import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors, cm
from VizTools import helpers


def dot_plot(dfs, size_col, color_col, names=None, fdr_cutoff=0.1, n_rows=50,
             sort_on=0, zero_replace=0.00001, title="Title"):
    """
    create a dot plot from a list of dataframes containing nes and fdr
        - size will be determined by log10 fdr and anything with an fdf < .5 wont be plotted
        - color by nes

    Args:
        dfs: a list of dataframes containing columns 'fdr' and 'nes'

    Returns:

    """


def create_meshgrid(x, y):
    return np.meshgrid(x, y)


def iloc_list_dfs(dfs, n, rows=True):
    if rows:
        return [df.iloc[:n, :] for df in dfs]
    else:
        return [df.iloc[:, :n] for df in dfs]


def loc_list_dfs(dfs, col, rows=True):
    pass