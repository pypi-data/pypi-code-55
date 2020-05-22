__author__ = 'Lorza'

import os
import numpy as np
from numpy import dtype
from netCDF4 import Dataset
from caeli.drought_indices import spei
# from warsa.drought.indices import spei


def add_variable_netcdf_file(filepath):

    for filename in os.listdir(filepath):
        filename = os.path.join(filepath, filename)
        if filename.endswith('.nc'):
            nc_in = Dataset(filename, 'r')  # opens the nc_file
            bal = nc_in.variables['ppet']
            ppet = bal[:]

            nc_in.close()

            parameters = list(nc_in.variables.keys())

            # if 'spei' in parameters:
            #     return

            #################################################################
            # transform numpy.ma.core.MaskedArray into numpy.ndarray (to deal with missing values):
            ppet = ppet.filled(np.nan)
            #################################################################
            all_rows_init = np.full(shape=(ppet.shape[0], ppet.shape[1], ppet.shape[2]), fill_value=np.nan)
            for i in list(range(0, ppet.shape[1])):  # rows
                for j in list(range(0, ppet.shape[2])):  # columns
                    all_rows_init[:, i, j] = spei(ppet[:, i, j])
            #################################################################
            nc_file_out = os.path.join(filepath, os.path.basename(filename))
            #################################################################
            nc_out = Dataset(nc_file_out, 'r+', format='NETCDF4')

            # create variable array
            try:
                spei_var = nc_out.createVariable('spei', dtype('float32'), ('time', 'lat', 'lon'))
                spei_var.standard_name = 'standardized_evapotranspiration_precipitation_index'
                spei_var.long_name = 'Standardized Evapotranspiration-Precipitation Index'
                spei_var.short_name = 'SPEI'
                spei_var.units = '-'
                spei_var.missing_value = np.float32(np.ma.array(all_rows_init[:]).get_fill_value())  # this works
                spei_var.comment01 = "SPEI calculated with the Python package caeli, version 0.0.1 (https://github.com/JRoehrig/caeli)"
                spei_var[:] = all_rows_init[:]
            except RuntimeError:
                pass

            nc_out.close()


if __name__ == '__main__':
    work_dir = 'spei_episodes_simulations'

    add_variable_netcdf_file(work_dir)
