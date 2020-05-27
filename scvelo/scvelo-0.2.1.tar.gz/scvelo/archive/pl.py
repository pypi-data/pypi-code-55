"""Plotting of velocity embedding and estimates

Main tools:
-----------
pl.scatter
pl.velocity
pl.velocity_embedding
pl.grid_velocity_embedding
"""

from .tl import velocity_embedding as tl_velocity_embedding
from .tl import grid_velocity_embedding as tl_grid_velocity_embedding

import matplotlib.pyplot as pl
from matplotlib import rcParams
from matplotlib.colors import rgb2hex, is_color_like
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import numpy as np
from scanpy.api.pl import *
from scipy.sparse import csr_matrix


"""
Helper functions
----------------
"""


def set_params(s=1):
    rcParams.update({'axes.labelsize': 8*s, 'legend.fontsize': 10*s, 'xtick.labelsize': 10*s, 'ytick.labelsize': 10*s,
                     'text.usetex': False, 'figure.figsize': [15*s, 10*s], 'figure.dpi': 100})


def get_colors(adata, basis):
    cluster_ix = adata.obs[basis].cat.codes
    if basis+'_colors' in adata.uns.keys():
        clusters_colors = adata.uns[basis + '_colors']
    else:
        colormap = np.vstack((pl.cm.tab20b(np.linspace(0., 1, 20))[::2], pl.cm.tab20c(np.linspace(0, 1, 20))[1::2],
                              pl.cm.tab20b(np.linspace(0., 1, 20))[1::2], pl.cm.tab20c(np.linspace(0, 1, 20))[0::2]))
        clusters_colors = [rgb2hex(c) for c in colormap[:len(adata.obs[basis])]]
    return np.array([clusters_colors[cluster_ix[i]] for i in range(adata.X.shape[0])])


def interpret_colorkey(adata, c=None, ckey=None, perc=None):
    if perc is None:
        perc = [2, 98]
    if isinstance(c, str):
        if c in adata.obs_keys():  # clusters colored
            if adata.obs[c].dtype.name == 'category':
                c = get_colors(adata, basis=c)
            else:
                c = adata.obs[c]
                lb, ub = np.percentile(c, perc)
                c = np.clip(c, lb, ub)
        elif c in adata.var_names:  # heatmap of gene expression, velocity or diffusion velocity
            if isinstance(ckey, str) and (ckey in adata.obsm_keys()):
                c = adata.obsm[ckey][:, np.where(adata.var_names == c)[0][0]]
                lb, ub = np.percentile(c, perc)
                c = np.clip(c, lb, ub)
            else:
                c = adata[:, c].X
                lb, ub = np.percentile(c, perc)
                c = np.clip(c, lb, ub)
    elif c is None:
        if 'clusters' in adata.obs_keys():  # clusters colored
            c = get_colors(adata, 'clusters')
        elif 'louvain' in adata.obs_keys():  # louvain colored
            c = get_colors(adata, 'louvain')
        else:
            c = 'grey'
    else:
        lb, ub = np.percentile(c, perc)
        c = np.clip(c, lb, ub)
    return c


def scatter_base(adata, basis='tsne', title=None, xlabel='', ylabel='', fontsize=None, show_annotation=False,
                 show_unannotated=False, show_axis=False, show_colorbar=False, nbins=3, ax=None):
    if show_annotation:
        if 'clusters' in adata.obs_keys():
            clusters = adata.obs['clusters']
            X_emb = adata.obsm['X_' + basis]
            for i, cluster_i in enumerate(np.unique(clusters)):
                if show_unannotated or (not cluster_i.isdigit()):
                    ts_m = np.median(X_emb[clusters == cluster_i, :], 0)
                    pl.text(ts_m[0], ts_m[1], str(clusters[clusters == cluster_i][0]),
                            fontsize=fontsize, bbox={"facecolor": "w", "alpha": 0.6})
        else:
            print('Define clusters first in order to show annotations.')

    if isinstance(title, str):
        pl.title(title, fontsize=fontsize)

    if isinstance(xlabel, str) or isinstance(ylabel, str):
        pl.xlabel(xlabel, fontsize=fontsize)
        pl.ylabel(ylabel, fontsize=fontsize)

    if show_axis:
        if ax is not None:
            ax.xaxis.set_major_locator(MaxNLocator(nbins=nbins))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=nbins))
            labelsize = int(fontsize * .75) if fontsize is not None else None
            ax.tick_params(axis='both', which='major', labelsize=labelsize)
    else:
        pl.axis('off')

    if show_colorbar and (ax is not None):
        cb = pl.colorbar(orientation='vertical', cax= inset_axes(ax, width="2%", height="30%", loc=4, borderpad=0))
        cb.locator = (MaxNLocator(nbins=nbins))
        cb.update_ticks()


def lim_clusters(adata, clusters_list, basis='tsne'):
    try:
        X_emb = adata.obsm['X_'+basis]
        idx_subset = np.array([label in clusters_list for label in adata.obs['clusters']])
        pl.xlim(X_emb[:, 0][idx_subset].min(), X_emb[:, 0][idx_subset].max())
        pl.ylim(X_emb[:, 1][idx_subset].min(), X_emb[:, 1][idx_subset].max())
    except ValueError:
        print('clusters not found.')


"""
Velocity embedding
----------------
"""


def scatter(adata, basis='tsne', x=None, y=None, c=None, ckey=None, perc=None, title=None, xlabel='', ylabel='',
            fontsize=None, show_annotation=False, show_unannotated=False, show_axis=False, show_colorbar=False,
            cmap='RdBu_r', nbins=3, ax=None, **kwargs):
    """Scatter plot

    Arguments
    ---------
    basis: str, default='tsne'
        plots embedding obsm['X_' + basis]

    x: np.ndarray, default=None
        x values for scatter if specified

    y: np.ndarray, default=None
        y values for scatter if specified

    c: str, default=None
        gene expression for heatmap

    c_velo: str, default=None
        gene velocity for heatmap

    title: float, default=.5

    show_annotation: bool, default=False

    show_axis: bool, default=False

    """
    _kwargs = {"s": 10, "alpha": 1}
    _kwargs.update(kwargs)
    c = interpret_colorkey(adata, c, ckey=ckey, perc=perc)

    if (x is None) | (y is None):
            X_emb = adata.obsm['X_' + basis][:, :2]
            x, y = X_emb[:, 0], X_emb[:, 1]

    pl.scatter(x, y, c=c, cmap=cmap, **_kwargs)
    scatter_base(adata, basis, title, xlabel, ylabel, fontsize, show_annotation,
                 show_unannotated, show_axis, show_colorbar, nbins, ax)

    return ax


def velocity_embedding(adata, basis='tsne', c=None, ckey=None, perc=None, vkey='velocity', cmap='RdBu_r', s=1, alpha=.2,
                       density=1, show_annotation=False, show_axis=False, show_colorbar=False,
                       title=None, fontsize=None, pca_transform=False, nbins=3, ax=None, **kwargs):
    """Scatter plot with single cell velocities

    Arguments
    ---------
    basis: str, default='tsne'
        plots embedding obsm['X_' + basis]

    velocity_only: bool, default=False

    show_axis: bool, default=False

    s: float

    alpha: float

    density: float, default=1
        fraction of randomly selected single cells velocities to be visualized
    """
    c = interpret_colorkey(adata, c, ckey=ckey, perc=perc)

    X_emb = adata.obsm['X_'+basis][:, :2]
    x, y = X_emb[:, 0], X_emb[:, 1]
    pl.scatter(x, y, c=c, s=s, alpha=alpha, cmap=cmap)
    scatter_base(adata, basis, title, None, None, fontsize, show_annotation, show_axis, show_colorbar, nbins, ax)

    Vkey = 'V' + vkey.split('velocity')[1] + '_' + basis
    if Vkey not in adata.obsm_keys():
        tl_velocity_embedding(adata, basis, vkey)
    V_emb = adata.obsm[Vkey]

    _kwargs = {"scale": 1, "width": .0005, "edgecolors": 'k', "headwidth": 9, "headlength": 10, "headaxislength": 6, "linewidth": .25}
    _kwargs.update(kwargs)

    ix_choice = np.random.choice(X_emb.shape[0], size=int(density * X_emb.shape[0]), replace=False)

    if pca_transform and (basis == 'pca'):
        X, V, C = adata.uns['pca'].fit_transform(adata.obsm['Ms'])[ix_choice], \
                  adata.uns['pca'].fit_transform(adata.obsm[vkey])[ix_choice], c[ix_choice]
    else:
        X, V, C = X_emb[ix_choice], V_emb[ix_choice], c[ix_choice]

    if is_color_like(C[0]):
        pl.quiver(X[:, 0], X[:, 1], V[:, 0], V[:, 1], color=C, angles='xy', scale_units='xy', cmap=cmap, **_kwargs)
    else:
        pl.quiver(X[:, 0], X[:, 1], V[:, 0], V[:, 1], C, angles='xy', scale_units='xy', cmap=cmap, **_kwargs)

    return ax


def grid_velocity_embedding(adata, basis='tsne', s=40, alpha=.2, density=1, min_mass=.5, smooth=.5, n_neighbors=None,
                            c=None, ckey=None, vkey='velocity', perc=None, cmap='RdBu_r', show_axis=False,
                            show_annotation=False, title=None, fontsize=None, show_colorbar=False, nbins=3, ax=None,  **kwargs):
    """Scatter plot with grid velocities

    Arguments
    ---------
    basis: str, default='tsne'
        plots embedding obsm['X_' + basis]

    velocity_only: bool, default=False

    show_axis: bool, default=False

    s: float

    alpha: float

    density: float, default=1
        density of grid points; higher density implies more grid points

    n_neighbors: int, default=None

    min_mass: float, default=.5

    smooth: float, default=.5
    """
    c = interpret_colorkey(adata, c, ckey=ckey, perc=perc)

    X_emb = adata.obsm['X_'+basis][:, :2]
    x, y = X_emb[:, 0], X_emb[:, 1]
    pl.scatter(x, y, c=c, s=s, alpha=alpha, cmap=cmap)

    Vkey = 'V' + vkey.split('velocity')[1] + '_' + basis
    if Vkey not in adata.obsm_keys():
        tl_velocity_embedding(adata, basis, vkey)
    V_emb = adata.obsm[Vkey]

    _kwargs = {"scale": .5, "width": .001, "color": 'black', "edgecolors": 'k', "headwidth": 4.5, "headlength": 5, "headaxislength": 3, "linewidth": .2}
    _kwargs.update(kwargs)

    X, V = tl_grid_velocity_embedding(X_emb, V_emb, density, smooth, n_neighbors, min_mass)
    pl.quiver(X[:, 0], X[:, 1], V[:, 0], V[:, 1], angles='xy', scale_units='xy', **_kwargs)
    scatter_base(adata, basis, title, None, None, fontsize, show_annotation, show_axis, show_colorbar, nbins, ax)


"""
Pseudotime analysis
-------------------
"""


def principal_curve(adata):
    X_curve = adata.uns['principal_curve']['projections']
    ixsort = adata.uns['principal_curve']['ixsort']
    pl.plot(X_curve[ixsort, 0], X_curve[ixsort, 1], c="k", lw=3, zorder=2000000)


def pseudotime(adata, gene_list, ckey='velocity', reverse=False):
    ixsort = adata.uns['principal_curve']['ixsort']
    arclength = adata.uns['principal_curve']['arclength']
    if reverse: arclength /= np.max(arclength)
    else: arclength = (np.max(arclength) - arclength) / np.max(arclength)
    cell_subset = adata.uns['principal_curve']['cell_subset']

    adata_subset = adata[cell_subset].copy()

    gs = pl.GridSpec(1, len(gene_list))
    for n, gene in enumerate(gene_list):
        i = np.where(adata_subset.var_names == gene)[0][0]
        ax = pl.subplot(gs[n])

        lb, ub = np.percentile(adata_subset.obsm[ckey][:, i], [.5, 99.5])
        c = np.clip(adata_subset.obsm[ckey][ixsort, i], lb, ub)
        # pl.scatter(arclength[ixsort], adata2.obsm['Mu'][ixsort, i], alpha=0.7, c='b', s=5, label="unspliced")
        pl.scatter(arclength[ixsort], adata_subset.obsm['Ms'][ixsort, i] * adata_subset.uns['velocity_pars']['gamma'][i],
                   c=c, cmap='coolwarm', alpha=1, s=1, label="spliced")

        c = c / abs(c).max() * (adata_subset.obsm['Ms'][ixsort, i] * adata_subset.uns['velocity_pars']['gamma'][i]).max()
        z = np.ma.polyfit(arclength[ixsort], c, 8)
        fun = np.poly1d(z)
        pl.plot(arclength[ixsort], fun(arclength[ixsort]), label=ckey)

        # Hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=3))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=3))

        pl.ylabel(gene)
        pl.title('Colored by ' + ckey)


"""
Velocity analysis
----------------
"""


def phase(adata, gene=None, x=None, y=None, ckey=None, vkeys=['velocity'], fontsize=None,
          show_axis=True, show_colorbar=False, ax=None, **kwargs):
    if (x is None) and (y is None):
        if isinstance(gene, str) and gene in adata.var_names:
            ix = np.where(adata.var_names == gene)[0][0]
            s, u = adata.obsm['Ms'][:, ix], adata.obsm['Mu'][:, ix]
        else:
            ix = (adata.obsm['Xs'] > 0).sum(0).argmax()
            gene = adata.var_names[ix]

    c = gene if ckey is not None else None
    scatter(adata, x=s, y=u, c=c, ckey=ckey, show_axis=show_axis, show_colorbar=show_colorbar, title=gene, fontsize=fontsize, ax=ax, **kwargs)
    xnew = np.linspace(0, s.max() * 1.02)

    for vkey in vkeys:
        vpars = vkey+'_pars'
        if vpars in adata.uns_keys():
            linestyle = '--' if 'o_ss' in adata.uns[vpars] else '-'
        pl.plot(xnew, adata.uns[vpars]['gamma'][ix] / adata.uns[vpars]['beta'][ix] * xnew
                + adata.uns[vpars]['o_s'][ix] / adata.uns[vpars]['beta'][ix], c='k', linestyle=linestyle)


def velocity(adata, gene_list=None, basis='tsne', fitkeys=['velocity'], ckeys=['velocity', 'Ms'], cmap='RdBu_r',
             show_clusters=True, var_plot=False, cv_plot=False, s2_plot=False, u2_plot=False, us_plot=False, **kwargs):
    """Plots spliced against unspliced expressions with steady-state fit along with expression and velocity in embedding

    Arguments
    ---------
    gene_list: str or list of str, default=None

    basis: str, default='tsne'
        plots embedding obsm['X_' + basis]

    expr_plot: bool, default=True
        plots gene expression in embedding

    velo_plot: bool, default=True
        plots gene velocity in embedding
    """
    # knn only needed for second order calculation
    knn = adata.uns['velocity_neighbors']['moments']['adjacency']
    knn_weights = knn.multiply(1. / knn[0].sum())

    if gene_list is None:
        idx_genes = (adata.obsm['Xs'] > 0).sum(0).argsort()[::-1][:4]
        gene_list = adata.var_names[idx_genes]
    else:
        gene_list = [gene for gene in gene_list if gene in adata.var_names]

    for ckey in ckeys:
        if ckey not in adata.obsm_keys(): ckeys.remove(ckey)

    for fitkey in fitkeys:
        if fitkey not in adata.obsm_keys(): fitkeys.remove(fitkey)

    vpars, vkeys, vpars2, vkeys2, vpars2u, vkeys2u = [], [], [], [], [], []
    for vkey in fitkeys:
        if 'o_ss' in adata.uns[vkey+'_pars']:
            vpars2.append(vkey+'_pars')
            vkeys2.append(vkey)
        else:
            vpars.append(vkey+'_pars')
            vkeys.append(vkey)
        if 'alpha' in adata.uns[vkey+'_pars']:
            vpars2u.append(vkey+'_pars')
            vkeys2u.append(vkey)

    n_row, n_col = len(gene_list), (1 + len(ckeys) + show_clusters + var_plot+cv_plot+s2_plot+u2_plot+us_plot)

    _kwargs = {"s": 10/n_col, "alpha": .5}
    _kwargs.update(kwargs)

    gs = pl.GridSpec(n_row, n_col, wspace=0.3, hspace=0.5)

    for i, gene in enumerate(gene_list):
        ix = np.where(adata.var_names == gene)[0][0]
        s, u = adata.obsm['Ms'][:, ix], adata.obsm['Mu'][:, ix]

        # spliced/unspliced plot with steady_state estimates
        ax = pl.subplot(gs[i*n_col])
        scatter(adata, x=s, y=u, show_axis=True, title=gene, fontsize=40/n_col,
                xlabel='spliced', ylabel='unspliced', ax=ax, **_kwargs)

        xnew = np.linspace(0, s.max()*1.02)
        for vpar in vpars:
            pl.plot(xnew, adata.uns[vpar]['gamma'][ix] / adata.uns[vpar]['beta'][ix] * xnew
                    + adata.uns[vpar]['o_s'][ix] / adata.uns[vpar]['beta'][ix], c='k')
        for vpar in vpars2:
            pl.plot(xnew, adata.uns[vpar]['gamma'][ix] / adata.uns[vpar]['beta'][ix] * xnew
                    + adata.uns[vpar]['o_s'][ix] / adata.uns[vpar]['beta'][ix], c='k', linestyle='--')
        for vpar in (vpars + vpars2):
            if 'alpha' in adata.uns[vpar]: pl.axhline(y=adata.uns[vpar]['alpha'][ix], c='k', linestyle=':')

        if i == len(gene_list)-1: pl.legend(vkeys + vkeys2, loc='lower right', prop={'size': 34/n_col})
        ix_row = 1

        # velocity and expression plots
        for ckey in ckeys:
            ax = pl.subplot(gs[i*n_col+ix_row])
            title = 'expression' if ckey == 'Ms' else ckey
            scatter(adata, basis, c=gene, ckey=ckey, cmap=cmap, title=title, fontsize=34/n_col, ax=ax, **_kwargs)
            ix_row += 1

        # grid velocity embedding with clusters
        if show_clusters:
            ax = pl.subplot(gs[i * n_col + ix_row])
            scatter(adata, basis, title='clusters', fontsize=34 / n_col, ax=ax, **_kwargs)
            ix_row += 1

        # second order moment plots
        if ix_row < n_col:
            ss = csr_matrix.dot(knn_weights, adata.obsm['Xs'][:, ix] ** 2)
            us = csr_matrix.dot(knn_weights, adata.obsm['Xu'][:, ix] * adata.obsm['Xs'][:, ix])

            if s2_plot:
                ax = pl.subplot(gs[i*n_col+ix_row])
                x = 2 * ss - s
                y = 2 * us + u
                scatter(adata, x=x, y=y, show_axis=True, title=gene, fontsize=40/n_col,
                        xlabel=r'2 $\langle s^2 \rangle - \langle s \rangle$',
                        ylabel=r'2 $\langle us \rangle + \langle u \rangle$', ax=ax, **_kwargs)
                xnew = np.linspace(x.min(), x.max())
                for vpar in vpars2: pl.plot(xnew, adata.uns[vpar]['gamma'][ix] / adata.uns[vpar]['beta'][ix] * xnew
                                            + adata.uns[vpar]['o_ss'][ix] / adata.uns[vpar]['beta'][ix], c='k', linestyle='--')
                if i == len(gene_list) - 1: pl.legend(vkeys2, loc='lower right', prop={'size': 34/n_col})
                ix_row += 1

            if var_plot:
                ax = pl.subplot(gs[i * n_col + ix_row])
                x = 2 * (ss - s**2) - s
                y = 2 * (us - u * s) + u + 2 * s * adata.uns[vkeys2[0]+'_pars']['o_s'][ix] / adata.uns[vkeys2[0]+'_pars']['beta'][ix]
                scatter(adata, x=x, y=y, show_axis=True, title=gene, fontsize=40/n_col,
                        xlabel=r'2 $\Sigma_s - \langle s \rangle$', ylabel=r'2 $\Sigma_{us} + \langle u \rangle$', ax=ax, **_kwargs)
                xnew = np.linspace(x.min(), x.max())
                for vpar in vpars2: pl.plot(xnew, adata.uns[vpar]['gamma'][ix] / adata.uns[vpar]['beta'][ix] * xnew
                                            + adata.uns[vpar]['o_ss'][ix] / adata.uns[vpar]['beta'][ix], c='k', linestyle='--')
                if i == len(gene_list) - 1: pl.legend(vkeys2, loc='lower right', prop={'size': 34/n_col})
                ix_row += 1

            if cv_plot:
                ax = pl.subplot(gs[i * n_col + ix_row])
                x = s * s
                y = 2 * us * s - 2 * u * ss + u * s \
                    + 2 * ss * adata.uns[vkeys2[0]+'_pars']['o_s'][ix]/adata.uns[vkeys2[0]+'_pars']['beta'][ix] \
                    - s * adata.uns[vpar]['o_ss'][ix] / adata.uns[vpar]['beta'][ix]
                scatter(adata, x=x, y=y, show_axis=True, title=gene, fontsize=40/n_col,
                        xlabel=r'2 $\Sigma_s - \mu_s$', ylabel=r'2 $\Sigma_{us} + \mu_u + o$', ax=ax, **_kwargs)
                xnew = np.linspace(x.min(), x.max())
                for vpar in vpars2: pl.plot(xnew, adata.uns[vpar]['gamma'][ix] / adata.uns[vpar]['beta'][ix] * xnew, c='k', linestyle='--')
                if i == len(gene_list) - 1: pl.legend(vkeys2, loc='lower right', prop={'size': 34/n_col})
                ix_row += 1

            if ix_row < n_col:
                uu = csr_matrix.dot(knn_weights, adata.obsm['Xu'][:, ix] ** 2)

            if u2_plot:
                ax = pl.subplot(gs[i * n_col + ix_row])
                x = 2 * u + 1
                y = 2 * uu - u
                scatter(adata, x=x, y=y, show_axis=True, title=gene, fontsize=40/n_col,
                        xlabel=r'$2 \langle u^2 \rangle - \langle u \rangle$', ylabel=r'$2 \langle u \rangle + 1$',
                        ax=ax, **_kwargs)
                xnew = np.linspace(x.min(), x.max())
                for vpar in vpars2u: pl.plot(xnew, adata.uns[vpar]['alpha'][ix] / adata.uns[vpar]['beta'][ix] * xnew
                                            + adata.uns[vpar]['o_uu'][ix] / adata.uns[vpar]['beta'][ix], c='k', linestyle='--')
                if i == len(gene_list) - 1: pl.legend(vkeys2u, loc='lower right', prop={'size': 34/n_col})
                ix_row += 1

            if us_plot:
                ax = pl.subplot(gs[i * n_col + ix_row])
                x = us - uu
                y = adata.uns[vkeys2u[0]+'_pars']['alpha'][ix] * s - adata.uns[vkeys2u[0]+'_pars']['gamma'][ix] * us
                scatter(adata, x=x, y=y, show_axis=True, title=gene, fontsize=40 / n_col,
                        xlabel=r'$2 \langle u^2 \rangle - \langle u \rangle$', ylabel=r'$2 \langle u \rangle + 1$',
                        ax=ax, **_kwargs)
                xnew = np.linspace(x.min(), x.max())
                for vpar in vpars2u: pl.plot(xnew, adata.uns[vpar]['beta'][ix] * xnew, c='k', linestyle='--')
                if i == len(gene_list) - 1: pl.legend(vkeys2u, loc='lower right', prop={'size': 34/n_col})
                ix_row += 1


def velocity_with_major_differences(adata, which='pars', basis='tsne', vkeys=['velocity', 'velocity2'], cmap='RdBu_r',
                                    var_plot=False, s2_plot=False, u2_plot=False, us_plot=False, **kwargs):
    if which == 'pars':
        ixs = np.hstack((adata.uns[vkeys[1]+'_pars']['r2'].argsort()[:2],
                         np.argmin(adata.uns[vkeys[1]+'_pars']['gamma']), np.argmin(adata.uns[vkeys[1]+'_pars']['o_s'])))
    elif which == 'diff':
        def fit_maxdiff():
            scale = adata.obsm['Ms'].max(0) / adata.obsm['Mu'].max(0)
            maxfit_reg = adata.uns[vkeys[0]+'_pars']['gamma'] / adata.uns[vkeys[0]+'_pars']['beta'] * scale
            maxfit_LNA = adata.uns[vkeys[1]+'_pars']['gamma'] / adata.uns[vkeys[1]+'_pars']['beta'] * scale
            return maxfit_LNA - maxfit_reg
        ixs = np.hstack((fit_maxdiff().argsort()[::-1][:2], fit_maxdiff().argsort()[:2]))
    elif which == 'ratio':
        ixs = np.hstack((adata.obsm['Ms'].max(0)/adata.obsm['Mu'].max(0)).argsort()[:4])
    else: ixs = (adata.obsm['Xs'] > 0).sum(0).argsort()[::-1][:4]

    velocity(adata, adata.var_names[ixs], basis, vkeys, cmap, var_plot, s2_plot, u2_plot, us_plot, **kwargs)

