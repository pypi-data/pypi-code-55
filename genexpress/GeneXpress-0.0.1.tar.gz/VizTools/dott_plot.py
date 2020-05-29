import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from VizTools import helpers
plt.style.use('seaborn-darkgrid')
# mpl.rc({'size': 3})
# mpl.rcParams.update({'figure.autolayout': True})


def dot_plot(dfs, names=None, fdr_cutoff=0.1, n_rows=50, sort_on=0, zero_replace=0.00001, title="Title"):

    fig, ax = plt.subplots(1, 1, figsize=(len(dfs)*3, dfs[0].shape[0]*0.2))
    ax.set_title(title, {'fontsize': 30})
    ax.set_aspect(.25)
    dfs = [df.iloc[:n_rows, :] for df in dfs]
    x_mesh, y_mesh = np.meshgrid(np.arange(len(dfs)), np.arange(dfs[0].shape[0]))
    nes_max = max([i.max()['nes'] for i in dfs])
    nes_min = min([i.min()['nes'] for i in dfs])
    b_r = colors.LinearSegmentedColormap.from_list("BluRed", ['b','r'])
    cmap = helpers.make_midpoint_mappable(nes_max, nes_min, cmap=b_r)

    filtered = []
    for idx, df in enumerate(dfs):
        filtered.append(df.loc[df['fdr'] < 0.5, :])
    idx = [df.index for df in filtered]
    common = set(idx[0]).intersection(*idx)

    common_dfs = [d.loc[common, :] for d in filtered]
    sorter = common_dfs[sort_on]['fdr'].sort_values(ascending=False).index
    sorted = []
    for df in common_dfs:
        sorted.append(df.reindex(index=sorter))
    dfs = sorted
    plots = []
    for idx, df in enumerate(dfs):
        # df = df.loc[df['fdr'] < 0.5, :]
        df.loc[:, 'fdr'].replace(0, zero_replace, inplace=True)
        df.loc[df['fdr'] > fdr_cutoff, 'fdr'] = np.nan
        df.loc[:, 'log10fdr'] = -df['fdr'].apply(np.log10)
        # not sure why the tolist and list calls here
        scaled = df.loc[:, 'log10fdr']

        ax.yaxis.grid(True)
        x = list(x_mesh[:len(scaled), idx])
        y = list(y_mesh[:len(scaled), idx])
        # The below lines are also weird
        ax.set_xticks(y)
        ax.set_yticks(y)
        helpers.add_tick_labels(ax, names, rotation=90)
        helpers.add_tick_labels(ax, df.index.to_list(), x_ticks=False, rotation=0)
        ax.autoscale(False)

        nes = df.loc[scaled.index, 'nes'].to_list()
        cmap.set_array([])
        c = cmap.to_rgba(nes)

        s = [i**3 for i in scaled]
        # s = scaled
        ax.scatter(x=x, y=y, s=s, c=c, alpha=0.8)
        ax.set_xlim(-0.5, len(dfs)-.5)
        ax.set_ylim(-1, len(scaled))
        # ax.tick_params(axis='x', labelsize=5)
        # annots = scaled.replace(np.nan, "", regex=True)
        # for i, num in enumerate(annots.to_list()):
        #     ax.annotate(str(num), x[i], y[i])
        plots.append(ax)


    # create the legend
    # leg_ax = plt.axes()
    ax.tick_params(axis='both', which='major', pad=10)
    leg_range = range(int(-np.log10(fdr_cutoff)), int(-np.log10(zero_replace)+1))
    handles = [plt.scatter([],[], color="black", marker="o", s=i**3)
               for i in leg_range]
    handles.reverse()
    leg_labels = [10 ** (-1*i) for i in leg_range]
    leg_labels.reverse()
    fig.legend(handles=handles, labels=leg_labels,
               title='False Discovery Rate')
    fig.colorbar(cmap, label="Normalized Enrichment Score")
    fig.axes[0].set_ylabel("MSigDB Hallmarks", rotation=90, size=20)

    fig.tight_layout()
    return fig, ax

