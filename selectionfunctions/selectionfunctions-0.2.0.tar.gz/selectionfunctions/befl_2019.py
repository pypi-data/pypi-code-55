#!/usr/bin/env python
#
# befl_2019.py
# Reads the Gaia DR2 selection function from Boubert, Everall, Fraser & Liu (2019, submitted).
#
# Copyright (C) 2019  Douglas Boubert & Andrew Everall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from __future__ import print_function, division

import os
import h5py
import numpy as np

import astropy.coordinates as coordinates
import astropy.units as units
import h5py
import healpy as hp
from scipy import interpolate, special

from .std_paths import *
from .map_base import SelectionFunction, ensure_flat_icrs, coord2healpix
from .source_base import ensure_gaia_g
from . import fetch_utils

from time import time


class BEFL2019Query(SelectionFunction):
    """
    Queries the Gaia DR2 selection function (Boubert & Everall, 2019).
    """

    def __init__(self, map_fname=None, version='modelAB', crowding=False, load_all_clusters=False):
        """
        Args:
            map_fname (Optional[:obj:`str`]): Filename of the BoubertEverall2019 selection function. Defaults to
                :obj:`None`, meaning that the default location is used.
            version (Optional[:obj:`str`]): The selection function version to download. Valid versions
                are :obj:`'modelT'` and :obj:`'modelAB'`
                Defaults to :obj:`'modelT'`.
            crowding (Optional[:obj:`bool`]): Whether or not the selection function includes crowding.
                Defaults to :obj:`'False'`.
            bounds (Optional[:obj:`bool`]): Whether or not the selection function is bounded to 1.7 < G < 21.5.
                Defaults to :obj:`'True'`.
            load_all_clusters (Optional[:obj:`bool`]): Whether or not the full array of clustering data is preloaded or not.
                Defaults to :obj:`'False'`.
        """

        if map_fname is None:
            map_fname = os.path.join(data_dir(), 'befl_2019', 'befl_2019.h5')

        t_start = time()
        
        with h5py.File(map_fname, 'r') as f:
            # Load auxilliary data
            print('Loading auxilliary data ...')
            self._fname = map_fname
            self._nside = 1024
            self._g_grid = f['g_grid'][...]
            self._n_field = f['n_field'][...]
            self._crowding = crowding
            self._version = version
            self._load_all_clusters = load_all_clusters
            if crowding == True:
                self._log10_rho_grid = f['log10_rho_grid'][...]
                self._log10_rho_field= np.log10(f['density_field'][...])
            self._amr_k = f['amr_k'][...]
            self._amr_g = f['amr_g'][...]
            self._amr_logit_p = np.zeros((193,150))
            self._amr_logit_p[:,5:145] = (f['amr_logit_p'][...][f['amr_map'][...]]).T
            self._binom_n_k = f['binom_n_k'][...]
            
            t_auxilliary = time()

            # Load selection function
            print('Loading selection function ...')
            if version == 'modelT':
                if crowding == True:
                    self._theta = f['t_theta_percentiles'][:,:,2]
                else:
                    self._theta = f['t_theta_percentiles'][0,:,2]
            elif version == 'modelAB':
                if crowding == True:
                    self._alpha = f['ab_alpha_percentiles'][:,:,2]
                    self._beta = f['ab_beta_percentiles'][:,:,2]
                else:
                    self._alpha = f['ab_alpha_percentiles'][0,:,2]
                    self._beta = f['ab_beta_percentiles'][0,:,2]

            if load_all_clusters == True:
                print('Warning: You have set load_all_clusters == True. This will load a 7GB array into memory and will take 10 seconds.')
                self._p_cut_II_given_k = f['m_given_k'][...]

            t_sf = time()

        # Create interpolator
        print('Creating detection efficiency interpolator...')
        if version == 'modelT':
            if crowding == True:
                self._theta_interpolator = interpolate.RectBivariateSpline(self._log10_rho_grid,self._g_grid,self._theta)
                self._interpolator = lambda _log10_rho, _g : self._theta_interpolator(_log10_rho, _g, grid = False)
            else:
                self._theta_interpolator = interpolate.interp1d(self._g_grid,self._theta,kind='linear',fill_value='extrapolate')
                self._interpolator = lambda _g : self._theta_interpolator(_g)
        elif version == 'modelAB':
            if crowding == True:
                self._alpha_interpolator = interpolate.RectBivariateSpline(self._log10_rho_grid,self._g_grid,self._alpha)
                self._beta_interpolator = interpolate.RectBivariateSpline(self._log10_rho_grid,self._g_grid,self._beta)
                self._interpolator = lambda _log10_rho, _g : (self._alpha_interpolator(_log10_rho, _g, grid = False),self._beta_interpolator(_log10_rho, _g, grid = False))
            else:
                self._alpha_interpolator = interpolate.interp1d(self._g_grid,self._alpha,kind='linear',fill_value='extrapolate')
                self._beta_interpolator = interpolate.interp1d(self._g_grid,self._beta,kind='linear',fill_value='extrapolate')
                self._interpolator = lambda _g : (self._alpha_interpolator(_g),self._beta_interpolator(_g))

        # Create interpolator which gives probability of satisfying sigma5d cut
        print('Creating sigma5d interpolator...')
        self._amr_logit_p_interpolator = interpolate.interp1d(self._amr_g,self._amr_logit_p,axis=0,kind='linear',fill_value='extrapolate')

        t_interpolator = time()
        
        t_finish = time()
        
        print('t = {:.3f} s'.format(t_finish - t_start))
        print('  auxilliary: {: >7.3f} s'.format(t_auxilliary-t_start))
        print('          sf: {: >7.3f} s'.format(t_sf-t_auxilliary))
        print('interpolator: {: >7.3f} s'.format(t_interpolator-t_sf))


    def _selection_function(self,_g,_hpxidx):

        _k = np.arange(150.0)
        # Calculate the number of observations of each source
        _n = self._n_field[_hpxidx].astype(np.int_)

        # Compute k distribution parameters
        if self._crowding == True:

            # Calculate the local density field at each source
            log10_rho = self._log10_rho_field[_hpxidx]

            # Calculate parameters
            _k_given_ast_parameters = self._interpolator(log10_rho,_g)

        else:

            # Calculate parameters
            _k_given_ast_parameters = self._interpolator(_g)

        # Calculate probability of k_given_ast
        if self._version == 'modelT':

            # This must be Model T, _parameters = (theta)
            _t = _k_given_ast_parameters

            # 0 < theta < 1, make it so!
            _t[_t<0.0] = 1e-6
            _t[_t>1.0] = 1-1e-6
            _k_given_ast = self._binom_n_k[_n]*_t[:,np.newaxis]**_k[np.newaxis,:]*(1.0-_t[:,np.newaxis])**(_n[:,np.newaxis]-_k[np.newaxis,:])

        elif self._version == 'modelAB':

            # This must be Model AB, _parameters = (alpha,beta)
            _a, _b = _k_given_ast_parameters

            # 0.01 < alpha,beta < 1000, make it so!
            _a[_a<1e-2] = 1e-2
            _a[_a>1e+2] = 1e+2
            _b[_b<1e-2] = 1e-2
            _b[_b>1e+2] = 1e+2

            _k_given_ast = self._binom_n_k[_n]*special.beta(_a[:,np.newaxis]+_k[np.newaxis,:],_b[:,np.newaxis]+_n[:,np.newaxis]-_k[np.newaxis,:])/special.beta(_a,_b)[:,np.newaxis]

        # Santity check
        _k_given_ast[np.isnan(_k_given_ast) == True] = 0.0

        # Cut I
        _p_cut_I = np.zeros(_g.size)
        _p_cut_I[_g<=21.0] = 1.0

        # Cut II given k
        if self._load_all_clusters == True:
            _p_cut_II_given_k = self._p_cut_II_given_k[_hpxidx]
        else:
            # This stops us from loading the same healpix multiple times
            unique_hpxidx, unique_inverse = np.unique(_hpxidx, return_inverse=True)
            with h5py.File(self._fname, 'r') as f:
                _p_cut_II_given_k = f['m_given_k'][unique_hpxidx][unique_inverse]

        # Cut III given k and cut II
        _p_cut_III_given_k_cut_II = special.expit(self._amr_logit_p_interpolator(_g))

        # Combine probabilities
        _p_cut_I_cut_II_cut_III = _p_cut_I * np.sum(_p_cut_III_given_k_cut_II*_p_cut_II_given_k*_k_given_ast,axis=1)

        return _p_cut_I_cut_II_cut_III


    @ensure_flat_icrs
    @ensure_gaia_g
    def query(self, sources):
        """
        Returns the selection function at the requested coordinates.

        Args:
            coords (:obj:`astropy.coordinates.SkyCoord`): The coordinates to query.

        Returns:
            Selection function at the specified coordinates, as a fraction.

        """

        # Convert coordinates to healpix indices
        hpxidx = coord2healpix(sources.coord, 'icrs', self._nside, nest=True)


        # Extract Gaia G magnitude
        G = sources.photometry.measurement['gaia_g']

        # Evaluate selection function
        selection_function = self._selection_function(G,hpxidx)

        return selection_function


def fetch():
    """
    Downloads the specified version of the Bayestar dust map.

    Args:
        version (Optional[:obj:`str`]): The map version to download. Valid versions are
            :obj:`'bayestar2019'` (Green, Schlafly, Finkbeiner et al. 2019),
            :obj:`'bayestar2017'` (Green, Schlafly, Finkbeiner et al. 2018) and
            :obj:`'bayestar2015'` (Green, Schlafly, Finkbeiner et al. 2015). Defaults
            to :obj:`'bayestar2019'`.

    Raises:
        :obj:`ValueError`: The requested version of the map does not exist.

        :obj:`DownloadError`: Either no matching file was found under the given DOI, or
            the MD5 sum of the file was not as expected.

        :obj:`requests.exceptions.HTTPError`: The given DOI does not exist, or there
            was a problem connecting to the Dataverse.
    """


    doi = '-----'

    requirements = {'filename': 'befl_2019.h5'}

    local_fname = os.path.join(data_dir(), 'befl_2019', 'befl_2019.h5')

    # Download the data
    fetch_utils.dataverse_download_doi(
        doi,
        local_fname,
        file_requirements=requirements)
