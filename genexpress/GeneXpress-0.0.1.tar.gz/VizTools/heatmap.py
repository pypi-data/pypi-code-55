import os
import pandas as pd
import seaborn as sns
from VizTools import helpers


def sns_clustermap(df: pd.DataFrame, title="Clustermap", z=None,
                   genes_of_interest: list = None,show_all=True, labels=True,
                   cmap='inferno', sample_clust=True, gene_clust=True, bar_label='log$_2$FC',
                   save_dir="./clustermap", save_plot=False, save_fmt='pdf', file_name=None) -> sns.matrix.ClusterGrid:
    # TODO: Z-score 1 or 0 is axis NOT T/F (0=rows, 1=cols)
    """Create a clustered heatmap of gene expression data.

    Creates a clustered heatmap from a DataFrame of expression data using the seaborn.clustermap function. There is an
    option to insert a title, use z-scored values, only show certain genes, and to show gene labels. If show all and
    labels are true and genes_of_interest != None, a map will be generated only showing labels for genes of interest.
    If show_all is False, a map of only genes_of_interest will be generated.

    Notes:
        - **Important**: A dataframe passed in MUST contain at least two columns and two rows.
        - probably something i'll think of later
        - Seaborn is a thin wrapper around matplotlib.

    Args:
        df: a DataFrame containing only gene expression data from multiple samples to compare.
        title: A title for the clustermap
        z: calculate z-score across genes for all samples in df. Default is False (don't use z-score).
            if z=True then z_score = 0
        genes_of_interest: If show_all=True, only labels for genes in genes_of_interest are displayed. If show_all=False
            a map is generated only using genes in genes_of_interest
        labels: Show labels (True) or hide (False). Default is True
        show_all: Generate map of all genes, or only genes in genes_of_interest iff (if and only if)
        genes_of_interest != None. Otherwise has no effect

    Returns:
        A clustered heatmap (ClusterGrid object)

    """
    if df.isnull().values.any().any():
        df.dropna(axis=0, inplace=True)
    if genes_of_interest is None:
        heatmap = sns.clustermap(df, row_cluster=gene_clust, figsize=(12,10),
                                 col_cluster=sample_clust,
                                 yticklabels=1, cbar_kws={'label': bar_label},
                                 cmap=cmap, center=0, z_score=z)

    else:
        heatmap = sns.clustermap(df.loc[genes_of_interest,:], figsize=(10,8),
                                 row_cluster=gene_clust, col_cluster=sample_clust,
                                 yticklabels=1, cbar_kws={'label': bar_label},
                                 cmap=cmap, center=0, z_score=z)
    # format the figure
    fig = heatmap.fig
    # figw, figh = (10,8)
    # fig.subplots_adjust(left=1/figw, right=1-1/figw, bottom=1/figh, top=1-1/figh)

    fig.suptitle(title)
    # fig.set_size(20)
    # TODO: find some way to scale this with the data rather than just making everything huge
    heatmap.fig.set_size_inches(18.5, 18.5, forward=True)
    # format the ax object
    ax = fig.axes[0]
    if df.shape[0] > 10:
        helpers.add_extended_ticks(ax, tick_len=8, x_ticks=False, rotation=45)
    # else:
        # may not need this
        # formatters.add_ticks(ax)
    #     TODO: adjust figure width
    if df.shape[1] > 10:
        helpers.add_extended_ticks(ax, tick_len=8, x_ticks=True, rotation=45)
    # else:
        # may not need this
        # formatters.add_ticks(ax)
    # helpers.set_text_size(ax.yaxis.label, 10)
    if save_plot:
        if file_name is None:
            file_name = title
        save_path = os.path.join(save_dir, file_name+"."+save_fmt)
        heatmap.savefig(save_path, save_fmt, dpi=400)
    return heatmap




