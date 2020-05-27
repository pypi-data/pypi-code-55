#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import math
import io
import os
import tempfile
import shutil
from configparser import ConfigParser
import numpy as np
from grass_session import Session as GrassSession
import grass.script as gscript

from itzi.itzi import SimulationRunner


def gen_eggbox(min_x, max_x, min_y, max_y, res, slope_x, slope_y,
               vshift, phase_shift, amplitude, period):
    """Return an eggbox 2D surface as a numpy array
    """
    X, Y = np.meshgrid(np.arange(min_x, max_x, res),
                       np.arange(min_y, max_y, res))
    ZX = vshift + slope_x*X + (amplitude/2) * np.sin(2*math.pi * (X-phase_shift) / period)
    ZY = slope_y*Y + (amplitude/2) * np.sin(2*math.pi * (Y-phase_shift) / period)
    return ZX + ZY


def np_to_asc(ndarr, res, coord_min, coord_max, filename):
    """Save a numpy ndarray as GRASS ascii raster.
    """
     # get the numpy array and replace nan
    nan_val = -99999
    ndarr[np.isnan(ndarr)] = nan_val
    ncellx = int((coord_max-coord_min) / res)
    assert ncellx == ndarr.shape[1]
    assert ncellx == ndarr.shape[0]
    # header
    north = f"north: {coord_max}\n"
    south = f"south: {coord_min}\n"
    east = f"east: {coord_max}\n"
    west = f"west: {coord_min}\n"
    nrows = f"rows: {ncellx}\n"
    ncols = f"cols: {ncellx}\n"
    nodata = f"null: {nan_val}\n"
    header = north + south + east + west + nrows + ncols + nodata
    # writing file
    np.savetxt(filename, ndarr, fmt='%.6f',
               header=header, comments='')


class EggBox():
    """
    """
    timeout = 300
    def setup(self):
        """Create a temporary GRASS environment
        Generate an eggbox DEM and synthetic inputs
        Generate the configuration file
        """
        os.environ['GRASS_OVERWRITE'] = '1'
        os.environ['ITZI_VERBOSE'] = '0'
        self.tmpdir = str(tempfile.mkdtemp(prefix='grassdata'))
        print(self.tmpdir)
        grass_session = GrassSession()
        grass_session.open(gisdb=self.tmpdir,
                           location='xy',
                           mapset=None,  # PERMANENT
                           create_opts='XY',
                           loadlibs=True)
        os.environ['GRASS_VERBOSE'] = '1'
        # Create new mapset
        mapset_name = 'eggbox'
        gscript.run_command('g.mapset', mapset=mapset_name, flags='c')
        # Define the region
        res = 5
        coord_min = 0
        coord_max = 1000
        region = gscript.parse_command('g.region', res=res,
                                       s=coord_min, n=coord_max,
                                       w=coord_min, e=coord_max,
                                       flags='g')
        # Generate the Egg box DEM
        n_peaks = 5
        amplitude = 2
        slope_x = 0.001
        slope_y = 0.002
        period = coord_max / n_peaks
        phase_shift = period / 4
        egg_box = gen_eggbox(min_x=coord_min, max_x=coord_max,
                             min_y=coord_min, max_y=coord_max,
                             res=res, slope_x=slope_x, slope_y=slope_y,
                             vshift=amplitude, phase_shift=phase_shift,
                             amplitude=amplitude, period=period)
        # Save array in a fake file
        eggbox_file = io.StringIO()
        np_to_asc(egg_box, res, coord_min, coord_max, eggbox_file)
        eggbox_str = str(eggbox_file.getvalue())
        # Map names
        # Import DEM into GRASS
        eggbox_str = eggbox_file.getvalue()
        gscript.write_command('r.in.ascii', input='-', output='dem', stdin=eggbox_str)
        univar_dem = gscript.parse_command('r.univar', map='dem', flags='g')
        assert int(univar_dem['null_cells']) == 0
        # Manning
        gscript.mapcalc('n=0.03')
        # Rain
        gscript.mapcalc('rain=30')
        # Infiltration
        gscript.mapcalc('infiltration=5')
        gscript.mapcalc('cap_pressure=110')
        gscript.mapcalc('eff_porosity=0.4')
        gscript.mapcalc('conductivity=22')

        # Config file
        config = {"time": dict(duration='03:00:00', record_step='00:05:00'),
                  "input": dict(dem='dem', friction='n', rain='rain', infiltration='infiltration'),
                  "output": dict(prefix='eggbox', values='h, infiltration, rainfall, verror')}
        parser = ConfigParser()
        parser.read_dict(config)
        self.config_file = tempfile.mkstemp()[1]
        print(self.config_file)
        with open(self.config_file, 'w') as f:
            parser.write(f)
        return self

    def time_eggbox(self):
        sim_runner = SimulationRunner(need_grass_session=False)
        sim_runner.initialize(self.config_file)
        sim_runner.run().finalize()
        return self

    def teardown(self):
        # shutil.rmtree(self.tmpdir, ignore_errors=True)
        pass



if __name__ == "__main__":
    eggbox = EggBox()
    eggbox.setup().time_eggbox()