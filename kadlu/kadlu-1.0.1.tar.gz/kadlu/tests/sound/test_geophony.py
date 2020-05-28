""" Unit tests for the the 'sound.geophony' module in the 'kadlu' package

    Authors: Oliver Kirsebom
    contact: oliver.kirsebom@dal.ca
    Organization: MERIDIAN-Intitute for Big Data Analytics
    Team: Acoustic data Analytics, Dalhousie University
    Project: packages/kadlu
             Project goal: Tools for underwater soundscape modeling
     
    License:

"""
import pytest
import numpy as np
from kadlu.sound.geophony import geophony, kewley_sl_func, source_level
from kadlu.geospatial.ocean import Ocean
from kadlu.utils import R1_IUGG, deg2rad


def test_kewley_sl_func():
    sl1 = kewley_sl_func(freq=10, windspeed=0)
    sl2 = kewley_sl_func(freq=40, windspeed=2.57)
    assert sl1 == sl2
    assert sl2 == 40.0
    sl3 = kewley_sl_func(freq=40, windspeed=5.14)
    assert sl3 == 44.0
    sl4 = kewley_sl_func(freq=100, windspeed=5.14)
    assert sl4 == 42.5

def test_source_level():
    ok = {'load_bathymetry': 10000, 'load_windspeed': 5.14}
    o = Ocean(**ok)
    sl = source_level(freq=10, x=0, y=0, area=1, ocean=o, sl_func=kewley_sl_func)
    assert sl == 44.0
    sl = source_level(freq=100, x=[0,100], y=[0,100], area=[1,2], ocean=o, sl_func=kewley_sl_func)
    assert sl[0] == 42.5
    assert sl[1] == sl[0] + 20*np.log10(2)

def test_geophony_flat_seafloor():
    """ Check that we can execute the geophony method for a 
        flat seafloor and uniform sound speed profile"""
    kwargs = {'load_bathymetry':10000, 'load_windspeed':1.0, 'ssp':1480, 'angular_bin':90, 'dr':1000, 'dz':1000}
    geo = geophony(freq=100, south=44, north=46, west=-60, east=-58, depth=[100, 2000], xy_res=71, **kwargs)
    spl = geo['spl']
    x = geo['x']
    y = geo['y']
    assert x.shape[0] == 3
    assert y.shape[0] == 5
    assert spl.shape[0] == 3
    assert spl.shape[1] == 5
    assert spl.shape[2] == 2
    assert np.all(np.diff(x) == 71e3)
    assert np.all(np.diff(y) == 71e3)
    # try again, but this time for specific location
    kwargs = {'load_bathymetry':10000, 'load_windspeed':1.0, 'ssp':1480, 'angular_bin':90, 'dr':1000, 'dz':1000, 'propagation_range':50}
    geo = geophony(freq=100, lat=45, lon=-59, depth=[100, 2000], **kwargs)

def test_geophony_in_canyon(bathy_canyon):
    """ Check that we can execute the geophony method for a 
        canyon-shaped bathymetry and uniform sound speed profile"""
    kwargs = {'load_bathymetry':bathy_canyon, 'load_windspeed':1.0, 'ssp':1480, 'angular_bin':90, 'dr':1000, 'dz':1000}
    z = [100, 1500, 3000]
    geo = geophony(freq=10, south=43, north=46, west=60, east=62, depth=z, xy_res=71, **kwargs)
    spl = geo['spl']
    x = geo['x']
    y = geo['y']
    assert spl.shape[0] == x.shape[0]
    assert spl.shape[1] == y.shape[0]
    assert spl.shape[2] == len(z)
    assert np.all(np.diff(x) == 71e3)
    assert np.all(np.diff(y) == 71e3)    
    # check that noise is NaN below seafloor and non Nan above
    bathy = np.swapaxes(np.reshape(geo['bathy'], newshape=(y.shape[0], x.shape[0])), 0, 1)
    bathy = bathy[:,:,np.newaxis]
    xyz = np.ones(shape=bathy.shape) * z
    idx = np.nonzero(xyz >= bathy)
    assert np.all(np.isnan(spl[idx]))
    idx = np.nonzero(xyz < bathy)
    assert np.all(~np.isnan(spl[idx]))