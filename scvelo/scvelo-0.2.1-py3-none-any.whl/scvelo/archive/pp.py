from .logg import print_logg
import numpy as np
from sklearn.svm import SVR
from scanpy.api.pp import *


def normalize_per_cell(adata, counts_per_cell_after=None, use_Xs=False, copy=False):
    n_counts = adata.X.sum(1)
    adata.X = adata.X / n_counts[:, None] * np.median(n_counts)

    cell_size_s = adata.obsm['Xs'].sum(1)  # = adata.uns['Xs'].A.sum(1)
    cell_size_u = adata.obsm['Xu'].sum(1)  # = adata.uns['Xu'].A.sum(1)
    cell_subset = (cell_size_s > 0) & (cell_size_u > 0)
    if not all(cell_subset):
        filter_cells(adata, cell_subset)
    if counts_per_cell_after is None:
        target_s = np.median(cell_size_s[cell_subset])
        target_u = np.median(cell_size_u[cell_subset]) if not use_Xs else target_s
    else:
        target_s = target_u = counts_per_cell_after

    adata.obsm['Xs'] = adata.obsm['Xs'] / cell_size_s[:, None][cell_subset] * target_s
    adata.obsm['Xu'] = adata.obsm['Xu'] / cell_size_u[:, None][cell_subset] * target_u
    return adata if copy else None


def filter_cells(adata, cell_subset, copy=False):
    """Filter cells using a boolean array.

    Parameters
    ---------
    cell_subset: boolean np.ndarray
        describes the cells to keep (True).

    Return
    ------
    Updates the attributes .X, .obs, .obsm
    """
    adata._inplace_subset_obs(cell_subset)
    if 'loom_obs' in adata.uns_keys():
        adata.uns['loom_obs'] = {k: v[cell_subset] for k, v in adata.uns['loom_obs'].items()}
    return adata if copy else None


def filter_genes(adata, gene_subset, copy=False):
    """Filter genes using a boolean array.

    Arguments
    ---------
    gene_subset: boolean np.ndarray
        describes the genes to keep (True).

    Return
    ------
    Updates the attributes .X, .var, .obsm['Xs'], .obsm['Xs']
    """
    adata._inplace_subset_var(gene_subset)
    adata.obsm['Xs'] = adata.obsm['Xs'][:, gene_subset]
    adata.obsm['Xu'] = adata.obsm['Xu'][:, gene_subset]

    if 'loom_var' in adata.uns_keys():
        adata.uns['loom_var'] = {k: v[gene_subset] for k, v in adata.uns['loom_var'].items()}

    for key in adata.obsm_keys():
        if (key in ['Ms', 'Mu']) or ('velocity' in key):
            adata.obsm[key] = adata.obsm[key][:, gene_subset]

    for key in adata.uns_keys():
        if 'pars' in key:
            for par in adata.uns[key]:
                adata.uns[key][par] = adata.uns[key][par][gene_subset]

    return adata if copy else None


def filter_genes_detection(adata, min_counts_s=30, min_cells_s=20, min_counts_u=20, min_cells_u=10, copy=False):
    """Filter genes outliers based on counts and numbers of cells detected.

    Arguments
    ---------
    min_counts_s: int
        filter genes by the minimum counts of spliced molecules detected

    min_cells_s: int
        filter genes by the minimum numbers of spliced molecules detected

    min_counts_u: int
        filter genes by the minimum counts of unspliced molecules detected

    min_cells_u: int
        filter genes by the minimum number of unspliced molecules detected

    normalize: bool, default=True
        whether to normalize the count matrices

    Returns
    -------
    Updates the attributes .X, .var, .obsm['Xs'], .obsm['Xs']
    """
    # if min_counts_s is None: min_counts_s = np.clip(adata.n_obs / 100, 20, 100)
    # if min_counts_u is None: min_counts_u = int(min_counts_s / 2)
    # if min_cells_s is None: min_cells_s = int(min_counts_s / 2)
    # if min_cells_u is None: min_cells_u = int(min_counts_u / 2)

    gene_subset = (adata.obsm['Xs'].sum(0) >= min_counts_s) & ((adata.obsm['Xs'] > 0).sum(0) >= min_cells_s) & \
                 (adata.obsm['Xu'].sum(0) >= min_counts_u) & ((adata.obsm['Xu'] > 0).sum(0) >= min_cells_u)
    filter_genes(adata, gene_subset)

    adata.X = adata.obsm['Xs']

    print_logg('Filtered genes based on counts and number of cells detected (' + str(adata.obsm['Xs'].shape[1]) + ')')

    return adata if copy else None


def cv_vs_mean(adata, n_genes):
    """Rank genes on the basis of a CV vs mean fit via support vector regression (SVR)

    Arguments
    ---------
    n_genes: int
        the number of genes to select

    Returns
    -------
    gene_subset: boolean np.ndarray
        describes the genes to keep (True)

    Note: To perform the filtering use the method `filter_genes`
    """
    mu, sigma = adata.obsm['Xs'].mean(0), adata.obsm['Xs'].std(0, ddof=1)
    cv = sigma / mu

    log_m, log_cv = np.log2(mu), np.log2(cv)

    # Fit the Support Vector Regression
    svr_gamma = 150. / len(mu)
    clf = SVR(gamma=svr_gamma)
    clf.fit(log_m[:, None], log_cv)
    log_cv_fit = clf.predict(log_m[:, None])
    score = log_cv - log_cv_fit

    n_genes = min(n_genes, adata.obsm['Xs'].shape[1])
    nth_score = np.sort(score)[::-1][n_genes-1]
    gene_subset = score >= nth_score

    return gene_subset


def filter_genes_dispersion(adata, n_genes=3000, copy=False):
    """Filter genes outliers based on counts and numbers of cells detected.

    Arguments
    ---------
    n_genes: int
        the number of genes to select

    normalize: bool, default=True
        whether to renormalize (by median / size) the expression matrices
        after filtering out highly variable genes

    Returns
    -------
    Updates the attributes .X, .var, .obsm['Xs'], .obsm['Xs']
    """
    if n_genes < adata.obsm['Xs'].shape[1]:
        gene_subset = cv_vs_mean(adata, n_genes)
        filter_genes(adata, gene_subset)
        print_logg('Extracted highly variable genes (' + str(adata.obsm['Xs'].shape[1]) + ')')

    return adata if copy else None
