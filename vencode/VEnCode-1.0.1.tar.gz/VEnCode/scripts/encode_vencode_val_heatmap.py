import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from VEnCode.scripts import encode_vencode_val_variables as var


# set the colormap and centre the colorbar
class MidpointNormalize(colors.Normalize):
    """
    Normalise the colorbar so that diverging bars work there way either side from a prescribed midpoint value)

    e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
    """

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))


def get_heatmap(data, path_out=None, order_by=None, one_at_time=False, label_size=7, vmin=True, vmax=None,
                diverging=False):
    def heatmap(df, lbl_size=label_size):
        fig_size = (15, 15)
        plt.figure(figsize=fig_size, dpi=600)

        colormap = plt.cm.get_cmap("plasma_r")
        # colormap = truncate_colormap(colormap, 0.03, 1)  # if you need to use only part of the colormap
        colormap.set_under('w')

        if vmin:
            plot = plt.pcolormesh(df, cmap=colormap, vmin=0.0001)
        else:
            plot = plt.pcolormesh(df, cmap=colormap)
        plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
        plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns, rotation=90)
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            labelsize=lbl_size  # label number size is reduced to fit
        )
        plt.tick_params(
            axis="y",
            which="both",
            labelsize=lbl_size  # label number size is reduced to fit
        )
        cb = plt.colorbar(plot, shrink=0.7)
        cb.ax.tick_params(labelsize=20)
        plt.axes().set_aspect("auto")
        plt.tight_layout()
        if path_out:
            plt.savefig(path_out, transparent=True, dpi="figure")
        else:
            plt.savefig(transparent=True, dpi="figure")
        plt.close()

    def heatmap_diverging(df, lbl_size=label_size):
        fig_size = (15, 15)
        plt.figure(figsize=fig_size, dpi=600)

        # colormap = plt.cm.get_cmap("plasma_r")
        # colormap = truncate_colormap(colormap, 0.03, 1)  # if you need to use only part of the colormap
        colormap = plt.cm.get_cmap("RdBu_r")  # set the colormap to something diverging

        mid_val = 0
        elev_max = np.amax(df.values)
        elev_min = np.amin(df.values)

        if vmin:
            plot = plt.pcolormesh(df, cmap=colormap, vmin=0.0001,
                                  norm=MidpointNormalize(midpoint=mid_val, vmin=elev_min, vmax=elev_max))
        else:
            plot = plt.pcolormesh(df, cmap=colormap, norm=MidpointNormalize(midpoint=mid_val, vmin=elev_min,
                                                                            vmax=elev_max))
        plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
        plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns, rotation=90)
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            labelsize=lbl_size  # label number size is reduced to fit
        )
        plt.tick_params(
            axis="y",
            which="both",
            labelsize=lbl_size  # label number size is reduced to fit
        )
        cb = plt.colorbar(plot, shrink=0.7)
        cb.ax.tick_params(labelsize=20)
        plt.axes().set_aspect("auto")
        plt.tight_layout()
        if path_out:
            plt.savefig(path_out, transparent=True, dpi="figure")
        else:
            plt.savefig(transparent=True, dpi="figure")
        plt.close()

    def heatmap_loop(df, lbl_size=label_size, vmax=vmax):
        fig_size = (15, 15)
        fig = plt.figure(figsize=fig_size, dpi=600)
        ax1 = fig.add_subplot(111)
        colormap = plt.cm.get_cmap("plasma_r")
        colormap.set_under('w')
        plot = ax1.pcolormesh(df, cmap=colormap, vmin=0.0001, vmax=vmax)
        plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
        plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns, rotation=90)
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            labelsize=lbl_size  # label number size is reduced to fit
        )
        plt.tick_params(
            axis="y",
            which="both",
            labelsize=lbl_size  # label number size is reduced to fit
        )
        plt.axes().set_aspect("equal")
        plt.tight_layout()
        cbaxes = fig.add_axes([0.3, 0.8, 0.6, 0.03])
        plt.colorbar(plot, cax=cbaxes, orientation="horizontal")
        if path_out:
            plt.savefig(path_out, transparent=True, dpi="figure")
        else:
            plt.savefig(transparent=True, dpi="figure")
        plt.close()

    if order_by is not None:
        data = data.reindex(order_by[0])
        data = data[order_by[1]]
    if one_at_time:
        for idx in data.index:
            data_temp = data.loc[idx]
            data_temp = data_temp.to_frame()
            heatmap_loop(data_temp.T, lbl_size=label_size, vmax=vmax)
    elif diverging:
        data.to_csv("signal_noise_subtraction_matrix_promoters_validated_matching.csv", sep=";")
        heatmap_diverging(data, lbl_size=label_size)
    else:
        # data.to_csv("CAGE VEn in ENCODE DNase matrix enhancers_validated-normalized_match.csv", sep=";")
        heatmap(data, lbl_size=label_size)


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


data_path_parent = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/1-Research/" \
                   "3-Vencode/Fantom5/Files/Validation_files/ENCODE/Pub/"
data_name = "matrix_promoters_totalrandom-normalized_match.csv"
# data_name = "signal_noise_subtraction_matrix_promoters_validated.csv"
data_path = os.path.join(data_path_parent, data_name)
figure_path = os.path.join(data_path_parent,
                           "ENCODE prom average random.png")
# figure_path = os.path.join(data_path_parent,
#                            "signal_noise_subtraction_matrix_promoters_validated heatmap_matching_d.png")

data_file = pd.read_csv(data_path, sep=";", engine="python", index_col=0)

normalize = pd.read_csv(os.path.join(data_path_parent,
                                     "CAGE VEn in ENCODE DNase matrix promoters_-normalized_match.csv"),
                        sep=";", engine="python", index_col=0)
to_normalize = normalize.values.max()

y_axis = var.index_promoter_matching[::-1]  # we reverse the list because plot axis get reversed during procedure
x_axis = var.columns_promoter_matching
get_heatmap(data_file, figure_path, vmax=to_normalize,
            one_at_time=True, label_size=17, vmin=True, diverging=False)  # order_by=(y_axis, x_axis),
