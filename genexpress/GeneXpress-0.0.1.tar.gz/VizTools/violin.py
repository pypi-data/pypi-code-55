import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
# The above palette is from https://gist.github.com/thriveth/8560036


def violin_plot(df, cols: dict, genes: [] or str = None):
    """Make a violin plot

    Makes a violin plot of all genes in df or genes defined by the parameter 'genes'.

    Args:
        df: DataFrame containing logFC and p-value. **Must** contain logfc and p-value data from one experiment
        genes: a list of genes
        cols:

    Returns:
        an instance of a violin plot
    """
    if genes is None:
        # sns.violinplot(y=cxcl10['CXCL10'], x='all', hue='State', data=cxcl10, split=True) must add all param for x
        plot = sns.violinplot(y="CXCL10", data=df, orient='v', palette="Set2",
                              title="Gene Expression of {} in Canine DLE Samples", split=True,
                              scale="count", inner="quartile", hue='State')
        plt.xlabel("Healthy")
        plt.ylabel('{} Expression (log2 Fold Change)'.format(genes))
        return plot
    elif len(genes) == 1 or isinstance(genes, str):
        if isinstance(genes, list):
            plot = sns.violinplot(y=df.loc[genes[0]], orient='v',
                                   color='#377eb8')
            plt.title = "Gene Expression of {} in Canine DLE Samples".format(genes[0])
            plt.xlabel("Healthy")
            plt.ylabel('{} Expression'.format(genes[0]))
            plt.tight_layout()
            # plt.ylim(ymin=0)
        else:
            gene = df.loc[genes]

            plot = sns.violinplot(y=df.loc[genes], orient='v',
                                  title="Gene Expression of {} in Canine DLE Samples".format(genes),
                                  scale="count", inner="quartile")
            plt.xlabel(genes)
            plt.ylabel('Expression (log2 Fold Change)')


        return plot
    else:
        # to_plot = df.loc[genes] # this makes one plot out of the list of genes
        plots = list()
        plots.append([sns.violinplot(y=df.loc[i], orient='v') for i in genes]) #this overlays plots on same canvas
        return plots
