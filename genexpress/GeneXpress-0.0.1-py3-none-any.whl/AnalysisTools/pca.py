from itertools import chain
from functools import reduce
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def calculate_principal_components(pca_df: pd.DataFrame):
    """PCA on a DataFrame or on a list of DataFrames.

        Perform PCA on several datasets to determine extent of batch effects or to compare global differences between
        datasets. A DataFrame containing samples to compare or a list of DataFrames (usually to compare between samples for
        batch effect) is passed. Data is standardized using the sklearn.preprocessing.StandardScaler class. (n/2)-1 components
        are calculated from standardized data. DataFrames passed should be formatted with experiments as columns and genes
        as rows.
        "The fit learns some quantities from the data, most importantly the "components" and "explained variance""
        "This transformation from data axes to principal axes is an affine transformation, which basically means it is composed of a translation, rotation, and uniform scaling."

    References: https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
                https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html
                http://www.marcottelab.org/users/BCH391L_2015/NBT_primer_PCA.pdf

    Args:
        pca_dfs: A DataFrame, or list of DataFrames containing gene expression data for PCA comparison.

    Returns: A DataFrame containing the first (n/2)-1 components

    """
    PCs = min(len(pca_df.columns.to_list()), len(pca_df.index.to_list()))
    vals = pca_df.columns.to_list()
    i = iter(vals)
    cols = dict(zip(range(len(vals)), i))
    pca_df.drop()
    # StandardScalar calculates z-score z = (x-mean)/std-dev
    scaled = StandardScaler().fit_transform(pca_df.transpose())
    pca = PCA(n_components=PCs)
    transformed_pcs = pca.fit_transform(scaled)
    final_df = pd.DataFrame(data=transformed_pcs, index=pca_df.columns, columns=["Principal Component {}".format(i+1) for i in range(PCs)])
    return final_df, cols, pca
