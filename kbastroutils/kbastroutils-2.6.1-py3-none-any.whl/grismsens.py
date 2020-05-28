import pandas as pd
from scipy.interpolate import interp1d
from astropy.io import fits
class GrismSens:
    def __init__(self,keyssens,meta,table):
        identifier = meta['IDENTIFIER']
        filt = meta['FILTER']
        sensfile = table['SENS'][identifier][filt]
        self.file = sensfile
        x = fits.open(self.file)
        xdata = pd.DataFrame(x[1].data.tolist())
        ww,ss,ee = xdata[0].values,xdata[1].values,xdata[2].values
        self.model = interp1d(ww,ss
                              ,kind='linear'
                              ,bounds_error=False,fill_value=None)
        self.emodel = interp1d(ww,ee
                              ,kind='nearest'
                              ,bounds_error=False,fill_value=None)