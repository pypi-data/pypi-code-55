import copy
from astropy.io import fits
import numpy as np
import re
import sys
from acstools import utils_calib

class GrismMeta:
    def __init__(self,files):
        self.files = copy.deepcopy(files)
        self.meta = {}
        for i,ii in enumerate(files):
            self.meta[i] = {}
            self.meta[i]['ID'] = i
            self.meta[i]['FILE'] = ii
        self.make_identifier()
        self.make_basic()
        self.make_advance()
        self.make_fullframe()
    #####
    #####
    #####
    def make_identifier(self):
        KEYS = {'PRIMARY': ['TELESCOP','INSTRUME','DETECTOR']}
        for i in self.meta:
            x = fits.open(self.meta[i]['FILE'])
            iden = []
            for j in KEYS:
                for k in KEYS[j]:
                    iden.append(x[j].header[k])
            self.meta[i]['IDENTIFIER'] = copy.deepcopy(tuple(iden))
    #####
    #####
    #####
    def make_basic(self):
        KEYS = {'PRIMARY': ['SUBARRAY','TARGNAME','RA_TARG','DEC_TARG',
                            'EXPSTART','EXPTIME','POSTARG1','POSTARG2']}
        for i in self.meta:
            x = fits.open(self.meta[i]['FILE'])
            for j in KEYS:
                for k in KEYS[j]:
                    try:
                        self.meta[i][k] = x[j].header[k]
                    except:
                        self.meta[i][k] = None
    #####
    #####
    #####
    def make_advance(self):
        for i in self.meta:
            x = fits.open(self.meta[i]['FILE'])
            identifier = self.meta[i]['IDENTIFIER']
            if identifier == ('HST','WFC3','IR'):
                ext = ('SCI',1)
                self.meta[i]['EXT'] = ext
                self.meta[i]['FILTER'] = x['PRIMARY'].header['FILTER']
                self.meta[i]['IDCSCALE'] = x[ext].header['IDCSCALE']
                self.meta[i]['BUNIT'] = x[ext].header['BUNIT']
            elif identifier == ('HST','ACS','WFC'):
                self.meta[i]['APERTURE'] = x['PRIMARY'].header['APERTURE']
                self.meta[i]['FILTER'] = x['PRIMARY'].header['FILTER1']
                ext = None
                if self.meta[i]['SUBARRAY']:
                    ext = ('SCI',1)
                else:
                    if re.search('WFC2',self.meta[i]['APERTURE']):
                        ext = ('SCI',1)
                    elif re.search('WFC1',self.meta[i]['APERTURE']):
                        ext = ('SCI',2)
                self.meta[i]['EXT'] = ext
                self.meta[i]['CCDCHIP'] = x[ext].header['CCDCHIP']
                self.meta[i]['IDCSCALE'] = x[ext].header['IDCSCALE']
                self.meta[i]['BUNIT'] = x[ext].header['BUNIT']
    #####
    #####
    #####
    def make_fullframe(self):
        for i in self.meta:
            if not self.meta[i]['SUBARRAY']:
                continue
            x = fits.open(self.meta[i]['FILE'])
            ext = self.meta[i]['EXT']
            identifier = self.meta[i]['IDENTIFIER']
            if identifier == ('HST','WFC3','IR'):
                pass
            elif identifier == ('HST','ACS','WFC'):
                hdr = x[ext].header
                binsize,corner = utils_calib.get_corner(hdr,rsize=1)
                self.meta[i]['SUBARRAY_PARAMS'] = {'BINSIZE':binsize, 'CORNER':corner}
            