import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
import numpy as np


def dendrogram(df: pd.DataFrame, groups: dict):
    """
    References: https://python-graph-gallery.com/401-customised-dendrogram/
    Args:
        df:

    Returns:

    """
    # del df.index.name
    # working = df.copy().to_numpy()
    dflt_col = "#808080"  # Unclustered gray
    D_leaf_colors = {"attr_1": dflt_col,

                     "attr_4": "#B061FF",  # Cluster 1 indigo
                     "attr_5": "#B061FF",
                     "attr_2": "#B061FF",
                     "attr_8": "#B061FF",
                     "attr_6": "#B061FF",
                     "attr_7": "#B061FF",

                     "attr_0": "#61ffff",  # Cluster 2 cyan
                     "attr_3": "#61ffff",
                     "attr_9": "#61ffff",
                     "attr_10": "#61ffff",
                     "attr_11": "#61ffff",
                     "attr_12": "#61ffff"

                     }

    # notes:
    # * rows in Z correspond to "inverted U" links that connect clusters
    # * rows are ordered by increasing distance
    # * if the colors of the connected clusters match, use that color for link
    # c_dist = distance.pdist(df.T,) # http://datanongrata.com/2019/04/27/67/
    Z = hierarchy.linkage(df.T.to_numpy(), 'ward', metric='complete')
    DF_dism = 1 - np.abs(df.corr())
    link_cols = {}
    for i, i12 in enumerate(Z[:, :2].astype(int)):
        c1, c2 = (link_cols[x] if x > len(Z) else D_leaf_colors["attr_%d" % x]
                  for x in i12)
        link_cols[i + 1 + len(Z)] = c1 if c1 == c2 else dflt_col
    plot = hierarchy.dendrogram(Z, labels=DF_dism.index, color_threshold=None,
                                leaf_font_size=12, leaf_rotation=45, link_color_func=lambda x: link_cols[x])

    # plot = hierarchy.dendrogram(Z, leaf_rotation=90, leaf_font_size=8,
    #                             color_threshold=2.5)
    plt.tight_layout()
    return plot
