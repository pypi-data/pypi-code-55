'''
This is an interface to read various Abacus file format,
like ASDF, pack9, and RVint.

The decoding of the binary formats is generally contained
in other modules (e.g. bitpacked); this interface mainly
deals with the container formats and high-level logic of
file names, Astropy tables, etc.
'''

import numpy as np
from astropy.table import Table

from .bitpacked import read_rvint

ASDF_DATA_KEY = 'data'
ASDF_HEADER_KEY = 'header'

def read_asdf(fn, colname=None, **kwargs):
    '''
    Read an Abacus ASDF file.  Will try to detect the ASDF column name
    to load, like 'rvint', 'packedpid', or 'pack9'.

    Parameters
    ----------
    
    '''

    import asdf.compression
    try:
        asdf.compression.validate('blsc')
    except:
        raise RuntimeError('Error: your ASDF installation does not support Blosc compression.  Please install the fork with Blosc support with the following command: "pip install git+https://github.com/lgarrison/asdf.git"')


    data_key = kwargs.get('data_key', ASDF_DATA_KEY)
    header_key = kwargs.get('data_key', ASDF_HEADER_KEY)

    with asdf.open(fn, lazy_load=True, copy_arrays=True) as af:
        if colname is None:
            _colnames = ['rvint', 'pack9', 'packedpid']
            for cn in _colnames:
                if cn in af.tree[asdf_data_key]:
                    if colname is not None:
                        raise ValueError(f"More than one key of {_colnames} found in asdf file {fn}. Need to specify colname!")
                    colname = cn
            if colname is None:
                raise ValueError(f"Could not find any of {_colnames} in asdf file {fn}. Need to specify colname!")

        header = af.tree[asdf_header_key]

        data = af.tree['data'][colname]


