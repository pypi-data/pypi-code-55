import plotly.offline
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from VizTools.helpers import construct_point, create_diagonal_trues
import pandas as pd
import numpy as np


def plot_pca2(df, filters=None):
    # index has sample names, colors+markers should be constructed with filter
    if filters is None:
        filters = create_diagonal_trues(df)
        markers, colors = construct_point(filters.shape)
    else:
        markers, colors = construct_point(filters.index)
    fig, ax = plt.subplots(figsize=(10, 8))



def plot_pca(df, rows, batch: bool =False):
    """Plots PCA data on a scatter plot where x = PC1 and y = PC2

    Plot the first two principal components of PC analyzed data on a scattermap. Plotting PCs can be used as a measure
    for batch effect or correction. PCA can also be used to determine correlation of a list of interest genes.

    Notes:
        - Perform PCA on specific genes to utilize PCA for non-batch analysis

    Args:
        df: a DataFrame containing PC analyzed data to plot on a scatter plot (x = PC1, y= PC2)
        rows: A dictionary that maps each sample or batch to each PC data experiment/sample in df.
        batch: consider changing to 'group' for generic grouping
    Returns:
        Figure and Axes objects

    """
    markers, colors = construct_point(df.shape[0])
    cdict = dict(zip(rows.keys(), colors))
    marker = dict(zip(rows.keys(), markers))
    fig, ax = plt.subplots(figsize=(10, 8))
    if batch:
        # consider changing batch to 'group' for generic grouping
        labels = ['Batch {}'.format(i+1) for i in range(len(colors))]
    else:
        labels = df.index.to_list()
    for k, v in rows.items():
        ax.scatter(x=df.loc[v, 'Principal Component 1'],
                   y=df.loc[v, 'Principal Component 2'],
                   c=[cdict.get(k)],
                   marker=marker.get(k), label=labels[k],
                   s=55)
    plt.xlabel("Principal Component 1", fontsize=15)
    plt.ylabel("Principal Component 2", fontsize=15)

    for i in df.index.to_list():
        ax.annotate(i, (df.loc[i, ['Principal Component 1']]+.05, df.loc[i, ['Principal Component 2']]+.05))
    # ax.legend(loc='upper right', bbox_to_anchor=(1.04, 1))
    plt.tight_layout()
    ax.legend().remove()
    return fig, ax


def plotly_3d_pca(df, batch: bool = False):
    markers, colors = construct_point(df.shape[0])
    # cdict = dict(zip(rows.keys(), colors))
    # marker = dict(zip(rows.keys(), markers))
    # if batch:
    #     # consider changing batch to 'group' for generic grouping
    #     labels = ['Batch {}'.format(i+1) for i in range(len(colors))]
    # else:
    #     labels = df.index.to_list()
    x = df.T.loc['Principal Component 1']
    y = df.T.loc['Principal Component 2']
    z = df.T.loc['Principal Component 3']
    fig = plotly.offline.plot(go.Figure(go.Scatter3d(x=x, y=y,z=z, mode='markers', text=labels)))
    fig.update_traces(textposition='top center')
    fig.update_layout(title_text='3D PCA of LPP Nanostring by groups')
    fig.update_layout(scene=dict(
        xaxis_title='Principal Component 1',
        yaxis_title='Principal Component 2',
        zaxis_title='Principal Component 3'))
    return fig


def plotly_3d_clusters(df):
    x = df.T.loc['Principal Component 1']
    y = df.T.loc['Principal Component 2']
    z = df.T.loc['Principal Component 3']
    scatter = dict(
        mode="markers",
        name="y",
        type="scatter3d",
        x=x, y=y, z=z,
        marker=dict(size=2, color="rgb(23, 190, 207)")
    )
    clusters = dict(
        alphahull=7,
        name="y",
        opacity=0.1,
        type="mesh3d",
        x=x, y=y, z=z
    )
    layout = dict(
        title='3d point clustering',
        scene=dict(
            xaxis=dict(zeroline=False),
            yaxis=dict(zeroline=False),
            zaxis=dict(zeroline=False),
        )
    )
    fig = dict(data=[scatter, clusters], layout=layout)
    plot = plotly.offline.plot(fig)
    return plot
