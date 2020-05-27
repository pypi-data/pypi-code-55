from .. import settings
from .. import logging as logg

from ..preprocessing.moments import get_connectivities
from .dynamical_model_utils import mRNA, vectorize, compute_divergence

import numpy as np


def get_reads(adata, key='fit', use_raw=False):
    if 'Ms' not in adata.layers.keys(): use_raw=True
    scaling = adata.var[key + '_scaling'].values
    u = adata.layers['unspliced'] / scaling if use_raw else adata.layers['Mu'] / scaling
    s = adata.layers['spliced'] if use_raw else adata.layers['Ms']
    return u, s


def get_vars(adata, key='fit'):
    alpha = adata.var[key + '_alpha'].values
    beta  = adata.var[key + '_beta'].values
    gamma = adata.var[key + '_gamma'].values
    t_ = adata.var[key + '_t_'].values
    scaling = adata.var[key + '_scaling'].values
    std_u = adata.var[key + '_std_u'].values
    std_s = adata.var[key + '_std_s'].values
    return alpha, beta, gamma, scaling, t_, std_u, std_s


def dynamical_velocity(data, vkey='dynamical_velocity', mode='soft', use_raw=False, copy=False):
    adata = data.copy() if copy else data
    if 'fit_alpha' not in adata.var.keys():
        raise ValueError('Run tl.recover_dynamics first.')

    logg.info('computing dynamical velocities', r=True)

    alpha, beta, gamma, scaling, t_, std_u, std_s = get_vars(adata)
    idx_valid = ~np.isnan(alpha + beta + gamma + scaling + t_)

    data = adata[:, idx_valid]
    alpha, beta, gamma, scaling, t_, std_u, std_s = get_vars(data)

    if mode is 'soft':
        u, s = get_reads(data, use_raw=use_raw)
        tau = data.layers['fit_tau'] if 'fit_tau' in adata.layers.keys() else None
        tau_ = data.layers['fit_tau_'] if 'fit_tau_' in adata.layers.keys() else None
        o_, o, ut, st = compute_divergence(u, s, alpha, beta, gamma, scaling, t_, tau=tau, tau_=tau_, mode='soft_eval',
                                           std_u=std_u, std_s=std_s, connectivities=get_connectivities(adata),
                                           normalized=True, constraint_time_increments=False)
        alpha = alpha * o

    else:
        t = data.layers['fit_t']
        tau, alpha, u0, s0 = vectorize(t, t_, alpha, beta, gamma,)
        ut, st = mRNA(tau, u0, s0, alpha, beta, gamma)

    adata.layers[vkey] = np.ones(adata.shape) * np.nan
    adata.layers[vkey + '_u'] = np.ones(adata.shape) * np.nan

    adata.layers[vkey][:, idx_valid] = ut * beta - st * gamma
    adata.layers[vkey + '_u'][:, idx_valid] = alpha - beta * ut

    logg.info('    finished', time=True, end=' ' if settings.verbosity > 2 else '\n')
    logg.hint('added \n'
              '    \'' + vkey + '\', velocity vectors for each individual cell (adata.layers)')

    return adata if copy else None


def dynamical_shared_time(data, copy=False):
    adata = data.copy() if copy else data

    logg.info('computing shared time', r=True)
    from .dynamical_model_utils import root_time, compute_shared_time
    from .terminal_states import terminal_states
    from ..utils import get_connectivities

    if 'iroot' not in adata.uns.keys():
        if 'root_cells' not in adata.obs.keys(): terminal_states(adata)
        adata.uns['iroot'] = get_connectivities(adata, mode='distances').dot(adata.obs['root_cells']).argmax()
    t, t_ = root_time(adata.layers['fit_t'], root=adata.uns['iroot'])
    adata.obs['time'] = compute_shared_time(t)

    logg.info('    finished', time=True, end=' ' if settings.verbosity > 2 else '\n')
    logg.hint('added \n'
              '    \'time\', shared time (adata.obs)')
    return adata if copy else None
