import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def read_count_bar(df: pd.DataFrame, cols: list, gene: str or list):
    """

    Args:
        df: dataframe containing genes, samples, and corresponding counts for each coordinate
            should be formatted with genes as index and samples as columns
        cols: a list of columns to include in the bar graph
        gene: the gene for which counts will be plotted

    Returns:

    """

    bar = sns.barplot(data=df, x=cols, y=gene, ci=None,
                    palette='rainbow')
    bar = format_bar(bar, gene)
    return bar


def format_bar(bar, gene):
    bar.set_xticklabels(labels=bar.get_xticklabels(), rotation=40)
    bar.set_title("Read counts {}".format(''.join([str(g) for g in gene])))
    plt.tight_layout()
    return bar
