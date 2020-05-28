import numpy as np
import copy
class GrismCONF:
    """
    Example:
    x = GrismCONF('WFC3.UVIS.G280.CHIP1.V2.0.conf')
    x.show() >>> read the file each line
    x.fetch() >>> fecth lines with given keys, and wrap them
    ----------
    GrismCONF is a class handling the read of the .conf files for grism reduction.
    """
    def __init__(self,keysconf,meta,table):
        identifier = meta['IDENTIFIER']
        filterpair = meta['DIRECT'][1]
        if identifier==('HST','WFC3','IR'):
            conffile = table['CONF'][identifier][filterpair]
        elif identifier==('HST','ACS','WFC'):
            conffile = table['CONF'][identifier][(filterpair[0],filterpair[1],meta['CCDCHIP'])]
            self.file = conffile
            self.keysconf = keysconf
            self.value = None
    ##############################
    def show(self):
        x = open(self.file,'r')
        out = {}
        for i,ii in enumerate(x.readlines()):
            print(i,ii)
    ##############################
    def fetch(self,keysconf):
        x = open(self.file,'r')
        xx = x.readlines()
        out = {}
        for i,ii in enumerate(xx):
            y = ii.split()
            if len(y) > 0:
                if y[0] in keysconf:
                    try:
                        a = np.array(y[1:]).astype(float)
                    except:
                        a = np.array(y[1:])
                    out[y[0]] = np.copy(a)
                    if 'ORDER' in y[0]:
                        imin = i+1
                        imax = i+1+np.array(y[1]).astype(int)
                        for j in np.arange(imin,imax+1):
                            yy = xx[j].split()
                            out[yy[0]] = np.array(yy[1:]).astype(float)
        self.value = out