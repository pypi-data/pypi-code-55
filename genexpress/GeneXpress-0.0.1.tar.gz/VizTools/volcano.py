import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from VizTools.helpers import MidpointNormalize



def sns_volcano(colnames, d=None, title=None, genes: list=None):
    # TODO: Adapt to OOP. Look up how mpl does oop vs functional.
    # TODO: split into multiple functions that sns_volcano uses
    """
    Adapted from example at: https://reneshbedre.github.IO/blog/volcano.html
    :param d:
    :return:

    # need to make object oriented but maintain axes
    """
    # y-value is -log10 normalized pvalue
    d, log_p = log_transform(d, colnames['pval'], logbase=10)
    d.dropna(inplace=True)
    # for i1 in d.index:
    #     if "CXCL" in str(i1):
    #         print(i1)
    sns.set_style('darkgrid')
    big = d[colnames['logfc']].nlargest(1).to_numpy()
    small = d[colnames['logfc']].nsmallest(1).to_numpy()
    xlim = big[0] if big[0] > np.fabs(small[0]) else np.fabs(small[0])
    plt.xlim = (-xlim, xlim)
    # plt.pcolor(X=d[colnames['logfc']], Y=d[colnames['pval']])
    # Create a colorbar for the volcano plot
    norm = plt.Normalize(d[colnames['logfc']].max(), d[colnames['logfc']].min())
    midnorm = MidpointNormalize(midpoint=0, vmin=small, vmax=big)
    cmap = sns.diverging_palette(h_neg=250, h_pos=10, as_cmap=True)
    mappable = plt.cm.ScalarMappable(cmap=cmap, norm=midnorm)
    # mappable.set_array([])
    # color dots on a green spectrum
    if 'DEG' in d.columns:

        scat = sns.scatterplot(x=colnames['logfc'], y=log_p,
                               data=d, hue=d[colnames['logfc']],
                               palette=cmap, legend=False)
        # non_deg = d[~d.DEG]
        # greys = non_deg.index.values
        # nans = np.argwhere(np.isnan(greys))
        # greys = greys.nan_to_num(range(len(nans)), copy=True)
        # x = d.loc[greys]
        # plt.scatter(d[greys][colnames["logfc"]], y=d[greys][colnames["pvalue"]], color='grey')
    else:


        scat = sns.scatterplot(x=colnames['logfc'], y=log_p,
                               data=d, hue=d[colnames['logfc']],
                               palette=cmap, hue_norm=midnorm, legend=False)
    scat.figure.colorbar(mappable)
    scat.set_xlabel('Log$_2$FC')
    scat.set_ylabel("Log$_{10}$ Adjusted P-Value")
    scat.figure.suptitle("{}".format(title))
    a = pd.concat({'x': d[colnames['logfc']], 'y': d[log_p], 'val': d.index.to_series()}, axis=1)
    text = []
    if genes is None:
        for i, point in a.iterrows():
            try:
                if d.loc[i, log_p] > 2.0 and (d.loc[i, colnames['logfc']] < -1 or d.loc[i, colnames['logfc']] > 2):
                    scat.text(point['x'] + .15, point['y'], str(point['val']), size=5)

            # This will turn everything below significance gray
            #     else:
            #         scat.scatter(point['x'], point['y'], color='silver')
            except Exception:
                pass

    elif genes is not None:
        for i, point in a.iterrows():
            try:
                if d.loc[i, log_p] > 2.0 and (d.loc[i, colnames['logfc']] < -1 or d.loc[i, colnames['logfc']] > 1) and i in genes:

                    scat.text(point['x'] + .15, point['y'], str(point['val']), size=5)
                    text.append(str(point['val']))

                elif i not in genes:
                    pass
            except Exception:
                print(d.loc[i, log_p])
                # This will turn everything below significance gray
                # else:
                #     scat.scatter(point['x'], point['y'], color='silver')
    # adjustText.adjust_text(a)
    return scat


def display_vals(df, genes_to_display):
    return df.join(genes_to_display, how='inner')

def log_transform(df: pd.DataFrame, col: str or list, logbase=2) -> tuple:
    """Log transform data by log2 or log10
        Perform a log transformation on FC data to eliminate bias between under and over-expressed genes,
        p-value data for volcano plot, or other log transformations.

    Args:
        df: a DataFrame containing some (but not only) data to log transform
        col: column if str or list of columns of df to perform log transformation on
        logbase: the log base to transform data by (default is log2)

    Returns:

    """

    if logbase == 2:
        if isinstance(col, list):
            log_col = list()
            for i in col:
                df[i] = replace_zeroes(df[i], i)
                log = 'log_{}'.format(i)
                log_col.append(log)
                # if logbase == 2:
                #     df[log] = (df[i].apply(np.log2))
                # else:
                df[log] = (df[i].apply(np.fabs))
            return df.copy(deep=True), log
        else:
            df[col] = replace_zeroes(df[col], col)
            log_col = 'log_{}'.format(col)
            df[log_col] = (np.fabs(np.log2(df[col])))
            return df.copy(deep=True), log_col
    else:
        if isinstance(col, list):
            log_col = list()
            for i in col:
                df[i] = replace_zeroes(df[i], i)
                log = 'log_{}'.format(i)
                log_col.append(log)
                df[log] = (df[i].apply(np.log10))
                df[log] = (df[i].apply(np.fabs))
            return df.copy(deep=True), log
        else:
            df[col] = replace_zeroes(df[col], col)
            log_col = 'log_{}'.format(col)
            df[log_col] = (np.fabs(np.log10(df[col])))
            return df.copy(deep=True), log_col


def replace_zeroes(df: pd.DataFrame or pd.Series, col: str):
    """

    Returns:

    """
    # method for lists...?  lowest = df[df > 0].min(axis=0)
    lowest = df.nsmallest(2, keep='first')
    return df.replace(to_replace=0, value=lowest)

