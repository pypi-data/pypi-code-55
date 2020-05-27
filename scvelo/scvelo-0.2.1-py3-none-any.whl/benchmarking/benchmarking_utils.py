import scanpy as sc
import scvelo as scv
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import pandas as pd
from scipy.sparse import issparse


def comp_velocities(adata, K=30, key='velocity_dynamical'):
    """Utility funciton that computes velocities from the model parameters
    """

    # delete moments if present and recompute
    if 'Ms' in adata.layers.keys(): del adata.layers['Ms']
    if 'Mu' in adata.layers.keys(): del adata.layers['Mu']
    use_raw = True if K == 0 else False
    if not use_raw:
        scv.pp.moments(adata, n_neighbors=K)

    # get the model parameters
    beta, gamma, z = adata.var['fit_beta'], adata.var['fit_gamma'], adata.var['fit_scaling']

    # get counts
    u = adata.layers['unspliced'] if use_raw else adata.layers['Mu']
    s = adata.layers['spliced'] if use_raw else adata.layers['Ms']
    if issparse(u): u = u.A
    if issparse(s): s = s.A

    # comp velocity
    velocity = u * beta[None, :] / z[None, :] - s * gamma[None, :]

    # save in adata
    adata.layers[key] = velocity


def check_gene(adata, gene, use_raw):
    """Utility function that checks how many shared counts in u and s exist for a gene
    :param adata: AnnData Object
        Annotated Data Matric
    :param gene: str
        Gene to check out
    :param use_raw:
        Checking in raw or imputed data
    :return: n, drop, mean
        number of shared counts, percentage dropout and mean expression (in s)
    """
    if use_raw:
        u = np.where(adata[:, gene].layers['unspliced'].A > 0)[0]
        s = np.where(adata[:, gene].layers['spliced'].A > 0)[0]
    else:
        u = np.where(adata[:, gene].layers['Mu'] > 0)[0]
        s = np.where(adata[:, gene].layers['Ms'] > 0)[0]
    intersect = set(u).intersection(set(s))
    n = len(intersect)

    # dropout and mean expression measured in raw data (.X)
    drop = np.round(1 - np.sum(adata[:, gene].X > 0) / adata.n_obs, 2)
    mean = np.round(np.mean(adata[:, gene].X, axis=0), 2)

    return n, drop, mean


def get_candidates(adata, K=5, N=100, genes=None, markers=None):
    """Utility function to find candidate genes for the dynamical model
    Likelihood based approach that also takes into account number of data points.
    Parameters
    --------
    adata : AnnData object
        Annotated data matrix
    K : int, optional (default: `5`)
        Number of neighbors for KNN smoothing
    N : int, optional (default: `100`)
        Minimum number of shared u and s counts
    genes : list or None, optional (default: `None`)
        Genes to consider. If None, looks at all genes in adata
    markers : dict or None, optional (default: `None`)
        Dictionary with marker genes
    Returns
    --------
    like_table: pd.DataFrame
        Table containing candidate genes, sorted by relevant in descending order
    """

    from scipy.stats import zscore

    # initialise empty likelihoods list
    likelihoods = {}

    # delete moments if present and recompute
    if 'Ms' in adata.layers.keys(): del adata.layers['Ms']
    if 'Mu' in adata.layers.keys(): del adata.layers['Mu']
    use_raw = True if K == 0 else False
    if not use_raw:
        scv.pp.moments(adata, n_neighbors=K)

    # loop over all genes
    if genes is None:
        genes = adata.var_names
    else:
        genes = np.array(genes)[[gene in adata.var_names for gene in genes]]
        if len(genes) == 0:
            print('Could not find any of these genes in adata.var_names.')
            return None
    for gene in tqdm(genes):
        n_data, drop, mean = check_gene(adata, gene, use_raw)
        if n_data > N:
            try:
                dm = scv.pp.DynamicsRecovery(adata, gene, use_raw=use_raw)
                dm.fit()
                likelihood = dm.get_likelihood()
            except:
                likelihood = None

            # add biological relevance
            if markers is not None:
                bio_rel = ", ".join([key for key in markers.keys() if gene in markers[key]])
            else:
                bio_rel = " "

            # write to dictionary
            likelihoods[gene] = [likelihood, n_data, drop, mean, bio_rel, K]

    if len(likelihoods) == 0:
        print('Too few counts for all genes that were considered.')
        return None

    # create DataFrame
    like_table = pd.DataFrame(likelihoods, index=['likelihood', 'n_data',
                                                  'dropout_s', 'mean_s',
                                                  'bio_rel', 'K']).transpose()
    like_table.dropna(inplace=True)

    # print some info
    print('Found {} potential candidates'.format(like_table.shape[0]))

    # compute a usefulness score and sort table
    z_likelihood = zscore(like_table['likelihood'])
    z_n_data = zscore(like_table['n_data'])
    u_score = z_likelihood + z_n_data
    like_table['u_score'] = np.round(u_score.astype(np.float), 2)
    like_table.sort_values(by='u_score', ascending=False, inplace=True)
    like_table['rank'] = np.arange(like_table.shape[0])

    # make sure the model parameters are updated in adata for these genes
    scv.pp.recover_dynamics(adata, var_names=list(like_table.index), return_model=False, use_raw=use_raw,
                            method='adam', plot_results=False, t_max=1 )

    return like_table


def exclude_cluster(adata, cluster, save=False):
    """Utility funciton to show the velocities in the embedding
    when excluding one cluster of data points
    """

    print('Excluding cluster {!r} from the computation.'.format(
        cluster))
    # based on this, we will see what happens when we remove one cluster of cells form the data
    if cluster != None:
        adata_r = adata[adata.obs['clusters'] != cluster, :].copy()
    else:
        adata_r = adata.copy()

    # delete all velocity information
    del adata_r.var['velocity_gamma']
    del adata_r.var['velocity_r2']
    del adata_r.var['velocity_genes']
    del adata_r.uns['velocity_graph']
    del adata_r.uns['velocity_graph_neg']
    del adata_r.obsm['velocity_umap']
    del adata_r.obsm['X_umap']
    del adata_r.layers['velocity']

    # re-compute embedding
    sc.tl.pca(adata_r, svd_solver='arpack', random_state=42)
    sc.pp.neighbors(adata, random_state=42)
    sc.tl.paga(adata_r, groups='clusters')

    # plot paga
    sc.pl.paga(adata_r, save=save)
    print('Computing UMAP...')
    sc.tl.umap(adata_r, init_pos='paga', random_state=42)

    # compute moments
    scv.pp.moments(adata_r, n_neighbors=30, method='sklearn', mode='distances')

    # compute velocities in deterministic mode
    scv.tl.velocity(adata_r, mode='deterministic')

    # compute the velocity graph, using the embedding
    scv.tl.velocity_graph(adata_r, n_neighbors=100, approx='X_umap')

    # compute the embedding
    scv.tl.velocity_embedding(adata_r, basis='umap', use_negative_cosines=False, self_transitions=False,
                              all_comps=False, autoscale=False)

    # plot in the umap
    ax = scv.pl.velocity_embedding_grid(adata_r, basis='umap', frameon=False,
                                        legend_loc='on data', dpi=200,
                                        save=save, show=False)
    ax.set_title(cluster)
    plt.show()


def small_dg_markers():
    marker_genes = {
        'Astrocytes': ['Sox9', 'Etv4', 'Sal3', 'Grin2c', 'Kcng4', 'Gfap', 'Hes5', 'Aqp4'],
        'Radial Glia': ['Tfap2c', 'Hopx', 'Rhcg', 'Vnn1', 'Wnt8b', 'Vnn1', 'Rhcg', 'Wnt8b'],
        'nIPC': ['Mxd3', 'Ascl1', 'Neurog2', 'Rfc4', 'Lockd', 'Neurog2', 'Eomes', 'Neurod4', 'Tfap2c' ],
        'Neuroblast 1': ['Eomes',
                         'Neurod4',
                         'Slc17a6',
                         'Mpped1',
                         'Igfbpl1'
                         'Calb2',
                         'Tac2',
                         'Sox11',
                         'Dcx'
                         ],
        'Neuroblast 2': ['Sox11',
                         'Bhlh2e22',
                         'Neurod2',
                         'Gal',
                         'Igfbpl1',
                         'Insc',
                         'Tac2',
                         'Syt2',
                         'Pdlim4',
                         'Rbp1',
                         'Plin2',
                         'Gins1',
                         'Draxin',
                         'Dcx'
                         ],
        'Immature GC': ['Stc1',
                        'Sdk2',
                        'Rasd1',
                        'Fxyd7',
                        'Il16',
                        'Dsp'
                        'Rspo3',
                        'Prickle2',
                        'Smim3',
                        'Mcm6',
                        'Rasgrf2'
                        ],
        'Mature GC': ['Trpc6',
                      'Ntng1',
                      'Rasgrp1',
                      'Nos1',
                      'Snhg11',
                      'Smad3',
                      'Adarb2',
                      'Ipcef1',
                      'Kcnip3',
                      'Tekt5',
                      'Krt2'
                      ],
        'RGL': ['Gfap',
                'Hes5',
                'Sox9',
                'Lpar1',
                'Nes',
                'Prom1'
                ],
        'Cell Cycle': ['Cdk1',
                       'Top2a',
                       'Aurkb',
                       'Cenpe',
                       'Aurkb',
                       'Mcm2',
                       'Mcm3',
                       'Mcm4',
                       'Mcm5',
                       'Mcm6',
                       'Mcm7',
                       'Mcm8',
                       'Mki67'
                       ]
    }
    return marker_genes


def compute_dist(x_obs, x_theo, weights=None):
    """
    Utility funciton to compute distance between point cloud and curve
    :param x_obs: observed data
    :param x_theo: theoretical data/curve
    :return: distance measure
    """

    """
    score = 0
    for point in x_obs:
        point_extended = np.ones((x_theo.shape[0], 1)) @ point[None, :]
        dist = np.linalg.norm(point_extended-x_theo, axis=1)
        ix = np.argmin(dist)
        min_dist = dist[ix]
        if weights is not None:
            min_dist *= weights[ix]*min_dist
        score += min_dist
    """
    from fastdtw import fastdtw
    score, path = fastdtw(x_obs, x_theo, dist=2)

    return score

def shift_scale(x_obs, x_theo, fit_intercept=False):
    """Utility funciton to shift and scale the integrated velocities
    :param exp_pred: np.array
        Integrated velocities, predictor for gene_expression
    :param gene_exp: np.array
        Original gene expression values
    :param exp_mean: np.array
        Smoothed gene expression
    :return: exp_pred
        Shifted and scaled integrated velocities
    """

    # find the best possible scaling factor using simple lin reg
    # this accounts for not knowing beta
    from sklearn.linear_model import LinearRegression

    reg = LinearRegression(fit_intercept=fit_intercept)
    reg.fit(x_obs[:, None], x_theo)

    return reg.coef_, reg.intercept_


def plot_gene(adata, ax, x, y, type='gene', x_test=None, x_mean=None, x_cov=None, x_grad=None,
                 scatter_kwgs=None):
    """Utility function to plot gene expression, velocity and dpt
    Parameters
    --------
    adata: AnnData Object
        Annotated Data Frame
    ax: plt.axes object
        Axes used for plotting
    x: np.array
        Temporal ordering
    y: np.array
        Expression values
    type: str, optional (default: `"s"`)
        What is being plotted. Gene expression (gene) or velocity (velocity)
    x_test: np.array, optional (default: `None`)
        Grid of values for testing
    x_mean: np.array, optional (default: `None`)
        Smoothed expression values
    x_cov: np.array, optional (default: `None`)
        Covariance matrix for smoothed expression
    x_grad: np.array, optional (default: `None`)
        Derivative of gene expression
    gene_name: str, optional (default: `" "`)
        Name of the gene for plotting
    scatter_kwgs: None or dict, optional (default: `None`)
        keyword arguments for scv.pl.scatter
    Returns
    --------
    Nothing, just plots.
    """

    # basic scatter plot
    if scatter_kwgs is not None:
        ax = scv.pl.scatter(adata, x=x, y=y, ax=ax, show=False, **scatter_kwgs)
    else:
        ax = scv.pl.scatter(adata, x=x, y=y, ax=ax, show=False)
    ax.set_title(" ")

    if x_test is not None:
        # add smoothed expression valued
        if x_mean is not None:
            ax.plot(x_test, x_mean, '-', color='orange', lw=3,
                    label='Smoothed {} expression values'.format(type))
            # add covariance
            if x_cov is not None:
                ax.fill_between(x_test.flatten(), x_mean - np.sqrt(np.diag(x_cov)),
                                x_mean + np.sqrt(np.diag(x_cov)),
                                alpha=0.5, color='k')
        # add the derivative
        if x_grad is not None:
            ax.plot(x_test, x_grad, '--', color='orange', lw=3,
                    label='Derivative of gene expression')

    ax.set_ylabel('{} expression'.format(type), fontsize=10)
    ax.set_xticks([])
    plt.legend(fontsize=10)


def smooth_expression(X, y, n_points=100, mode="gp",
                      length_scale=0.2, type=""):
    """Curve smoothing using Kernel Ridge Regression
    Parameters
    --------
    X: np.array
        Features, at least 2D
    y: np.array
        Targets
    n_points: int, optional (default: `100`)
        number of evenly spaced grid points
    mode: str, optional (default: `"krr"`)
        Smoothing technique to use. Either "krr" for "Kernel Ridge Regression", or "gp",
        for "Gaussian Process". Both use scikit learn implementations and are similar, however, GPs
        offer the possiblity for elegant hyperparameter tuning via gradient descent and are fully Bayesian,
        which offers elegent uncertainty treatment.
    length_scale : float, optional (default: `0.2`)
        Length scale to use for the RBF kernel
    type: str, optional (default: `""`)
        For printing out what's being smoothed
    Returns
    --------
    X_test, y_mean, y_cov: np.array
        Grid of points in feature space and corresponding predicted mean and covariance of targets
    """

    # create the grid we later use for the prediction
    X_test = np.linspace(0, 1, n_points)[:, None]

    if mode == 'krr':
        from sklearn.kernel_ridge import KernelRidge

        # from length scale, compute gamma parameter for RBF kernel
        gamma = 1 / (2 * length_scale ** 2)
        print("Smoothing {!r} using Kernel Ridge Regression and l = {} ".format(type, length_scale))

        # initiate a model
        model = KernelRidge(alpha=1e-6, kernel='rbf', gamma=gamma)

        # fit the data
        model.fit(X, y)

        # predict on grid
        y_mean = model.predict(X_test)
        y_cov = None

    elif mode == 'gp':
        print('Smoothing {} using a Gaussian Process...'.format(type))
        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import RBF

        # create the kernel
        kernel = RBF(length_scale=length_scale)
        alpha = np.std(y)

        # initialise the model
        model = GaussianProcessRegressor(kernel=kernel, alpha=alpha, optimizer=None)

        # fit the model
        model.fit(X, y)

        # make a prediction
        y_mean, y_cov = model.predict(X_test, return_cov=True)

    return X_test, y_mean, y_cov


def pred_exp(X_test, y_test):
    """Predict gene expression based on velocities
    Parameters
    --------
    X_test: np.array
        grid of points in feature space for prediction
    y_test: np.array
        smoothed velocity values
    Returns
    --------
    y_pred: np.array
        predicted values from velocities
    """

    # integrate the velocity to get gene expression
    from scipy.integrate import simps
    n_points = X_test.shape[0]

    # define a function for the derivatife
    def integrate(t, y, x):
        return simps(y[:t], x[:t])

    # compute on a grid
    y_pred = np.array([integrate(t, y_test, X_test.flatten())
                       for t in range(1, n_points + 1)])
    return y_pred


def check_cons(adata, genes=None, n_points=100, smooth=True, length_scale=0.2, mode='gp', differentiate=True,
               return_values=False, return_scores=False, exp_key='Ms', velo_key_ss='velocity',
               velo_key_dyn='velocity_dynamical', scatter_kwgs=None, plotting=True):
    """Plotting function which shows expression level as well as velocity per gene as a function of DPT.
    Aim here is to check for the consistency of the computed velocities
    Params
    --------
    adata: AnnData object
        Annotated data matrix
    genes: list or None, optional (default: `None`)
        List of genes to show
    n_points: int, optional (default: `100`)
        Number of points for the prediction
    smooth: bool, optional (default: `True`)
        Whether to compute smoothed curves
    length_scale : float, optional (default `0.2`)
        length scale for RBF kernel
    mode: str, optional (default: `krr`)
        Whether to use Kernel Ridge Regressin (krr) or a Gaussian Process (gp) for
        smoothing the expression values
    differentiate: bool, optional (default: `True`)
        Whether to take the derivative of gene expression
    return_values: bool, optional (default: `False`)
        Whether to return computed values
    return_scores: bool, optional (default: `False`)
        Whether to return computed goodness-of-velocity scores
    exp_key: str, optional (default:`"ms"`)
        key from adata.layers or just 'X' to get gene expression values
    velo_key_ss, velo_key_dyn: str, optional (default: `"velocity"`)
        key from adata.layers to get velocity  values for the steady state (ss)
        and the dynamical (dyn) model
    scatter_kwgs: dict or None, optional (default: `None`)
        Keyword arguments for scv.pl.scatter
    plotting: bool, optional (default `True`)
        Whether to plot
    Returns
    --------
    Depends on the value of return_values. If True, returns the following:
    dpt: np.array
        Diffusion pseudotime
    gene_exp: np.array
        Gene expresion values for the last gene
    velo_exp: np.array
        Velocity values for the last gene
    """
    # check the input
    if 'dpt_pseudotime' not in adata.obs.keys():
        raise ValueError('Compute DPT first.')

    if velo_key_ss not in adata.layers.keys():
        raise ValueError('Compute {}'.format(velo_key_ss))
    if velo_key_dyn not in adata.layers.keys():
        raise ValueError('Compute {}'.format(velo_key_dyn))

    # check the genes list
    if genes is None:
        genes = adata[:, adata.var['velocity_genes'] == True].var_names[:5]
    else:
        # check whether all of those genes exist in the adata object
        genes_indicator = [gene in adata.var_names for gene in genes]
        if False in genes_indicator:
            genes_missing = np.array(genes)[np.invert(genes_indicator)]
            print('Could not find the following genes: {}'.format(genes_missing))
            genes = list(np.array(genes)[genes_indicator])
    print('Plotting the following genes: {}\n'.format(list(genes)))

    # extract pseudotime
    dpt = adata.obs['dpt_pseudotime']

    # loop over genes
    for gene in genes:
        if exp_key != 'X':
            gene_exp = adata[:, gene].layers[exp_key]
        else:
            gene_exp = adata[:, gene].X
        # exclude dropouts
        ix = (gene_exp != 0)

        velo_exp_ss = adata[:, gene].layers[velo_key_ss]
        velo_exp_dyn = adata[:, gene].layers[velo_key_dyn]
        if issparse(gene_exp): gene_exp = gene_exp.A
        if issparse(velo_exp_ss): velo_exp_ss = velo_exp_ss.A
        if issparse(velo_exp_dyn): velo_exp_dyn = velo_exp_dyn.A
        gene_exp = gene_exp.flatten()

        # compute smoothed values from expression
        if smooth:
            # gene expression
            X_test, exp_mean, exp_cov = smooth_expression(dpt[ix, None], gene_exp[ix], mode=mode, n_points=n_points,
                                                          length_scale=length_scale, type='gene expression')
        else:
            X_test, exp_mean, exp_cov = None, None, None

        if differentiate:
            if not smooth:
                print('You must smooth the data to do compute derivatives.')
            else:
                print('Taking the derivative of gene expression....')
                spacing = X_test[1, 0] - X_test[0, 0]
                gene_grad = np.gradient(exp_mean, spacing)

                # compute goodness-of-velocities measure
                x_obs_ss = np.concatenate((dpt[:, None], velo_exp_ss[:, None]), axis=1)
                x_obs_dyn = np.concatenate((dpt[:, None], velo_exp_dyn[:, None]), axis=1)
                x_theo = np.concatenate((X_test, gene_grad[:, None]), axis=1)
                weights = 1/np.sqrt(np.diag(exp_cov))
                weights = weights/sum(weights)
                score_ss = compute_dist(x_obs_ss, x_theo, weights)
                score_dyn = compute_dist(x_obs_dyn, x_theo, weights)
                print('ss_score = {:2.2e}\ndyn_score = {:2.2e}'.format(score_ss, score_dyn))
        else:
            gene_grad = None

        # scale the steady state velocities
        scaling_factor, _ = shift_scale(velo_exp_ss, gene_grad, fit_intercept=False)
        velo_exp_ss = scaling_factor * velo_exp_ss

        if plotting:
            # Plotting all three quantities
            fig = plt.figure(None, (12, 10))
            y_min = np.min([np.min(velo_exp_ss), np.min(velo_exp_dyn)])
            y_max = np.max([np.max(velo_exp_ss), np.max(velo_exp_dyn)])

            # Gene expression
            ax = fig.add_subplot(311)
            plot_gene(adata, ax, x=dpt, y=gene_exp, type='gene', x_test=X_test, x_mean=exp_mean, x_cov=exp_cov,
                         scatter_kwgs=scatter_kwgs)

            # Steady State Velocities
            ax = fig.add_subplot(312)
            plot_gene(adata, ax, x=dpt, y=velo_exp_ss, type='ss velocity', x_test=X_test, x_grad=gene_grad,
                         scatter_kwgs=scatter_kwgs)
            ax.set_ylim(y_min, y_max)

            # Dynamical Model Velocities
            ax = fig.add_subplot(313)
            plot_gene(adata, ax, x=dpt, y=velo_exp_dyn, type='dyn velocity', x_test=X_test, x_grad=gene_grad,
                         scatter_kwgs=scatter_kwgs)
            ax.set_ylim(y_min, y_max)
            ax.set_xlabel('DPT', fontsize=10)
            ax.set_xticks(np.linspace(0, 1, 10))
            plt.suptitle('Gene: {}'.format(gene), fontsize=20)
            plt.show()

    if return_values:
        return dpt, gene_exp, velo_exp_ss, velo_exp_dyn

    if return_scores:
        return score_ss, score_dyn