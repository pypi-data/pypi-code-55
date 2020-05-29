import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def density_plot(df: pd.DataFrame, groups: pd.DataFrame = None):
    """Create a density plot from a DataFrame

    Plot density of all samples in df. All columns should be of the same data (e.g. log2fc, read counts, p-values.
    Density plots can be used to determine presence of batch effects

    Args:
        df: a DataFrame containing sample data
        groups: a dictionary mapping each batch to a list of experiments

    Returns:
        A density plot

    """

    # fig = plt.figure(figsize=(10,10))

    groups = groups.to_dict()
    if groups is None:
        plot = df.plot(kind='kde', legend=True)
    else:
        num_colors = len(groups)
        labels = groups.index.to_list()
        cm = plt.get_cmap('gist_rainbow')
        colors = [cm(1. * i / num_colors) for i in range(num_colors)]
        for k, v in [*groups.items()]:
            count = k
            for i in df[[*v]]:
                plot = sns.distplot(df[i], color=colors[k], kde=True, hist=False, label=(labels[k] if count == k else None))
                count += 1
        # g = sns.FacetGrid(df, col=[*batch.values()], hue=[*batch.keys()], palette="Set1")
        #
        # g = (g.map(sns.distplot, , hist=False, rug=True))
        # plot = df.plot(kind=kind, legend=True, c=colors)
    # plt.xlim(-10000, 10000)
    # plt.xlim(df.values.min(), df.values.max()+1)
    plt.legend().remove()
    plt.tight_layout()
    return plot