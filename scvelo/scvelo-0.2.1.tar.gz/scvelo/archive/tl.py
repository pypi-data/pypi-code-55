"""Estimation and Analysis of Stochastic RNA Velocity & Diffusion Velocity

Main tools:
-----------
tl.velocity
    - calculates first (and second) order moments for each cells across nearest neighbors
    - estimates velocity from relationship of precursor (unspliced) and mature (spliced) mRNA.
    - use tl.filter_genes_velocity to select genes with high-quality fit.

tl.velocity_graph
    - computes likely cell transitions based on cosine similarity with velocity vector

tl.velocity_embedding
    - compute embedded velocity vetors using cell transitions from velocity graph
"""

from .logg import print_logg
from .pp import filter_genes

import pandas as pd
import numpy as np

from scipy.optimize import minimize
from scipy.stats import norm as normal
from scipy.sparse import csr_matrix, coo_matrix

from matplotlib.colors import rgb2hex
import matplotlib.pyplot as pl

from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

from scanpy.api import Neighbors
from scanpy.api.tl import *

from scanpy import settings
from scanpy import logging as logg

from anndata import AnnData

from typing import Any

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


"""
Helper functions for velocity estimation
----------------------------------------
"""


def norm(A):
    """computes the L2-norm along axis 1 (e.g. genes or embedding dimensions)
    """
    return np.sqrt(np.einsum('ij, ij -> i', A, A))


def prod(A, B, axis=0):
    """computes the dot product and sums over axis 0 (cells) or axis 1 (genes)
    """
    if axis == 0:
        return np.einsum('ij, ij -> j', A, B)
    else:
        return np.einsum('ij, ij -> i', A, B)


def pca(adata, lb=10, ub=100, n_pcs=None, pca_plot=False, copy=False):
    """Performs a Principal Component Analysis (PCA)
    with numbers of principal components based on a variance ratio threshold

    Arguments
    ---------
    lb: int
        lower bound for number of principal components to be used

    ub: int
        upper bound for number of principal components to be used

    n_pcs: int, default=None
        if not None, specific number of principal components to be used

    pca_plot: bool, default=False
        whether to plot the ratio of explained variance per number of principal components

    Returns
    -------
    Creates the attributes .obsm['X_pca']
    """
    n_components = min(ub, adata.X.shape[0])
    pca = PCA(n_components=n_components)
    adata.obsm['X_pca'] = pca.fit_transform(adata.X)
    if n_pcs is None:
        try:
            n_pcs = np.clip(np.where(np.diff(np.diff(np.cumsum(pca.explained_variance_ratio_))>0.002))[0][0], lb, ub)
        except Exception:
            n_pcs = n_components

    print_logg('Performed PCA (' + str(n_pcs) + ' PCs explain '
               + str(round(np.cumsum(pca.explained_variance_ratio_)[n_pcs - 1], 2))
               + ' of variation and will be used for velocity estimation)')

    adata.obsm['X_pca'] = adata.obsm['X_pca'][:, :n_pcs]

    if pca_plot:
        pl.plot(np.cumsum(pca.explained_variance_ratio_)[:100])
        pl.axvline(n_pcs, c="k")

    return adata if copy else None


def velocity_neighbors(adata: AnnData, n_neighbors: int=100, n_pcs: int=10, use_rep: str='X_pca', random_state: int=0,
                       knn: bool=True, method: str='umap', metric: str='euclidean', metric_kwds: Any={}, copy: bool=False):
    logg.info('computing neighbors', r=True)
    adata = adata.copy() if copy else adata
    neighbors = Neighbors(adata)

    neighbors.compute_neighbors(
        n_neighbors=n_neighbors, knn=knn, n_pcs=n_pcs, use_rep=use_rep,
        method=method, metric=metric, metric_kwds=metric_kwds,
        random_state=random_state, write_knn_indices=True)

    adata.uns['velocity_neighbors'] = {}
    adata.uns['velocity_neighbors']['params'] = {'n_neighbors': n_neighbors, 'method': method}
    adata.uns['velocity_neighbors']['distances'] = neighbors.distances
    adata.uns['velocity_neighbors']['connectivities'] = neighbors.connectivities
    logg.info('    finished', time=True, end=' ' if settings.verbosity > 2 else '\n')
    logg.hint(
        'added to `.uns[\'velocity_neighbors\']`\n'
        '    \'distances\', weighted adjacency matrix\n'
        '    \'connectivities\', weighted adjacency matrix')

    return adata if copy else None


def neighbors(adata, n_neighbors=None, for_moments=False, use_pca=True, n_pcs=None, random_fraction=1, copy=False):
    """Computes a k-nearest-neighbors (knn) graph

    Arguments
    ---------
    n_neighbors: int
        number of neighbors to be used for knn graph

    mode: str, default='distance'
        mode of knn graph

    Returns
    -------
    knn_graph: knn graph
    """
    if use_pca:
        if 'X_pca' not in adata.obsm.keys(): pca(adata, n_pcs=n_pcs)
        use_rep = 'X_pca'
    else:
        use_rep = 'X'

    if 'velocity_neighbors' not in adata.uns_keys():
        adata.uns['velocity_neighbors'] = dict()

    n_obs = adata.X.shape[0]

    if n_neighbors is None:
        n_neighbors = int(n_obs / 50) if for_moments else int(n_obs / 20)

    neighs = Neighbors(adata)

    if for_moments:
        if 'moments' not in adata.uns['velocity_neighbors']:
            adata.uns['velocity_neighbors']['moments'] = dict()
            adata.uns['velocity_neighbors']['moments']['n_neighbors'] = 0
        if adata.uns['velocity_neighbors']['moments']['n_neighbors'] < n_neighbors:
            neighs.compute_neighbors(n_neighbors=n_neighbors, use_rep=use_rep,
                                     n_pcs=n_pcs, write_knn_indices=True)
            adjacency = neighs.distances > 0
            adjacency.setdiag(1)

            adata.uns['velocity_neighbors']['moments']['adjacency'] = adjacency
            adata.uns['velocity_neighbors']['moments']['indices'] = neighs.knn_indices
            adata.uns['velocity_neighbors']['moments']['n_neighbors'] = n_neighbors
            adata.uns['velocity_neighbors']['moments']['n_pcs'] = n_pcs

            print_logg('Updated \'{}\' in .uns'.format('velocity_neighbors'))

    else:
        if 'vgraph' not in adata.uns['velocity_neighbors']:
            adata.uns['velocity_neighbors']['vgraph'] = dict()
            adata.uns['velocity_neighbors']['vgraph']['n_neighbors'] = 0
        if adata.uns['velocity_neighbors']['vgraph']['n_neighbors'] < int(random_fraction * (n_neighbors + 1)):
            neighs.compute_neighbors(n_neighbors=n_neighbors+1, use_rep=use_rep, n_pcs=n_pcs, write_knn_indices=True)
            adjacency = neighs.distances > 0
            adjacency.setdiag(0)
            indices = neighs.knn_indices[:, 1:]

            if random_fraction < 1:
                np.random.seed(27)
                p = np.linspace(5, 1, n_neighbors)
                p /= p.sum()
                size = int(random_fraction * (n_neighbors + 1))
                sample_ixs = np.vstack((np.random.choice(n_neighbors, size=size, replace=False, p=p) for _ in range(n_obs)))
                indices = indices[np.arange(n_obs)[:, None], sample_ixs]

                n_obs, n_neighbors = indices.shape
                vals, indptr = np.ones(n_obs * n_neighbors), np.arange(0, n_obs * n_neighbors + 1, n_neighbors)
                adjacency = csr_matrix((vals, indices.ravel(), indptr), shape=(n_obs, n_obs))
                adata.uns['velocity_neighbors']['vgraph']['random_fraction'] = random_fraction

            adata.uns['velocity_neighbors']['vgraph']['adjacency'] = adjacency
            adata.uns['velocity_neighbors']['vgraph']['indices'] = indices
            adata.uns['velocity_neighbors']['vgraph']['n_neighbors'] = n_neighbors
            adata.uns['velocity_neighbors']['vgraph']['n_pcs'] = n_pcs

            print_logg('Updated \'{}\' in .uns'.format('velocity_neighbors'))

    return adata if copy else None


"""
Deterministic and Stochastic RNA Velocity estimation
---------
"""


def moments(adata, n_neighbors=None, use_pca=True, renormalize=False, copy=False):
    """Computes first order moments for velocity estimation

    Arguments
    ---------
    n_neighbors: int
        number of neighbors to be used for computing moments

    Returns
    -------
    Creates attributes .layers['Ms'], .layers['Mu']
    """
    neighbors(adata, n_neighbors=n_neighbors, for_moments=True, use_pca=use_pca)
    knn = adata.uns['velocity_neighbors']['moments']['adjacency']
    knn_weights = knn.multiply(1. / knn[0].sum())

    adata.layers['Ms'] = csr_matrix.dot(knn_weights, adata.layers['spliced'])
    adata.layers['Mu'] = csr_matrix.dot(knn_weights, adata.layers['unspliced'])

    if renormalize:
        adata.layers['Ms'] = adata.layers['Ms'] / adata.layers['Ms'].sum(1)[:, None] * np.median(adata.layers['Ms'].sum(1))
        adata.layers['Mu'] = adata.layers['Mu'] / adata.layers['Mu'].sum(1)[:, None] * np.median(adata.layers['Mu'].sum(1))

    return adata if copy else None


def second_order_moments(adata, n_neighbors=None, use_pca=True):
    """Computes first order moments for velocity estimation

    Arguments
    ---------
    n_neighbors: int
        number of neighbors to be used for computing moments

    Returns
    -------
    Creates attributes .layers['Ms'], .layers['Mu'], .layers['Muu'], .layers['Mus'], .layers['Mss']
    """
    neighbors(adata, n_neighbors=n_neighbors, for_moments=True, use_pca=use_pca)
    knn = adata.uns['velocity_neighbors']['moments']['adjacency']
    knn_weights = knn.multiply(1. / knn[0].sum())
    Mss = csr_matrix.dot(knn_weights, adata.layers['spliced']**2)
    Mus = csr_matrix.dot(knn_weights, adata.layers['unspliced'] * adata.layers['spliced'])
    return Mss, Mus


def second_order_moments_u(adata, n_neighbors=None, use_pca=True):
    """Computes first order moments for velocity estimation

    Arguments
    ---------
    n_neighbors: int
        number of neighbors to be used for computing moments

    Returns
    -------
    Creates attributes .layers['Ms'], .layers['Mu'], .layers['Muu'], .layers['Mus'], .layers['Mss']
    """
    neighbors(adata, n_neighbors=n_neighbors, for_moments=True, use_pca=use_pca)
    knn = adata.uns['velocity_neighbors']['moments']['adjacency']
    knn_weights = knn.multiply(1. / knn[0].sum())
    Muu = csr_matrix.dot(knn_weights, adata.layers['unspliced']**2)
    return Muu


def ls_solver(x, y, fit_offset=False):
    n_obs, n_var = x.shape
    if fit_offset:
        cov_xy, cov_xx = prod(x, y) / n_obs, prod(x, x) / n_obs
        mean_x, mean_y = x.mean(0), y.mean(0)
        numerator_offset = cov_xx * mean_y - cov_xy * mean_x
        numerator_gamma = cov_xy - mean_x * mean_y
        offset, gamma = (numerator_offset, numerator_gamma) / (cov_xx - mean_x * mean_x)
    else:
        offset, gamma = np.zeros(n_var), prod(x, y) / prod(x, x)
    return offset, gamma


def ls_solver1(x, y, fit_offset=False):
    n_obs, n_var = x.shape
    offset, gamma = np.zeros(n_var, dtype="float32"), np.ones(n_var, dtype="float32")
    if fit_offset:
        offset_vectors = np.ones(n_obs)
        for i in range(n_var):
            A = np.c_[offset_vectors, x[:, i]]
            offset[i], gamma[i] = np.linalg.pinv(A.T.dot(A)).dot(A.T.dot(y[:, i]))
    else:
        for i in range(n_var):
            A = x[:, i]
            gamma[i] = np.linalg.pinv(A.T.dot(A)).dot(A.T.dot(y[:, i]))
    return offset, gamma


def ls_solver2(x, y, x2, y2, res_std=None, res2_std=None, fit_offset=False, fit_offset2=False):
    n_obs, n_var = x.shape
    offset, offset_ss = np.zeros(n_var, dtype="float32"), np.zeros(n_var, dtype="float32")
    gamma = np.ones(n_var, dtype="float32")

    if (res_std is None) or (res2_std is None): res_std, res2_std = np.ones(n_var), np.ones(n_var)
    ones, zeros = np.ones(n_obs), np.zeros(n_obs)
    x, y = np.vstack((x/res_std, x2/res2_std)), np.vstack((y/res_std, y2/res2_std))

    if fit_offset and fit_offset2:
        for i in range(n_var):
            A = np.c_[np.vstack((np.c_[ones/res_std[i], zeros], np.c_[zeros, ones/res2_std[i]])), x[:, i]]
            offset[i], offset_ss[i], gamma[i] = np.linalg.pinv(A.T.dot(A)).dot(A.T.dot(y[:, i]))
    elif fit_offset:
        for i in range(n_var):
            A = np.c_[np.hstack((ones/res_std[i], zeros)), x[:, i]]
            offset[i], gamma[i] = np.linalg.pinv(A.T.dot(A)).dot(A.T.dot(y[:, i]))
    elif fit_offset2:
        for i in range(n_var):
            A = np.c_[np.hstack((zeros, ones/res2_std[i])), x[:, i]]
            offset_ss[i], gamma[i] = np.linalg.pinv(A.T.dot(A)).dot(A.T.dot(y[:, i]))
    else:
        for i in range(n_var):
            A = np.c_[x[:, i]]
            gamma[i] = np.linalg.pinv(A.T.dot(A)).dot(A.T.dot(y[:, i]))

    return offset, offset_ss, gamma


def opt_solver2(Ms, Mu, Mus, Mss, fit_offset=False, fit_offset2=False):
    # maximize likelihood using weights according to empirical bayes
    n_obs, n_var = Ms.shape
    offset, offset_ss = np.zeros(n_var, dtype="float32"), np.zeros(n_var, dtype="float32")
    gamma = np.ones(n_var, dtype="float32")

    def sse(A, data, b):
        sigma = (A.dot(data) - b).std(1)
        return np.log(sigma).sum()  # np.log(np.sqrt(2*np.pi) * sigma).sum() + (.5 * (res/sigma[:, None])**2).sum()

    if fit_offset and fit_offset2:
        for i in range(n_var):
            data = np.vstack((Mu[:, i], Ms[:, i], Mus[:, i], Mss[:, i]))
            offset[i], offset_ss[i], gamma[i] = \
                minimize(lambda m: sse(np.array([[1, -m[2], 0, 0], [1, m[2], 2, -2 * m[2]]]),
                                       data, b=np.array(m[0], m[1])), x0=(1e-4, 1e-4, 1), method="L-BFGS-B").x
    elif fit_offset:
        for i in range(n_var):
            data = np.vstack((Mu[:, i], Ms[:, i], Mus[:, i], Mss[:, i]))
            offset[i], gamma[i] = \
                minimize(lambda m: sse(np.array([[1, -m[1], 0, 0], [1, m[1], 2, -2 * m[1]]]),
                                       data, b=np.array(m[0], 0)), x0=(1e-4, 1), method="L-BFGS-B").x
    elif fit_offset2:
        for i in range(n_var):
            data = np.vstack((Mu[:, i], Ms[:, i], Mus[:, i], Mss[:, i]))
            offset_ss[i], gamma[i] = \
                minimize(lambda m: sse(np.array([[1, -m[1], 0, 0], [1, m[1], 2, -2 * m[1]]]),
                                       data, b=np.array(0, m[0])), x0=(1e-4, 1), method="L-BFGS-B").x
    else:
        for i in range(n_var):
            data = np.vstack((Mu[:, i], Ms[:, i], Mus[:, i], Mss[:, i]))
            gamma[i] = \
                minimize(lambda m: sse(np.array([[1, -m, 0, 0], [1, m, 2, -2 * m]]), data, b=0),
                         x0=gamma[i], method="L-BFGS-B").x
    return offset, offset_ss, gamma


def velocity(adata, vkey='velocity', second_order=False, bayes=False, estimate_alpha=False,
             fit_offset=False, fit_offset2=True, n_neighbors=None, use_pca=True, copy=False):
    """Estimates steady-states and velocities in a gene-specific manner

    Arguments
    ---------
    fit_offset: bool, default=True
        whether to fit with offset (accounting for ambiguous reads)

    fit_on_percentiles: bool, default=False (this is not implemented yet)
        whether to fit on lower and upper percentiles only

    fit_with_bounds: bool, default=False
        whether to set lower and upper boundaries for offset and gamma

    Returns
    -------
    Creates attributes .var['offset'], .var['gamma'], .var['r2'], .layers['velocity']
    """
    if 'Ms' not in adata.layers.keys():
        moments(adata)
    Ms, Mu = adata.layers['Ms'], adata.layers['Mu']
    n_obs, n_var = Ms.shape
    beta = np.ones(n_var, dtype="float32")  # estimate all rates in units of the splicing rate

    o_s, gamma = ls_solver(Ms, Mu, fit_offset)
    pars, pars_str = [o_s, beta, gamma], ['o_s', 'beta', 'gamma']

    if second_order or bayes:
        Mss, Mus = second_order_moments(adata, n_neighbors, use_pca)
        o_ss, gamma = ls_solver(2*Mss-Ms, 2*Mus+Mu, fit_offset2)

        res_std = (Mu - gamma[None, :] * Ms - o_s[None, :]).std(0)
        res2_std = (2*Mus+Mu - gamma[None, :] * (2*Mss-Ms) - o_s[None, :]).std(0)

        if second_order: o_s, o_ss, gamma = \
            ls_solver2(Ms, Mu, 2*Mss-Ms, 2*Mus+Mu, res_std, res2_std, fit_offset, fit_offset2)
        else: o_s, o_ss, gamma = \
            opt_solver2(Ms, Mu, Mus, Mss, fit_offset, fit_offset2)

        adata.layers['diffusion_velocity'] = \
            beta[None, :] * (2*Mus-2*Ms*Mu+Mu) - gamma[None, :]*(2*Mss-2*Ms**2-Ms) - o_ss[None, :]+2*o_s[None, :]*Ms
        pars, pars_str = [beta, gamma, o_s, o_ss], ['beta', 'gamma', 'o_s', 'o_ss']

    if estimate_alpha:
        Muu = second_order_moments_u(adata, n_neighbors, use_pca)
        o_uu, alpha = ls_solver(np.ones(Mu.shape) + 2 * Mu, 2 * Muu - Mu)
        pars.extend([o_uu, alpha])
        pars_str.extend(['o_uu', 'alpha'])

    res, tot = Mu - gamma[None, :] * Ms - o_s[None, :], Mu - Mu.mean(0)
    r2 = np.ones(n_var) - prod(res, res) / prod(tot, tot)

    pars.extend([r2])
    pars_str.extend(['r2'])

    adata.uns[vkey + '_pars'] = dict()
    for i, par in enumerate(pars_str): adata.uns[vkey + '_pars'][par] = pars[i]

    adata.layers[vkey] = res
    print_logg('Added \'{}\' to .layers (velocity = beta Mu - gamma Ms - offset)'.format(vkey))

    return adata if copy else None


def filter_genes_velocity(adata, vkey='velocity', min_r2=0.01, min_gamma=0.01, copy=False):
    """Filter genes based on minimum level of r2 and gamma

    Arguments
    ---------
    min_r2: float
        minimum r2 level

    min_gamma: float
        minimum gama level

    Returns
    -------
    Updates attributes .X, .var, .layers['spliced'], .layers['unspliced'], .layers['Ms'], .layers['Mu'], .layers['velocity']
    """
    r2_filter = adata.uns[vkey+'_pars']['r2'] > min_r2
    gamma_filter = adata.uns[vkey+'_pars']['gamma'] > min_gamma

    gene_subset = list(r2_filter & gamma_filter)

    if not all(gene_subset):
        filter_genes(adata, gene_subset)
        print_logg('Filtered genes based on quality of steady-state fit ({} genes passed criteria)'.format(adata.n_vars))
        print('Excluded ' + str(len(r2_filter)-r2_filter.sum()) + ' genes due to low r2 and '
              + str(len(gamma_filter)-gamma_filter.sum()) + ' genes due to negative correlation')
    else:
        print('No genes would pass the filter. Try adjusting the criteria.')

    return adata if copy else None


"""
Velocity graph (cosine correlations and transition matrix)
---------
"""


# class CosineCorrelation:
#
#     def __init__(self, var_transform=False):
#         self.var_transform = var_transform
#
#     def linear(self, i):
#         dX = adata.obsm['Ms'][adata.uns['velocity_neighbors']['vgraph']['indices'][i]] - adata.obsm['Ms'][i, None]
#         Vi = adata.obsm['V_norm'][i]
#         if self.var_transform:
#             dX = np.sqrt(np.abs(dX)) * np.sign(dX)
#         dX -= dX.mean(1)[:, None]
#         with warnings.catch_warnings():
#             warnings.simplefilter("ignore")
#             vals = np.dot(dX, Vi) / (norm(dX) * norm(Vi))[None, :]
#         return vals

# class CosineCorrelation:
#
#     def __init__(self, X, V, knn_ixs, var_transform=False):
#         self.X = X
#         self.knn_ixs = knn_ixs
#         self.var_transform = var_transform
#
#         if var_transform:
#             V = np.sqrt(np.abs(V)) * np.sign(V)
#         self.V = V - V.mean(1)[:, None]
#         self.V_norm = norm(self.V)
#
#     def compute(self, i):
#         dX = self.X[self.knn_ixs[i]] - self.X[i, None]
#         if self.var_transform:
#             dX = np.sqrt(np.abs(dX)) * np.sign(dX)
#         dX -= dX.mean(1)[:, None]
#         with warnings.catch_warnings():
#             warnings.simplefilter("ignore")
#             vals = np.dot(dX, self.V[i]) / (norm(dX) * self.V_norm[i])[None, :]
#         return vals


def _cosines_multicore(dX, Vi):
    return np.einsum('ij, j', dX, Vi) / (norm(dX) * norm(Vi))[None, :]


def velocity_graph(adata, vkey='velocity', n_neighbors=None, n_pcs=None,
                   random_fraction=1, sqrt_transform=False, n_jobs=1, multicore=False, copy=False):
    """Computes a velocity graph based on cosine similarities between velocities and cell state transitions

    Arguments
    ---------
    Xs: np.ndarray
        Data matrix to be used; moments .layers['Ms'] per default

    Xv: np.ndarray
        Velocity matrix to be used; standard non-transformed .layers['velocity'] per default

    n_neighbors: int
        number of neighbors to be used for knn graph

    knn_random_frac: float
        fraction of random samples to be used for knn graph

    var_transform: bool, default=False
        whether to variance-transform the cell states and velocities before computing cosine similarities

    Returns
    -------
    Creates sparse graph .uns['velocity_graph']
    """
    if vkey not in adata.layers.keys():
        velocity(adata)
    X, V = adata.layers['Ms'].copy(), adata.layers[vkey].copy()

    if ('velocity_neighbors' not in adata.uns_keys()) or \
            ('vgraph' not in adata.uns['velocity_neighbors']) or (n_neighbors is not None):
        neighbors(adata, n_neighbors, use_pca=True, n_pcs=n_pcs, random_fraction=random_fraction)
    knn_ixs = adata.uns['velocity_neighbors']['vgraph']['indices']
    n_obs, n_neighbors = knn_ixs.shape

    if sqrt_transform: V = np.sqrt(np.abs(V)) * np.sign(V)
    V -= V.mean(1)[:, None]
    V_norm = norm(V)

    def cosines_linear(i):
        dX = X[knn_ixs[i]] - X[i, None]
        dX -= dX.mean(1)[:, None]
        return np.einsum('ij, j',  dX, V[i]) / (norm(dX) * V_norm[i])[None, :]

    def cosines_sqrt(i):
        dX = X[knn_ixs[i]] - X[i, None]
        dX = np.sqrt(np.abs(dX)) * np.sign(dX)
        dX -= dX.mean(1)[:, None]
        return np.einsum('ij, j', dX, V[i]) / (norm(dX) * V_norm[i])[None, :]

    # corr = CosineCorrelation(var_transform)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        vals = []
        if sqrt_transform:
            for i in range(n_obs): vals.append(cosines_sqrt(i))
        elif multicore:
            from multiprocessing import Pool
            p = Pool(n_jobs)
            vals = p.apply_async() #p.map(_cosines_multicore, range(n_obs))
        else:
            for i in range(n_obs): vals.append(cosines_linear(i))

        #
        # p = Pool(n_jobs)
        # vals = p.map(corr.compute, range(n_obs))

    vals = np.hstack(vals)[0]

    vals[np.isnan(vals)] = 0
    vals = np.clip(vals, 0, 1)

    rows = np.hstack(np.array(range(n_obs))[:, None].dot(np.ones(n_neighbors, dtype=int)[None, :]))
    cols = np.hstack(knn_ixs)

    graph = coo_matrix((vals, (rows, cols)), shape=(n_obs, n_obs))
    graph.eliminate_zeros()

    adata.uns[vkey+'_graph'] = graph.tocsr()
    print_logg('Added sparse velocity graph \'{}\' to .uns'.format(vkey+'_graph'))

    return adata if copy else None


# def chunk_multicore():
#     tasks = []
#     # split the adata.X matrix by columns in chunks of size n_chunk (the last chunk could be of smaller
#     # size than the others)
#     chunk_list = np.array_split(adata.X, n_chunks, axis=1)
#     if variable_is_categorical:
#         regressors_chunk = np.array_split(regressors, n_chunks, axis=1)
#     for idx, data_chunk in enumerate(chunk_list):
#         # each task is a tuple of a data_chunk eg. (adata.X[:,0:100]) and
#         # the regressors. This data will be passed to each of the jobs.
#         if variable_is_categorical:
#             regres = regressors_chunk[idx]
#         else:
#             regres = regressors
#         tasks.append(tuple((data_chunk, regres, variable_is_categorical)))
#
#     if n_jobs > 1 and n_chunks > 1:
#         import multiprocessing
#         pool = multiprocessing.Pool(n_jobs)
#         res = pool.map_async(_regress_out_chunk, tasks).get(9999999)
#         pool.close()
#
#     else:
#         res = list(map(_regress_out_chunk, tasks))

def transition_matrix(adata, vkey='velocity', scale=10):
    """Computes a transition probabilities as Gaussian kernel of cosine similarities x scale

    Arguments
    ---------
    scale: float
        scale parameter of gaussian kernel

    Returns
    -------
    Creates sparse transition matrix .uns['velocity_transitions']
    """
    if vkey+'_graph' not in adata.uns_keys():
        velocity_graph(adata, vkey)
    knn = adata.uns['velocity_neighbors']['vgraph']['adjacency']

    T = np.expm1(csr_matrix.multiply(knn, adata.uns[vkey + '_graph']) * scale)  # + knn
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        T = T.multiply(1. / csr_matrix.sum(T, axis=1))

    return T


def score_transition(adata, vkey='velocity', scale=10, copy=False):
    # compute velocity score as in correlation of mean transition with velocity
    if vkey not in adata.layers.keys():
        velocity(adata, vkey)
    dX = transition_matrix(adata, vkey, scale).dot(adata.layers['Ms']) - adata.layers['Ms']
    V = adata.layers[vkey].copy()
    dX -= dX.mean(1)[:, None]
    V -= V.mean(1)[:, None]
    adata.obs[vkey+'_score_transition'] = prod(dX, V, axis=1) / (norm(dX) * norm(V))

    print_logg('Added \'{}\' to .obs'.format(vkey+'_score_transition'))
    return adata if copy else None


def score_smoothness(adata, vkey='velocity', n_neighbors=10, copy=False):
    if vkey not in adata.layers.keys():
        velocity(adata, vkey)
    X, V = adata.layers['Ms'].copy(), adata.layers[vkey].copy()

    knn_ixs = adata.uns['velocity_neighbors']['moments']['indices'][:, :n_neighbors]
    n_obs, n_neighbors = knn_ixs.shape

    V -= V.mean(1)[:, None]
    V_norm = norm(V)
    R = np.zeros(shape=(n_obs, n_neighbors))

    for i in range(n_obs):
        Vi_neighs = V[knn_ixs[i]]
        Vi_neighs -= Vi_neighs.mean(1)[:, None]
        R[i] = np.einsum('ij, j', Vi_neighs, V[i]) / (norm(Vi_neighs) * V_norm[i])[None, :]

    # V -= V.mean(0)
    # R = np.zeros(shape=(n_obs, n_neighbors))
    #
    # for i in range(n_obs):
    #     Vi_neighs = V[knn_ixs[i]]
    #     Vi_neighs -= Vi_neighs.mean(1)[:, None]
    #     ssS, ssV = [(Vi_neighs ** 2).sum(1), (V[i] ** 2).sum()]
    #     R[i] = np.dot(Vi_neighs, V[i]) / (np.sqrt(ssS) * np.sqrt(ssV))

    adata.obs[vkey + '_score_smoothness'] = R.mean(1)

    print_logg('Added \'{}\' to .obs'.format(vkey + '_score_smoothness'))
    return adata if copy else None


"""
Prepare embedding
---------
"""


def set_clusters_colors(adata, ckey='clusters'):
    colormap = np.vstack((pl.cm.tab20b(np.linspace(0., 1, 20))[::2], pl.cm.tab20c(np.linspace(0, 1, 20))[1::2],
                          pl.cm.tab20b(np.linspace(0., 1, 20))[1::2], pl.cm.tab20c(np.linspace(0, 1, 20))[0::2]))
    if ckey in adata.obs_keys():
        adata.uns[ckey + '_colors'] = [rgb2hex(c) for c in colormap[:len(adata.obs[ckey])]]
    else:
        print('could not find ' + ckey + ' in .obs')


def set_clusters(adata, clusters=None, clusters_colors=None, colormap=None, copy=False):
    """Sets clusters

    Arguments
    ---------
    clusters: np.array
        array of clusters (size: n_obs)

    clusters_colors: np.array
        array of clusters_colors (size: n_clusters)

    colormap: np.array
        array of colors to be used for clusters (size: n_clusters)

    Returns
    -------
    Creates attributes .var['clusters'], .uns['clusters_colors']
    """
    if (clusters is not None) and (len(clusters) == adata.n_obs):
        adata.obs['clusters'] = pd.Categorical(clusters)
        if (clusters_colors is not None) & (len(clusters_colors) == len(np.unique(clusters))):
            adata.uns['clusters_colors'] = clusters_colors
        elif colormap is not None:
            adata.uns['clusters_colors'] = colormap[:len(adata.obs['clusters'])]
        else:
            set_clusters_colors(adata, 'clusters')
    elif ('clusters' not in adata.obs_keys()) and ('louvain' not in adata.obs_keys()):
        louvain(adata)

    return adata if copy else None


def tsne(adata, use_pca=True, n_pcs=None, perplexity=50, angle=0.5, init_pos='random', random_state=4, copy=False):
    """Computes a tsne embedding based on perplexity and angle specified

    Arguments
    ---------
    use_pca: bool, default=True
        whether to use principal component space

    n_pcs: int
        number of principal components to be used; optimally chosen if None

    perplexity: int

    angle: float

    init_pos: str or np.array

    random_state: int

    Returns
    -------
    Creates attribute .obsm['X_tsne']
    """
    try:
        from MulticoreTSNE import MulticoreTSNE as TSNE
    except ImportError:
        from sklearn.manifold import TSNE

    if use_pca:
        if 'X_pca' not in adata.obsm_keys():
            pca(adata, n_pcs=n_pcs)
        X = adata.obsm['X_pca'][:, :n_pcs]
    else:
        X = adata.X

    tsne = TSNE(perplexity=perplexity, angle=angle, init=init_pos, random_state=random_state, n_jobs=4)
    adata.obsm['X_tsne'] = tsne.fit_transform(X)
    print_logg('Added tsne embedding \'X_{}\' to .obsm'.format('tsne'))
    return adata if copy else None


def joint_tsne(adata, n_pcs=None, perplexity=50, angle=0.5, init_pos='random', random_state=27, copy=False):
    """Computes a tsne embedding based on perplexity and angle specified

    Arguments
    ---------
    use_pca: bool, default=True
        whether to use principal component space

    n_pcs: int
        number of principal components to be used; optimally chosen if None

    perplexity: int

    angle: float

    init_pos: str or np.array

    random_state: int

    Returns
    -------
    Creates attribute .obsm['X_tsne']
    """
    try:
        from MulticoreTSNE import MulticoreTSNE as TSNE
    except ImportError:
        from sklearn.manifold import TSNE

    if n_pcs is None:
            n_pcs = adata.obsm['X_pca'].shape[1] if 'X_pca' in adata.obsm_keys() else 30

    pca = PCA(n_components=n_pcs)
    X_pca = pca.fit_transform(np.vstack((adata.layers['Ms'], adata.layers['Ms'] + adata.layers['velocity'])))

    tsne = TSNE(perplexity=perplexity, angle=angle, init=init_pos, random_state=random_state, n_jobs=4)
    joint_tsne = tsne.fit_transform(X_pca)

    adata.obsm['X_joint_tsne'] = joint_tsne[:adata.n_obs]
    adata.obsm['V_joint_tsne'] = joint_tsne[adata.n_obs:] - joint_tsne[:adata.n_obs]
    print_logg('Added joint tsne embedding \'X_{}\' to .obsm'.format('joint_tsne'))
    return adata if copy else None


"""
Velocity embedding
---------
"""


def velocity_embedding(adata, basis='tsne', vkey='velocity', scale=10, retain_scale=False, copy=False):
    """Computes the single cell velocities in the embedding

    Arguments
    ---------
    basis: string, default='tsne'
        specifies embedding .obsm['X_' + basis]

    Returns
    -------
    Creates attribute .obsm['V_' + basis]
    """
    T = transition_matrix(adata, vkey, scale).A
    # T = transition_matrix(adata, vkey, scale).tocsr()

    X_emb = adata.obsm['X_' + basis][:, :2]
    knn_ixs = adata.uns['velocity_neighbors']['vgraph']['indices']
    n_obs, n_neighbors = knn_ixs.shape

    V_emb = np.zeros((n_obs, 2))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for i in range(n_obs):
            idx = knn_ixs[i]
            # idx = T[i].indices
            diff = X_emb[idx] - X_emb[i, None]
            diff /= norm(diff)[:, None]
            diff[np.isnan(diff)] = 0  # zero diff in a steady-state
            V_emb[i] = T[i, idx].dot(diff) - diff.sum(0) / n_neighbors
            # V_emb[i] = T[i].data.dot(diff) - diff.sum(0) / len(idx)

    if retain_scale:
        delta = T.dot(adata.X) - adata.X
        cos_proj = (adata.layers[vkey] * delta).sum(1) / norm(delta)
        V_emb *= np.clip(cos_proj, 0, 1)

    Vkey = 'V' + vkey.split('velocity')[1] + '_' + basis
    adata.obsm[Vkey] = V_emb

    print_logg('Added tsne velocity embedding \'{}\' to .obsm'.format(Vkey))
    return adata if copy else None


def grid_velocity_embedding(X_emb, V_emb, density=1, smooth=0.5, n_neighbors=None, min_mass=.5):
    """Computes the velocities for the grid points on the embedding

    Arguments
    ---------
    X_emb: np.ndarray
        embedding coordinates

    V_emb: np.ndarray
        embedded single cell velocity (obtained with 'velocity_embedding')

    density: float, default=1

    smooth: float, default=.5

    n_neighbors: int

    min_mass: float, default=.5

    Returns
    -------
    grid_coord: np.array
        grid point coordinates
    grid_velocity: np.array
        velocity for each grid point in the embedding
    """
    # prepare grid
    n_obs, n_dim = X_emb.shape
    steps = (int(np.sqrt(n_obs) * density), int(np.sqrt(n_obs) * density))

    grs = []
    for dim_i in range(n_dim):
        m, M = np.min(X_emb[:, dim_i]), np.max(X_emb[:, dim_i])
        m = m - .01 * np.abs(M - m)
        M = M + .01 * np.abs(M - m)
        gr = np.linspace(m, M, steps[dim_i])
        grs.append(gr)

    meshes_tuple = np.meshgrid(*grs)
    grid_coord = np.vstack([i.flat for i in meshes_tuple]).T

    # estimate grid velocities
    if n_neighbors is None:
        n_neighbors = int(n_obs/50)
    nn = NearestNeighbors(n_neighbors=n_neighbors, n_jobs=-1)
    nn.fit(X_emb)
    dists, neighs = nn.kneighbors(grid_coord)

    std = np.mean([(g[1] - g[0]) for g in grs])
    weight = normal.pdf(loc=0, scale=smooth * std, x=dists)
    p_mass = weight.sum(1)

    grid_velocity = (V_emb[neighs] * weight[:, :, None]).sum(1) / np.maximum(1, p_mass)[:, None]
    grid_coord, grid_velocity = grid_coord[p_mass > min_mass], grid_velocity[p_mass > min_mass]

    return grid_coord, grid_velocity


def principal_curve(adata, basis='pca', n_comps=4, clusters_list=None, copy=False):
    """
    input : numpy.array
    returns:
    Result::Object
        Methods:
        projections - the matrix of the projectiond
        ixsort - the order ot the points (as in argsort)
        arclength - the lenght of the arc from the beginning to the point
    """
    import rpy2.robjects as robjects
    from rpy2.robjects.packages import importr

    if clusters_list is not None:
        cell_subset = np.array([label in clusters_list for label in adata.obs['clusters']])

    X_emb = adata[cell_subset].obsm['X_' + basis][:, :n_comps]
    n_obs, n_dim = X_emb.shape

    # convert array to R matrix
    xvec = robjects.FloatVector(X_emb.T.reshape((X_emb.size)))
    X_R = robjects.r.matrix(xvec, nrow=n_obs, ncol=n_dim)

    fit = importr("princurve").principal_curve(X_R)

    adata.uns['principal_curve'] = dict()
    adata.uns['principal_curve']['projections'] = np.array(fit[0])
    adata.uns['principal_curve']['ixsort'] = np.array(fit[1])-1
    adata.uns['principal_curve']['arclength'] = np.array(fit[2])
    adata.uns['principal_curve']['cell_subset'] = cell_subset

    return adata if copy else None


def pseudotime(adata, iroot=229, clusters_list=None, copy=False):
    # iroot = adata.obsm['X_umap'][adata.obs['clusters']=='neuroblast 1'][:,1].argmax()
    root_cell = adata.obs_names[iroot]
    if clusters_list is not None:  # ['granule mature', 'neuroblast 1', 'neuroblast 2', 'granule immature']
        cell_subset = np.array([label in clusters_list for label in adata.obs['clusters']])
        adata_subset = adata.copy()
        adata_subset._inplace_subset_obs(cell_subset)
        adata_subset.uns['iroot'] = np.where(adata_subset.obs_names == root_cell)[0][0]
    dpt(adata_subset, n_branchings=0)

    adata.obs['dpt_pseudotime'] = np.zeros(adata.n_obs)
    adata.obs['dpt_pseudotime'][cell_subset] = adata_subset.obs['dpt_pseudotime']
    adata.obs['dpt_pseudotime'][~cell_subset] = -.5

    return adata if copy else None


def random_subsample(adata, frac=.5):
    adata_subset = adata.copy()

    size = int(frac * (adata_subset.n_obs + 1))
    sample_ixs = np.random.choice(range(adata_subset.n_obs), size=size, replace=False)
    adata_subset = adata_subset[sample_ixs]

    del adata_subset.uns['velocity_neighbors']
    moments(adata_subset)

    return adata_subset


def prepare_velocyto_for_comparison(adata, filepath='data/DentateGyrus/10X43_1.loom', fit_offset=False):
    import velocyto as vcy
    vlm = vcy.VelocytoLoom(filepath)

    vlm.Ux_sz = adata.layers['Mu'].T
    vlm.Sx_sz = adata.layers['Ms'].T
    vlm.pcs = adata.obsm['X_pca']
    vlm.ts = adata.obsm['X_tsne']
    vlm.q = np.zeros(adata.n_vars)

    vlm.fit_gammas(weighted=False, fit_offset=fit_offset)

    vlm.predict_U()
    vlm.calculate_velocity()
    vlm.calculate_shift()
    vlm.extrapolate_cell_at_t()

    vkey = 'velocity0'
    adata.layers[vkey] = vlm.velocity.T

    adata.uns[vkey + '_pars'] = dict()
    adata.uns[vkey + '_pars']['gamma'] = vlm.gammas
    adata.uns[vkey + '_pars']['beta'] = np.ones(adata.n_vars)
    adata.uns[vkey + '_pars']['o_s'] = vlm.q

    # if min_counts_s is None: min_counts_s = np.clip(vlm.S.shape[1] / 100, 20, 100)
    # if min_counts_u is None: min_counts_u = int(min_counts_s / 2)
    # if min_cells_s is None: min_cells_s = int(min_counts_s / 2)
    # if min_cells_u is None: min_cells_u = int(min_counts_u / 2)
    #
    # vlm.score_detection_levels(min_expr_counts=min_counts_s, min_cells_express=min_cells_s,
    #                            min_expr_counts_U=min_counts_u, min_cells_express_U=min_cells_u)
    # vlm.filter_genes(by_detection_levels=True)
    #
    # vlm.score_cv_vs_mean(N=n_genes)
    # vlm.filter_genes(by_cv_vs_mean=True)
    #
    # vlm.normalize_by_total(skip_low_U_pop=False)
    # vlm.adjust_totS_totU(normalize_total=True)
    #
    # vlm.default_fit_preparation()

    return vlm


def run_velocyto():

    return None

# adata2 = scv.rx.read_loom("data/DentateGyrus/10X43_1.loom")
# adata2.obs['clusters'] = np.load('./write/DG_clusters.npy')
# adata2.obsm['X_umap'] = np.load('./write/DG_umap.npy')
#
# scv.rx.pp.filter_genes_detection(adata2, min_counts_s=10, min_cells_s=0, min_counts_u=0, min_cells_u=0)
# scv.rx.pp.normalize_per_cell(adata2)
# sc.pp.log1p(adata2)
#
# sc.pp.pca(adata2, n_comps=50)
# #scv.rx.tl.neighbors(adata2, n_neighbors=15, for_moments=True)
# #scv.rx.tl.neighbors(adata2, n_neighbors=14, for_moments=False)
#
# scv.rx.tl.moments(adata2)
#
# scv.rx.tl.velocity(adata2)
# scv.rx.tl.filter_genes_velocity(adata2, min_r2=.01, min_gamma=.01)
#
# scv.rx.tl.velocity_graph(adata2)
#
# scv.rx.tl.velocity_embedding(adata2, basis='umap')
# sc.pl.umap(adata2, color='clusters', show=False)
#
# pl.figure(figsize=(14,12), dpi=120)
# scv.rx.pl.velocity_embedding(adata2, basis='umap', c='clusters', scale=1.5)