#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
dendrogram_encode.py: file used to generate hierarchical clustering and subsequent dendrograms from ENCODE DNase-seq
data
"""

import os

import pandas as pd
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

from VEnCode import common_variables as cv

DATA_TYPE = "enhancers"
encode_data_path = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/" \
                   "1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/" \
                   "ENCODE DNase expression in FANTOM5 {}_merged.csv".format(DATA_TYPE)
encode_data = pd.read_csv(encode_data_path, sep=";", engine="python", index_col=0)

values = encode_data.T.values
index = encode_data.T.index

clustering = hierarchy.linkage(values, 'single')

plt.figure(figsize=(14, 14))
dn = hierarchy.dendrogram(clustering, labels=index, color_threshold=0, above_threshold_color='#333333',
                          leaf_rotation=0, orientation="left")

no_axes = False
no_border = True

ax = plt.gca()
if no_axes:
    ax.axis('off')
else:
    dflt_col = "#808080"
    ylbls = ax.get_ymajorticklabels()
    for lbl in ylbls:
        lbl.set_color(dflt_col)

    if no_border:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

path = "D:/Utilizador HDD\OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/1-Research/3-Vencode/" \
       "Fantom5/Dendrograms/"
file_name = "dendro_encode_{}_noBorders.png".format(DATA_TYPE)
output_path = os.path.join(path, file_name)

plt.savefig(output_path, dpi=600, bbox_inches="tight", transparent=True)

retrieve_leaves = False
if retrieve_leaves:
    leaves_list = dn["leaves"]
    leaves_names = [index[x] for x in leaves_list]
    with open("leaves.csv", "w") as f:
        for item in leaves_names:
            f.write("{}\n".format(item))
    print(leaves_names)
