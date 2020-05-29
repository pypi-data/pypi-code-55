import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import pandas as pd


def make_venn(df1, df2, df1_col, df2_col, pval, name1, name2,
              pval_cutoff=.01, as_percent=False):
    w_df = pd.merge(df1, df2, left_index=True, right_index=True)

    w_df = w_df.loc[[i < pval_cutoff for i in w_df.loc[:, pval+'_x']]]
    w_df = w_df.loc[[i < pval_cutoff for i in w_df.loc[:, pval + '_y']]]
    v1 = w_df.loc[[i > 0 for i in w_df.loc[:, df1_col]], [df1_col]]
    v2 = w_df.loc[[i > 0 for i in w_df.loc[:, df2_col]], [df2_col]]
    fig, ax = plt.subplots(1, 2)
    plt.sca(ax[0])

    if as_percent:
        set_a = set(v1.index.to_list())
        set_b = set(v2.index.to_list())
        total = len(set_a.union(set_b))
        up = list(set(v1.index.to_list() + v2.index.to_list()))
        ven1 = venn2([set(v1.index.to_list()), set(v2.index.to_list())],
                     set_labels=[name1, name2], subset_label_formatter=lambda x: f"{(x/total):1.0%}")
    else:
        up = list(set(v1.index.to_list() + v2.index.to_list()))
        ven1 = venn2([set(v1.index.to_list()), set(v2.index.to_list())],
                     set_labels=[name1, name2])
    plt.sca(ax[1])
    v3 = w_df.loc[[i < 0 for i in w_df.loc[:, df1_col]], [df1_col]]
    v4 = w_df.loc[[i < 0 for i in w_df.loc[:, df2_col]], [df2_col]]
    if as_percent:
        set_c = set(v3.index.to_list())
        set_d = set(v4.index.to_list())
        total = len(set_c.union(set_d))
        down = list(set(v3.index.to_list() + v4.index.to_list()))
        ven2 = venn2([set(v3.index.to_list()), set(v4.index.to_list())],
                     set_labels=[name1, name2], subset_label_formatter = lambda x: f"{(x / total):1.0%}")
    else:
        down = list(set(v3.index.to_list() + v4.index.to_list()))
        ven2 = venn2([set(v3.index.to_list()), set(v4.index.to_list())],
                     set_labels=[name1, name2])
    ax[0].set_title('Upregulated (p-value cutoff = {})'.format(pval_cutoff))
    ax[1].set_title('Downregulated (p-value cutoff = {})'.format(pval_cutoff))
    return fig, ax, up, down
