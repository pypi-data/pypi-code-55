import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from IPython.display import display, Markdown
import transparentai

def plot_or_save(fname=None):
    """

    Parameters
    ----------
    fname: str
        file name where to save the plot
    """
    global __SAVEPLOT__
    if __SAVEPLOT__ is None:
        __SAVEPLOT__ = False
    
    if not __SAVEPLOT__:
        plt.show()
    else:
        fname = 'plot.png' if fname is None else fname
        plt.savefig(fname)

def plot_missing_values(df):
    """
    Show a bar plot that display percentage of missing values on columns that have some.
    If no missing value then it use `display` & `Markdown` functions to indicate it.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe to inspect
    """
    df_null = pd.DataFrame(len(df) - df.notnull().sum(), columns=['Count'])
    df_null = df_null[df_null['Count'] > 0].sort_values(
        by='Count', ascending=False)
    df_null = df_null/len(df)*100

    if len(df_null) == 0:
        display(Markdown('No missing value.'))
        return

    x = df_null.index.values
    height = [e[0] for e in df_null.values]

    fig, ax = plt.subplots(figsize=(20, 5))
    ax.bar(x, height, width=0.8)
    plt.xticks(x, x, rotation=30)
    plt.xlabel('Columns')
    plt.ylabel('Percentage')
    plt.title('Percentage of missing values in columns')

    plot_or_save(fname='missing_values.png')