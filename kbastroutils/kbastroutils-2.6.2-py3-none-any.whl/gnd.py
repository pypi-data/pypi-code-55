from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from scipy.optimize import curve_fit
from scipy.integrate import quad
from scipy.interpolate import interp2d
from photutils import CircularAnnulus,CircularAperture,aperture_photometry
from photutils.utils import calc_total_error
from photutils import centroid_sources,centroid_2dg,centroid_com

from kbastroutils.grismconf import GrismCONF
from kbastroutils.grismsens import GrismSens
from kbastroutils.grismapcorr import GrismApCorr
from kbastroutils.dqmask import DQMask
from kbastroutils.make_sip import make_SIP
from kbastroutils.photapcorr import PhotApCorr
from kbastroutils.grismmeta import GrismMeta
from kbastroutils.grismmodel import GrismModel
from kbastroutils.grismcrclean import GrismCRClean
from kbastroutils.grismcalibpath import GrismCalibPath
from kbastroutils.grismdrz import GrismDRZ

import copy,os,pickle,sys,re,shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class GND:
    def __init__(self,files):
        meta = GrismMeta(files)
        self.files = copy.deepcopy(meta.files)
        self.meta = copy.deepcopy(meta.meta)
    ####################
    ####################
    ####################
    def make_pair(self,pairs=None):
        if pairs:
            self.pairs = copy.deepcopy(pairs)
            gid,did = [],[]
            for i in pairs:
                did.append(i)
                for j in pairs[i]:
                    gid.append(j)
                    self.meta[j]['DIRECT'] = (i,(self.meta[j]['FILTER'],self.meta[i]['FILTER']))
            self.did = copy.deepcopy(did)
            self.gid = copy.deepcopy(gid)
        else:
            self.gid,self.did = self.make_pair_id()
            pairs = self.make_pair_auto()
            self.make_pair(pairs)  
    def make_pair_id(self):
        KEYS = {
            'DIRECT': ['F.+'],
            'GRISM': ['G.+']
        }
        gid,did = [],[]
        for i in self.meta:
            filt = self.meta[i]['FILTER']
            y = None
            for j in KEYS:
                for k in KEYS[j]:
                    if re.search(k,filt):
                        y = j
            if y=='DIRECT':
                did.append(i)
            elif y=='GRISM':
                gid.append(i)
            else:
                print('Warning: cannot assign DIRECT or GRISM. {0} {1}'.format(i,self.meta[i]['FILE']))
        return gid,did
    def make_pair_auto(self):
        KEY = 'EXPSTART'
        out = {}
        dmeta = {}
        for i in self.did:
            dmeta[i] = self.meta[i]
        dtab = pd.DataFrame(dmeta).T
        did,dval = dtab['ID'].values,dtab[KEY].values
        tmp = []
        for i in self.gid:
            gval = self.meta[i][KEY]
            tmpp = np.abs(dval-gval)
            tmppp = np.where(tmpp == np.min(tmpp))[0][0]
            tmp.append((did[tmppp],i))
        for i in tmp:
            if i[0] not in out.keys():
                out[i[0]] = [i[1]]
            else:
                tmpppp = out[i[0]]
                tmpppp.append(i[1])
        return out   
    ####################
    ####################
    ####################  
    def make_calibpath(self,
                       keysconf=['DQMASK','DRZSCALE','BEAMA','DYDX_ORDER_A','XOFF_A','YOFF_A','DISP_ORDER_A'],
                       keyssens=None
                      ):
        self.calibpath = GrismCalibPath()
        self.make_calibpath_conf(keysconf)
        self.make_calibpath_sens(keyssens)  
    def make_calibpath_conf(self,keysconf):
        for i in self.gid:
            self.meta[i]['CONF'] = GrismCONF(keysconf,self.meta[i],self.calibpath.table)
            self.meta[i]['CONF'].fetch(self.meta[i]['CONF'].keysconf)
            self.meta[i]['CONF'].value['DQMASK'] = int(self.meta[i]['CONF'].value['DQMASK'][0])
    def make_calibpath_sens(self,keyssens):
        for i in self.gid:
            self.meta[i]['SENS'] = GrismSens(keyssens,self.meta[i],self.calibpath.table)
    ####################
    ####################
    #################### 
    def make_crclean(self,identifier,group=None,params=None,run=False,outpath=None):
        pairs = self.pairs
        meta = self.meta
        self.crclean = GrismCRClean(identifier,pairs,group,params,run,outpath,meta)
        if run:
            for i in self.crclean.meta:
                self.meta[i]['CRCLEAN'] = self.crclean.meta[i]
    ####################
    ####################
    ####################
    def make_xyref(self):
        self.make_xyoff()
        self.make_xydif()
        for j in self.gid:
            xyoff = self.meta[j]['XYOFF']
            xydif = self.meta[j]['XYDIF']
            direct = self.meta[j]['DIRECT'][0]
            xyd = self.meta[direct]['XYD']
            xref = xyd[0] + xyoff[0] + xydif[0]
            yref = xyd[1] + xyoff[1] + xydif[1]
            xyref = (xref,yref)
            self.meta[j]['XYREF'] = xyref 
    def make_xyoff(self):
        for i in self.gid:
            coefxoff = self.meta[i]['CONF'].value['XOFF_A']
            coefyoff = self.meta[i]['CONF'].value['YOFF_A']
            orderx,ordery = self.make_xyofforder(coefxoff),self.make_xyofforder(coefyoff)
            direct = self.meta[i]['DIRECT'][0]
            xyd = self.meta[direct]['XYD']
            if self.meta[i]['SUBARRAY']:
                corner = self.meta[i]['SUBARRAY_PARAMS']['CORNER']
                naxis1 = xyd[0] + corner[0]
                naxis2 = xyd[1] + corner[1]
                xoff = make_SIP(coefxoff,naxis1,naxis2,startx=True)
                yoff = make_SIP(coefyoff,naxis2,naxis2,startx=True)
            else:
                xoff = make_SIP(coefxoff,xyd[0],xyd[1],startx=True)
                yoff = make_SIP(coefyoff,xyd[0],xyd[1],startx=True)
            self.meta[i]['XYOFF'] = (xoff[0],yoff[0])
    def make_xyofforder(self,coef):
        ncoef = len(coef)
        out,n = 0,1
        while n!=ncoef:
            out += 1
            n += out+1
        return out
    def make_xydif(self):
        for i in self.gid:
            post1g,post2g = self.meta[i]['POSTARG1'],self.meta[i]['POSTARG2']
            direct = self.meta[i]['DIRECT'][0]
            post1d,post2d = self.meta[direct]['POSTARG1'],self.meta[direct]['POSTARG2']
            scaleg,scaled = self.meta[i]["IDCSCALE"],self.meta[direct]['IDCSCALE']
            dx = post1g/scaleg - post1d/scaled
            dy = post2g/scaleg - post2d/scaled
            xydif = (dx,dy)
            self.meta[i]['XYDIF'] = copy.deepcopy(xydif)
    ####################
    ####################
    ####################
    def make_xyd(self,XYD=None
                 ,inittype='header'
                 ,adjust=True,box_size=25,maskin=[0]
                ):
        if XYD:
            for i in XYD:
                self.meta[i]['XYD'] = XYD[i]
        else:
            init = self.make_xydinit(inittype)
            if not init:
                print('Error: cannot initiate. Terminate')
                sys.exit()
            if adjust:                    
                xyd = self.make_xydadjust(init,box_size,maskin)
                self.make_xyd(xyd)
            else:
                self.make_xyd(init)
    def make_xydinit(self,inittype):
        out = {}
        if inittype=='header':
            for i in self.did:
                try:
                    tmp = self.meta[i]['XYD']
                    continue
                except:
                    pass
                ra,dec = self.meta[i]['RA_TARG'],self.meta[i]['DEC_TARG']
                w = WCS(header=fits.open(self.files[i])[self.meta[i]['EXT']]
                        ,fobj=fits.open(self.files[i])
                       )
                coord = SkyCoord(ra,dec,unit='deg')
                xx,yy = w.all_world2pix(coord.ra,coord.dec,1)
                out[i] = copy.deepcopy((xx,yy))
            return out
        else:
            print("Error: only inittype='header' is available. Terminate")
            return False 
    def make_xydadjust(self,init,box_size,maskin):
        out = {}
        for i in self.did:
            try:
                tmp = self.meta[i]['XYD']
                continue
            except:
                pass
            x = fits.open(self.files[i])
            xdata = x[self.meta[i]['EXT']].data
            xdq = x['DQ',self.meta[i]['EXT'][1]].data
            xi,yi = int(init[i][0]),int(init[i][1])
            mask = DQMask(maskin)
            mask.make_mask(xdq)
            try:
                xx,yy = centroid_sources(xdata,xi,yi,box_size=box_size,mask=~mask.mask)
                tmp = np.full_like(xdata,False,dtype=bool)
                xi,yi = int(xx[0]),int(yy[0])
                tmp[yi-box_size:yi+box_size+1,xi-box_size:xi+box_size+1] = True
                newmask = (mask.mask & tmp)
                xx,yy = centroid_2dg(xdata,mask=~newmask)            
            except:
                print('Error: cannot make_xydadjust. {0} {1}. Set to inits'.format(i,self.files[i].split('/')[-1]))
                xx,yy = copy.deepcopy(init[i][0]),copy.deepcopy(init[i][1])
            out[i] = copy.deepcopy((xx,yy))
        return out
    ####################
    ####################
    ####################
    def make_traceNwavelength(self):
        self.make_trace()
        self.make_wavelength()
    def make_trace(self):
        for j in self.gid:
            xhbound = self.meta[j]['CONF'].value['BEAMA']
            xh = np.arange(xhbound[0],xhbound[1]+1,step=1)
            xyref = self.meta[j]['XYREF']
            order = self.meta[j]['CONF'].value['DYDX_ORDER_A']
            sip = []
            for k in np.arange(order+1):
                string = 'DYDX_A_' + str(int(k))
                coef = self.meta[j]['CONF'].value[string]
                x = make_SIP(coef,*xyref,startx=True)
                sip.append(x)
            yh = np.full_like(xh,0.,dtype=float)
            for k,kk in enumerate(sip):
                yh += kk*xh**k
            xg = xh + xyref[0]
            yg = yh + xyref[1]
            self.meta[j]['XG'] = xg
            self.meta[j]['YG'] = yg
            self.meta[j]['DYDX'] = sip
    def make_wavelength(self):
        varclength = np.vectorize(self.arclength)
        for j in self.gid:
            xhbound = self.meta[j]['CONF'].value['BEAMA']
            xh = np.arange(xhbound[0],xhbound[1]+1,step=1)
            xyref = self.meta[j]['XYREF']
            order = self.meta[j]['CONF'].value['DISP_ORDER_A'].astype(int)
            dydx = self.meta[j]['DYDX']
            d = []
            sip = []
            for k in np.arange(order+1):
                string = 'DLDP_A_' + str(int(k))
                coef = self.meta[j]['CONF'].value[string]
                x = make_SIP(coef,*xyref,startx=True)
                sip.append(x)
            arc,earc = np.array(varclength(xh,*dydx))
            ww = np.full_like(xh,0.,dtype=float)
            for k,kk in enumerate(sip):
                ww += kk*arc**k
            self.meta[j]['WW'] = ww    
            self.meta[j]['WWUNIT'] = r'$\AA$'
    def arclength_integrand(self,Fa,*coef):
        s = 0
        for i,ii in enumerate(coef):
            if i==0:
                continue
            s += i * ii * (Fa**(i-1))
        return np.sqrt(1. + np.power(s,2))
    def arclength(self,Fa,*coef):
        integral,err = quad(self.arclength_integrand, 0., Fa, args=coef)
        return integral,err 
    ####################
    ####################
    ####################
    def make_bkg(self,method='median',sigma=3.,iters=5,usecrclean=True,maskin=None):
        for j in self.gid:
            x = fits.open(self.files[j])
            ext = self.meta[j]['EXT']
            identifier = self.meta[j]['IDENTIFIER']
            filt = self.meta[j]['FILTER']
            try:
                xdq = fits.open(self.meta[j]['CRCLEAN'])[('DQ',ext[1])].data
            except:
                xdq = x[('DQ',ext[1])].data
            xdata = x[ext].data
            if not maskin:
                maskin = [self.meta[j]['CONF'].value['DQMASK']]
            a = DQMask(value=maskin,declass=True,makeclass=True)
            a.make_mask(xdq)
            mean,median,std = sigma_clipped_stats(xdata,mask=~a.mask,sigma=sigma,maxiters=iters)
            self.meta[j]['BKG'] = None
            self.meta[j]['BKG_FILE'] = None
            if method=='median':
                bkgim = np.full_like(xdata,median,dtype=float)
                self.meta[j]['BKG'] = bkgim
                self.meta[j]['BKG_FILE'] = (method,median,'No file')
            elif method=='master':
                if identifier==('HST','WFC3','IR'):
                    bkg = self.calibpath.table['BKG'][identifier][filt]
                elif identifier==('HST','ACS','WFC'):
                    bkg = self.calibpath.table['BKG'][identifier][(self.meta[j]['CCDCHIP'])]
                if not bkg:
                    print('Error: bkg file is required. Terminate')
                    sys.exit()
                elif bkg:
                    mask = np.full_like(a.mask,True,dtype=bool)
                    mask[np.where(np.abs((xdata - median)/std) > sigma)] = False
                    mask = copy.deepcopy(mask & a.mask)
                    bkgdata = fits.open(bkg)[0].data
                    if self.meta[j]['SUBARRAY']:
                        shape = mask.shape
                        corner = self.meta[j]['SUBARRAY_PARAMS']['CORNER']
                        naxis1 = corner[0] + shape[1] 
                        naxis2 = corner[1] + shape[0]
                        tmp = bkgdata[corner[1]:naxis2,corner[0]:naxis1]
                        bkgdata = copy.deepcopy(tmp)
                    masktmp = np.full_like(mask,False,dtype=bool)
                    m = np.where(bkgdata>0.)
                    masktmp[m] = True
                    mask = copy.deepcopy(mask & masktmp)
                    scale = self.make_mastersky(xdata,mask,bkgdata)
                    self.meta[j]['BKG'] = scale[0] * bkgdata
                    self.meta[j]['BKG_FILE'] = (method,scale,bkg)
    def make_mastersky(self,xdata,xmask,bkgdata):
        x,y = bkgdata[xmask],xdata[xmask]
        popt,pcov = curve_fit(lambda x, *p: p[0]*x, x,y,p0=[1.])
        return (popt,pcov)
    ####################
    ####################
    ####################    
    def make_flat(self,method='uniform'):
        for j in self.gid:
            x = fits.open(self.files[j])
            ext = self.meta[j]['EXT']
            xdata = x[ext].data
            identifier = self.meta[j]['IDENTIFIER']
            filt = self.meta[j]['FILTER']
            self.meta[j]['FLAT'] = None
            self.meta[j]['FLAT_FILE'] = None
            if method=='uniform':
                flatim = np.full_like(xdata,1.,dtype=float)
                self.meta[j]['FLAT'] = flatim
                self.meta[j]['FLAT_FILE'] = (method,'No file')
            elif method=='master':
                if identifier==('HST','WFC3','IR'):
                    flatfile = self.calibpath.table['FLAT'][identifier][filt]
                elif identifier==('HST','ACS','WFC'):
                    flatfile = self.calibpath.table['FLAT'][identifier][(self.meta[j]['CCDCHIP'])]
                if not flatfile:
                    print('Error: flat file is required. Set to None')
                else:
                    flatim = np.full_like(xdata,np.nan,dtype=float)
                    nrow,ncol = xdata.shape[0],xdata.shape[1]
                    y = fits.open(flatfile)
                    wmin,wmax = y[0].header['WMIN'],y[0].header['WMAX']
                    a = {}
                    for k,kk in enumerate(y):
                        if self.meta[j]['SUBARRAY']:
                            shape = xdata.shape
                            corner = self.meta[j]['SUBARRAY_PARAMS']['CORNER']
                            naxis1 = corner[0] + shape[1] 
                            naxis2 = corner[1] + shape[0]
                            a[k] = y[k].data[corner[1]:naxis2,corner[0]:naxis1]
                        else:
                            a[k] = y[k].data
                    x1 = np.copy(self.meta[j]['XG'].astype(int))
                    w1 = np.copy(self.meta[j]['WW'])
                    w1[np.where(w1<=wmin)],w1[np.where(w1>=wmax)] = wmin,wmax
                    x1min,x1max = np.min(x1),np.max(x1)
                    x0,x2 = np.arange(0,x1min),np.arange(x1max+1,ncol)
                    w0,w2 = np.full_like(x0,wmin,dtype=float),np.full_like(x2,wmax,dtype=float)
                    ww = np.concatenate((w0,w1,w2))
                    ww = (ww - wmin) / (wmax - wmin)
                    xx = np.concatenate((x0,x2,x2))
                    s = 0.
                    for k,kk in enumerate(a):
                        s += a[k] * ww**k
                    self.meta[j]['FLAT'] = np.copy(s)
                    self.meta[j]['FLAT_FILE'] = (method,flatfile)
    ####################
    ####################
    ####################
    def make_pam(self,method='uniform'):
        for j in self.gid:
            x = fits.open(self.files[j])
            xdata = x[self.meta[j]['EXT']].data
            self.meta[j]['PAM'] = None
            self.meta[j]['PAM_FILE'] = None
            if method=='uniform':
                self.meta[j]['PAM'] = np.full_like(xdata,1.,dtype=float)
                self.meta[j]['PAM_FILE'] = (method,'No file')
            elif method=='custom':
                if not pamfile:
                    print('Error: pamfile is required. Terminate')
                    sys.exit()
                self.meta[j]['PAM'] = np.copy(fits.open(pamfile)[1].data)
                self.meta[j]['PAM_FILE'] = (method,pamfile)
            elif method=='master':
                print('Error: master method is not available in this version. Terminate')
                sys.exit()
    ####################
    ####################
    ####################
    def make_clean(self,method=[True,True,False,False]):
        for j in self.gid:
            x = fits.open(self.files[j])
            ext = self.meta[j]['EXT']
            xdata = x[ext].data
            bkg = self.meta[j]['BKG'] if method[0]==True else 0.
            flat = self.meta[j]['FLAT'] if method[1]==True else 1.
            pam = self.meta[j]['PAM'] if method[2]==True else 1.
            tmp = (xdata - bkg) * pam
            m = np.where(flat>0.)
            cleandata = np.copy(tmp)
            cleandata[m] = tmp[m] / flat[m]
            if method[3]:
                data = np.full_like(cleandata,0.,dtype=float)
                bkglocal = self.meta[j]['BKG_LOCAL']['VAL']
                corner = self.meta[j]['BKG_LOCAL']['PARAMS']['corner']
                shape = self.meta[j]['BKG_LOCAL']['PARAMS']['shape']
                data[corner[1]:corner[1]+shape[0],corner[0]:corner[0]+shape[1]] = copy.deepcopy(bkglocal)
                cleandata = cleandata - data
            self.meta[j]['CLEAN'] = np.copy(cleandata)
    ####################
    ####################
    ####################
    def make_drz(self,group=None,params=None,run=False,outpath=None):
        pairs = self.pairs
        meta = self.meta
        self.drz = GrismDRZ(pairs,group,params,run,outpath,meta)
    ####################
    ####################
    ####################

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def make_photparams(self,method='aperture',apsize=5,apunit='pix',maskin=None
                        ,sigma=3.,iters=5
                        ,dobkgann=True,bkgann=(20.,25.)
                       ):
        for j in self.did:
            instrument = '-'.join((self.meta[j]['TELESCOP'],self.meta[j]['INSTRUME'],self.meta[j]['DETECTOR']))
            self.meta[j]['PHOT_PARAMS'] = {}
            self.meta[j]['PHOT_PARAMS']['INSTRUMENT'] = instrument
#             nchip = self.meta[j]['NCHIP']
            string = 'FILTER'
            self.meta[j]['PHOT_PARAMS']['FILTER'] = self.meta[j][string]
            self.meta[j]['PHOT_PARAMS']['METHOD'] = method
            self.meta[j]['PHOT_PARAMS']['APSIZE'] = apsize
            self.meta[j]['PHOT_PARAMS']['APUNIT'] = apunit
            self.meta[j]['PHOT_PARAMS']['MASKIN'] = maskin
            self.meta[j]['PHOT_PARAMS']['SIGMA'] = sigma
            self.meta[j]['PHOT_PARAMS']['ITERS'] = iters
            self.meta[j]['PHOT_PARAMS']['DOBKGANN'] = dobkgann
            self.meta[j]['PHOT_PARAMS']['BKGANN'] = bkgann
    def make_phot(self):
        mean,median,std,error = [],[],[],[]
        for i in self.did:
            xdata = fits.open(self.files[i])[self.meta[i]['EXT']].data
            exptime = self.meta[i]['EXPTIME']
            photparams = copy.deepcopy(self.meta[i]['PHOT_PARAMS'])
            photapcorr = PhotApCorr()
            if photparams['APUNIT']!='pix':
                print('Error: apunit must be pix. Terminate')
                continue
            if photparams['MASKIN']:
                print('Error: maskin is not implemented in this version. Terminate')
                continue
            if photparams['INSTRUMENT'] not in photapcorr.instrument:
                print('Error: instrument does not match PhotApCorr.instrument. Terminate')
                continue
            m = np.isfinite(xdata)
            error = calc_total_error(data=xdata,bkg_error=np.zeros_like(xdata),effective_gain=exptime)
            xyd = self.meta[i]['XYD']
            ap = CircularAperture((xyd[0],xyd[1]),r=photparams['APSIZE'])
            aptab = aperture_photometry(xdata,ap,error=error)
            ann = CircularAnnulus((xyd[0],xyd[1]),r_in=photparams['BKGANN'][0],r_out=photparams['BKGANN'][1])
            bkgtab = aperture_photometry(xdata,ann,error=error)
            bkg,bkg_error = None,None
            if photparams['DOBKGANN']:
                bkg = bkgtab['aperture_sum'] * ap.area / ann.area
                ebkg = bkgtab['aperture_sum_err'] * ap.area / ann.area
            else:
                bkg,bkg_error = 0.,0.
            wave,ZP = None,None  
            if photapcorr.table[photparams['INSTRUMENT']]['ZP'][photparams['FILTER']]:
                tmp = photapcorr.table[photparams['INSTRUMENT']]['ZP'][photparams['FILTER']]
                wave = tmp[0]
                ZP = tmp[1]
                self.meta[i]['PHOT_PARAMS']['ZP'] = copy.deepcopy(tmp)
            else:
                print('Error: filter does not match PhotApCorr.table. Terminate')
                continue
            apsize = copy.deepcopy(photparams['APSIZE'])
            if photparams['APUNIT']=='pix':
                if photapcorr.table[photparams['INSTRUMENT']]['scaleunit']=='arcsec/pix':
                    apsize = apsize * photapcorr.table[photparams['INSTRUMENT']]['scale']
                elif photapcorr.table[photparams['INSTRUMENT']]['scaleunit']=='pix/arcsec':
                    apsize = apsize / photapcorr.table[photparams['INSTRUMENT']]['scale']
            EE = photapcorr.table[photparams['INSTRUMENT']]['model'](wave,apsize)
            mag = -2.5 * np.log10((aptab['aperture_sum'] - bkg) / EE) + ZP
            emag = -2.5 * np.sqrt(aptab['aperture_sum_err']**2 + ebkg**2) / ((aptab['aperture_sum'] - bkg) * np.log(10.))
            self.meta[i]['ABMAG'] = (mag[0],emag[0])



    ####################
    ####################
    ####################
    def make_stamp(self,padx=5,pady=50):
        for j in self.gid:
            xg = self.meta[j]['XG']
            yg = self.meta[j]['YG']
            xgmin,xgmax = xg.min().astype(int)-padx,xg.max().astype(int)+padx
            ygmin,ygmax = yg.min().astype(int)-pady,yg.max().astype(int)+pady
            self.meta[j]['STAMP'] = ((xgmin,xgmax),(ygmin,ygmax))
    ####################
    ####################
    ####################
    def make_wavebin(self,method='WW',wavebin=None):
        for j in self.gid:
            self.meta[j]['WAVEBIN'] = None
            if method=='custom':
                if not wavebin:
                    print('Error: wavebin is required. Set to None')
                else:
                    self.meta[j]['WAVEBIN'] = wavebin
            elif (method=='WW') or (method=='median'):
                ww = np.copy(self.meta[j]['WW'])
                wavebin = np.diff(ww)
                median = np.median(wavebin)
                if method=='median':
                    wavebin = np.full_like(ww,median,dtype=float)
                elif method=='WW':
                    wavebin = np.concatenate((wavebin,[median]))
                self.meta[j]['WAVEBIN'] = np.copy(wavebin)
    ####################
    ####################
    ####################
    def make_exparams(self,method='aperture',apsize=5,apunit='pix',maskin=None):
        for j in self.gid:
            self.meta[j]['EX_PARAMS'] = {}
#             nchip = self.meta[j]['NCHIP']
            string = 'FILTER'
            instrument = '-'.join((*self.meta[j]['IDENTIFIER']
                                   ,self.meta[j][string]
                                  ))
            self.meta[j]['EX_PARAMS']['INSTRUMENT'] = instrument
            self.meta[j]['EX_PARAMS']['METHOD'] = method
            self.meta[j]['EX_PARAMS']['APSIZE'] = apsize
            self.meta[j]['EX_PARAMS']['APUNIT'] = apunit
            self.meta[j]['EX_PARAMS']['MASKIN'] = maskin
    ####################
    ####################
    ####################
    def make_apcorr(self,replace='median'):
        grismapcorr = GrismApCorr()
        for j in self.gid:
            instrument = self.meta[j]['EX_PARAMS']['INSTRUMENT']
            ww = self.meta[j]['WW']
            apsize = self.meta[j]['EX_PARAMS']['APSIZE']
            apunit = self.meta[j]['EX_PARAMS']['APUNIT']
            self.meta[j]['APCORR'] = grismapcorr.make_apcorr(instrument,ww,apsize,apunit,replace)
    ####################
    ####################
    ####################
    
    
    
    
    
    
    
    
    
    
    
    
    
    def make_count(self,replace=None,usedrz=False):
        for j in self.gid:
            xg = self.meta[j]['XG'].astype(int)
            yg = self.meta[j]['YG'].astype(int)
            xdata = self.meta[j]['CLEAN']
            bunit = self.meta[j]['BUNIT']
            apsize = self.meta[j]['EX_PARAMS']['APSIZE']
            apunit = self.meta[j]['EX_PARAMS']['APUNIT']
            method = self.meta[j]['EX_PARAMS']['METHOD']
            maskin = self.meta[j]['EX_PARAMS']['MASKIN']
            if apunit!='pix':
                print('Error: apunit must be pix. Terminate')
                sys.exit()
            if method=='aperture':
                cc = np.full_like(xg,np.nan,dtype=float)
                for k,kk in enumerate(xg):
                    cc[k] = np.sum(xdata[yg[k]-apsize:yg[k]+apsize+1,xg[k]])
                self.meta[j]['COUNT'] = np.copy(cc)  
            else:
                print('Error: method must be aperture. Terminate')
                sys.exit()
        if usedrz:
            for j in self.drz.meta:
                xg = self.drz.meta[j]['XG'].astype(int)
                yg = self.drz.meta[j]['YG'].astype(int)
                xdata = self.drz.meta[j]['CLEAN']
                bunit = 'ELECTRONS/S'
                apsize = self.drz.meta[j]['EX_PARAMS']['APSIZE']
                apunit = self.drz.meta[j]['EX_PARAMS']['APUNIT']
                method = self.drz.meta[j]['EX_PARAMS']['METHOD']
                maskin = self.drz.meta[j]['EX_PARAMS']['MASKIN']
                if apunit!='pix':
                    print('Error: apunit must be pix. Terminate')
                    sys.exit()
                if method=='aperture':
                    cc = np.full_like(xg,np.nan,dtype=float)
                    for k,kk in enumerate(xg):
                        cc[k] = np.sum(xdata[yg[k]-apsize:yg[k]+apsize+1,xg[k]])
                    self.drz.meta[j]['COUNT'] = np.copy(cc)  
                else:
                    print('Error: method must be aperture. Terminate')
                    sys.exit()
    ####################
    ####################
    ####################
    def make_flam(self,usedrz=False):
        for j in self.gid:
            count = self.meta[j]['COUNT']
            apcorr = self.meta[j]['APCORR']
            wavebin = self.meta[j]['WAVEBIN']
            ww = self.meta[j]['WW']
            ss = self.meta[j]['SENS'].model(ww)
            flam = count / (wavebin * apcorr * ss)
            self.meta[j]['FLAM'] = np.copy(flam)
            if self.meta[j]['BUNIT'] == 'ELECTRONS':
                self.meta[j]['FLAM'] = copy.deepcopy(self.meta[j]['FLAM'] / self.meta[j]['EXPTIME'])
            self.meta[j]['FLAMUNIT'] = r'erg/s/cm$^2$/$\AA$'
        if usedrz:
            for j in self.drz.meta:
                count = self.drz.meta[j]['COUNT']
                apcorr = self.drz.meta[j]['APCORR']
                wavebin = self.drz.meta[j]['WAVEBIN']
                ww = self.drz.meta[j]['WW']
                ss = self.drz.meta[j]['SENS'].model(ww)
                flam = count / (wavebin * apcorr * ss)
                self.drz.meta[j]['FLAM'] = np.copy(flam)
                if self.drz.meta[j]['BUNIT'] == 'ELECTRONS':
                    self.drz.meta[j]['FLAM'] = copy.deepcopy(self.drz.meta[j]['FLAM'] / self.drz.meta[j]['EXPTIME'])
                self.drz.meta[j]['FLAMUNIT'] = r'erg/s/cm$^2$/$\AA$'
    ####################
    ####################
    ####################
    def save(self,path=None,filename='GND.pickle'):
        if not path:
            print('Error: path is required. Terminate')
            return
        if path[-1] != '/':
            path += '/'
        try:
            os.mkdir(path)
        except:
            pass
        file = path + filename
        f = open(file,'wb')
        pickle.dump(self,f)
        f.close()
    ####################
    ####################
    ####################
    def show(self,method='meta',scale=('percentile',5.,95.)
             ,column=None,dosort=True,sort = ['EXPSTART','POSTARG1','POSTARG2','FILTER']
             ,traceon=False,dqon=False
             ,normalize=False
             ,showconf='long'
             ,zoom=False,dx=50,dy=50
             ,apsize=5,tracefrom='original'
             ,xmin=None, xmax=None
             ,ymin=None, ymax=None
             ,output=False
             ,ylog=False
            ):
        if method=='meta':
            tab = pd.DataFrame(self.meta).T
            if output:
                return tab
            else:
                if dosort:
                    display(tab.sort_values(sort))
                else:
                    display(tab)
        if method=='direct':
            for i in self.did:
                x = fits.open(self.files[i])
                xdata = x[self.meta[i]['EXT']].data
                m = np.where(np.isfinite(xdata))
                vmin,vmax=None,None
                if scale[0]=='percentile':
                    vmin,vmax = np.percentile(xdata[m],scale[1]),np.percentile(xdata[m],scale[2])
                elif scale[0]=='value':
                    vmin,vmax = scale[1],scale[2]
                else:
                    print("Error: scale must be either percentile or value. Set to ('percentile',5.,95.).")
                    vmin,vmax = np.percentile(xdata[m],5.),np.percentile(xdata[m],95.)
                plt.figure(figsize=(10,10))
                plt.imshow(xdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                plt.title('{0} {1}'.format(i,self.files[i]))
                xyd = self.meta[i]['XYD']
                plt.scatter(*xyd,s=500,lw=4,edgecolor='red',facecolor='None',label='XYD')
                plt.legend()
                if zoom:
                    x,y = xyd[0],xyd[1]
                    plt.xlim(x-dx,x+dx+1)
                    plt.ylim(y-dx,y+dy+1)
        if method=='grism':
            for i in self.pairs:
                for j in self.pairs[i]:
                    x = fits.open(self.files[j])
                    xdata = x[self.meta[i]['EXT']].data
                    m = np.where(np.isfinite(xdata))
                    vmin,vmax=None,None
                    if scale[0]=='percentile':
                        vmin,vmax = np.percentile(xdata[m],scale[1]),np.percentile(xdata[m],scale[2])
                    elif scale[0]=='value':
                        vmin,vmax = scale[1],scale[2]
                    else:
                        print("Error: scale must be either percentile or value. Set to ('percentile',5.,95.).")
                        vmin,vmax = np.percentile(xdata[m],5.),np.percentile(xdata[m],95.)
                    plt.figure(figsize=(10,10))
                    plt.imshow(xdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                    plt.title('{0} {1}'.format(j,self.files[j]))
                    ############
                    xyd = self.meta[i]['XYD']
                    xyref = self.meta[j]['XYREF']
                    plt.scatter(*xyref,s=30,color='red',label='XYREF')
                    plt.scatter(*xyd,s=30,color='orange',label='XYD')
                    plt.legend()
                    if traceon:
                        xg = self.meta[j]['XG']
                        yg = self.meta[j]['YG']
                        plt.plot(xg,yg,color='red',label='trace')
                        plt.legend()
                    if zoom:
                        xmin = self.meta[j]['XG'].min() - dx
                        xmax = self.meta[j]['XG'].max() + dx + 1
                        plt.xlim(xmin,xmax)
                        ymin = self.meta[j]['YG'].min() - dy
                        ymax = self.meta[j]['YG'].max() + dy + 1
                        plt.ylim(ymin,ymax)
        if (method=='CONF') & (showconf=='long'):
            for i in self.pairs:
                for j in self.pairs[i]:
                    x = open(self.meta[j]['CONF'].file,'r')
                    print('gid ',j,self.meta[j]['CONF'].file,'\n')
                    for i,ii in enumerate(x.readlines()):
                        print(i,ii)
                    print('\n############################\n')
        elif (method=='CONF') & (showconf=='short'):
            for i in self.pairs:
                for j in self.pairs[i]:
                    print('gid',j,self.meta[j]['CONF'].file,'\n')
                    display(self.meta[j]['CONF'].value)
                    print('\n############################\n')
        if method=='count':
            for i in self.pairs:
                plt.figure(figsize=(10,10))
                for j in self.pairs[i]:
                    xg = self.meta[j]['XG'].astype(int)
                    yg = self.meta[j]['YG'].astype(int)
                    ww = self.meta[j]['WW']
                    if tracefrom=='original':
                        x = fits.open(self.files[j])
                        xdata = x[self.meta[j]['EXT']].data
                    elif tracefrom=='clean':
                        xdata = self.meta[j]['CLEAN']
                    cc = np.full_like(xg,np.nan,dtype=float)
                    for k,kk in enumerate(xg):
                        cc[k] = np.sum(xdata[yg[k]-apsize:yg[k]+apsize+1,xg[k]])
                    plt.plot(ww,cc,label='{0} {1}'.format(j,self.files[j].split('/')[-1]))
                plt.ylabel('{0} \n apsize={1}'.format(self.meta[j]['BUNIT'],apsize))
                plt.xlabel('Wavelength ($\AA$)')
                plt.legend(bbox_to_anchor=(1.04,1),loc='upper left',ncol=1)                     
        if method=='bkg':
            for i in self.pairs:
                for j in self.pairs[i]:
                    fig,ax = plt.subplots(1,3,figsize=(30,10))
                    xdata = fits.open(self.files[j])[self.meta[j]['EXT']].data
                    bkgdata = self.meta[j]['BKG']
                    subdata = xdata - bkgdata
                    m = np.where(np.isfinite(xdata))
                    vmin,vmax = np.percentile(xdata[m],5.),np.percentile(xdata[m],95.)
                    ax[0].imshow(xdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                    ax[1].imshow(bkgdata,origin='lower',cmap='viridis'
                                 ,vmin=np.percentile(bkgdata,5.),vmax=np.percentile(bkgdata,95.)
                                )
                    ax[2].imshow(subdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                    ax[0].set_title('{0} {1}'.format(j,self.files[j].split('/')[-1]))
                    ax[1].set_title('bkg')
                    ax[2].set_title('subtract')
        if method=='flat':
            for i in self.pairs:
                for j in self.pairs[i]:
                    fig,ax = plt.subplots(1,3,figsize=(30,10))
                    xdata = fits.open(self.files[j])[self.meta[j]['EXT']].data
                    flatdata = self.meta[j]['FLAT']
                    normdata = xdata / flatdata
                    m = np.where(np.isfinite(xdata))
                    vmin,vmax = np.percentile(xdata[m],5.),np.percentile(xdata[m],95.)
                    ax[0].imshow(xdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                    ax[1].imshow(flatdata,origin='lower',cmap='viridis'
                                 ,vmin=np.percentile(flatdata,5.),vmax=np.percentile(flatdata,95.)
                                )
                    ax[2].imshow(normdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                    ax[0].set_title('{0} {1}'.format(j,self.files[j].split('/')[-1]))
                    ax[1].set_title('flat')
                    ax[2].set_title('normalized')
        if method=='pam':
            for i in self.pairs:
                for j in self.pairs[i]:
                    fig,ax = plt.subplots(1,3,figsize=(30,10))
                    xdata = fits.open(self.files[j])[self.meta[j]['EXT']].data
                    pamdata = self.meta[j]['PAM']
                    correctdata = xdata * pamdata
                    m = np.where(np.isfinite(xdata))
                    vmin,vmax = np.percentile(xdata[m],5.),np.percentile(xdata[m],95.)
                    ax[0].imshow(xdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                    ax[1].imshow(pamdata,origin='lower',cmap='viridis'
                                 ,vmin=np.percentile(pamdata,5.),vmax=np.percentile(pamdata,95.)
                                )
                    ax[2].imshow(correctdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                    ax[0].set_title('{0} {1}'.format(j,self.files[j].split('/')[-1]))
                    ax[1].set_title('pam')
                    ax[2].set_title('corrected')
        if method=='stamp':
            for j in self.gid:
                ext = self.meta[j]['EXT']
                xdata = fits.open(self.files[j])[ext].data
                xdq = fits.open(self.files[j])[('DQ',ext[1])].data
                m = np.where(np.isfinite(xdata))
                vmin,vmax = np.percentile(xdata[m],5.),np.percentile(xdata[m],95.)
                stamp = self.meta[j]['STAMP']
                plt.figure(figsize=(10,10))
                plt.imshow(xdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                plt.xlim(stamp[0][0],stamp[0][1])
                plt.ylim(stamp[1][0],stamp[1][1])
                plt.title('{0} {1}'.format(j,self.files[j].split('/')[-1]))
                if dqon:
                    plt.figure(figsize=(10,10))
                    plt.imshow(xdq,origin='lower',cmap='viridis',vmin=0,vmax=1)
                    plt.xlim(stamp[0][0],stamp[0][1])
                    plt.ylim(stamp[1][0],stamp[1][1])
                    plt.title('DQ vmin=0, vmax=1')
        if method=='WW':
            for i in self.pairs:
                for j in self.pairs[i]:
                    ww = np.copy(self.meta[j]['WW'])
                    xg = np.copy(self.meta[j]['XG'])
                    if normalize:
                        xg -= self.meta[j]['XYREF'][0]
                    plt.plot(xg,ww,label='{0} {1}'.format(j,self.files[j].split('/')[-1]))
                    plt.xlabel('pix X')
                    plt.ylabel('wavelength')
                    plt.legend(bbox_to_anchor=(1.04,1),loc='upper left',ncol=1)                     
        if method=='trace':
            for i in self.pairs:
                for j in self.pairs[i]:
                    yg = np.copy(self.meta[j]['YG'])
                    xg = np.copy(self.meta[j]['XG'])
                    if normalize:
                        xg -= self.meta[j]['XYREF'][0]
                        yg -= self.meta[j]['XYREF'][1]
                    plt.plot(xg,yg,label='{0} {1}'.format(j,self.files[j].split('/')[-1]))
                    plt.xlabel('pix x')
                    plt.ylabel('pix y')
                    plt.legend(bbox_to_anchor=(1.04,1),loc='upper left',ncol=1)
        if method=='clean':
            for i in self.pairs:
                for j in self.pairs[i]:
                    fig,ax = plt.subplots(1,2,figsize=(20,10))
                    xdata = fits.open(self.files[j])[self.meta[j]['EXT']].data
                    cleandata = self.meta[j]['CLEAN']
                    m = np.where(np.isfinite(xdata))
                    vmin,vmax=None,None
                    if scale[0]=='percentile':
                        vmin,vmax = np.percentile(xdata[m],scale[1]),np.percentile(xdata[m],scale[2])
                    elif scale[0]=='value':
                        vmin,vmax = scale[1],scale[2]
                    else:
                        print("Error: scale must be either percentile or value. Set to ('percentile',5.,95.).")
                        vmin,vmax = np.percentile(xdata[m],5.),np.percentile(xdata[m],95.)
                    ax[0].imshow(xdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                    ax[1].imshow(cleandata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                    ax[0].set_title('{0} {1}'.format(j,self.files[j].split('/')[-1]))
                    ax[1].set_title('clean')
                    if traceon:
                        xg = self.meta[j]['XG']
                        yg = self.meta[j]['YG']
                        ax[0].plot(xg,yg,color='red',label='trace')
                        ax[1].plot(xg,yg,color='red',label='trace')
                        plt.legend()
                    if zoom:
                        xmin = self.meta[j]['XG'].min() - dx
                        xmax = self.meta[j]['XG'].max() + dx + 1
                        ax[0].set_xlim(xmin,xmax)
                        ax[1].set_xlim(xmin,xmax)
                        ymin = self.meta[j]['YG'].min() - dy
                        ymax = self.meta[j]['YG'].max() + dy + 1
                        ax[0].set_ylim(ymin,ymax)
                        ax[1].set_ylim(ymin,ymax)
        if method=='flam':
            for i in self.pairs:
                plt.figure(figsize=(10,10))
                for j in self.pairs[i]:
                    flam = self.meta[j]['FLAM']
                    flamunit = self.meta[j]['FLAMUNIT']
                    ww = self.meta[j]['WW']
                    wwunit = self.meta[j]['WWUNIT']
                    if not xmin:
                        xmin = np.min(ww)
                    if not xmax:
                        xmax = np.max(ww)
                    mask = np.where((ww>=xmin) & (ww<=xmax))
                    plt.plot(ww[mask],flam[mask],label='{0} {1}'.format(j,self.files[j].split('/')[-1]))
                plt.ylabel('{0}'.format(flamunit))
                plt.xlabel('{0}'.format(wwunit))
                if ylog:
                    plt.yscale('log')
                if ymin or ymax:
                    ymin = np.min(flam[mask]) if not ymin else ymin
                    ymax = np.max(flam[mask]) if not ymax else ymax
                    plt.ylim(ymin,ymax)
                plt.legend(bbox_to_anchor=(1.04,1),loc='upper left',ncol=1) 
        if method=='bkglocal':
            for i in self.gid:
                fig,ax = plt.subplots(1,3,figsize=(30,10))
                data = self.meta[i]['CLEAN']
                bkglocal = self.meta[i]['BKG_LOCAL']['VAL']
                corner = self.meta[i]['BKG_LOCAL']['PARAMS']['corner']
                shape = self.meta[i]['BKG_LOCAL']['PARAMS']['shape']
                stampdata = data[corner[1]:corner[1]+shape[0],corner[0]:corner[0]+shape[1]]
                m = np.where(np.isfinite(stampdata))
                vmin,vmax = np.percentile(stampdata[m],5.),np.percentile(stampdata[m],95.)
                ax[0].imshow(stampdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                ax[1].imshow(bkglocal,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                sub = stampdata - bkglocal
                ax[2].imshow(sub,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
        if method=='drz':
            for i in self.drz.meta:
                x = self.drz.meta[i]
                xdata = x['CLEAN']
                plt.figure(figsize=(10,10))
                m = np.where(np.isfinite(xdata))
                vmin,vmax=np.percentile(xdata[m],5.),np.percentile(xdata[m],95.)
                plt.imshow(x['CLEAN'],origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                plt.plot(x['XG'],x['YG'],color='red')
                plt.scatter(*x['XYREF'],color='red')
    ####################
    ####################
    ####################                
    def make_localbkg(self,method=(['polynomial','1d'],[3,3.]),apsize=(6,10),maskin=[0],show=False):
        for i in self.gid:
            xg = self.meta[i]['XG'].astype(int)
            yg = self.meta[i]['YG'].astype(int)
            xmin,xmax = min(xg),max(xg)
            yminout,yminin = min(yg)-apsize[1],min(yg)-apsize[0]
            ymaxout,ymaxin = max(yg)+apsize[1],max(yg)+apsize[0]
            data = copy.deepcopy(self.meta[i]['CLEAN'])
            dq = copy.deepcopy(fits.open(self.meta[i]['FILE'])[('DQ',self.meta[i]['EXT'][1])].data)
            stampdata = copy.deepcopy(data[yminout:ymaxout+1,xmin:xmax+1])
            stampdq = copy.deepcopy(dq[yminout:ymaxout+1,xmin:xmax+1])
            ### make mask ###
            mask = DQMask(maskin)
            mask.make_mask(stampdq)
            tmp = np.full_like(mask.mask,True,dtype=bool)
            shape = tmp.shape
            a = apsize[1] - apsize[0] + 1
            b = shape[0] - a
            tmp[a:b,:] = False
            outmask = (mask.mask & tmp)
            #################
            ### method ###
            if method[0]==['polynomial','1d']:
                x = np.arange(0,shape[0])
                y = np.arange(0,shape[1])
                z = (stampdata * outmask)
                z[z<=0.] = np.nan
                deg,std = method[1][0],method[1][1]
                zfit = np.full_like(z,np.nan,dtype=float)
                for j in y:
                    tmpz = z[:,j].copy()
                    m = np.where(np.isfinite(tmpz))
                    init = np.zeros(deg+1,dtype=float)
                    init[0] = np.median(tmpz[m])
                    popt,pcov = curve_fit(GrismModel.polynomial1d,x[m],tmpz[m],p0=init)
                    zfit[:,j] = copy.deepcopy(GrismModel.polynomial1d(x,*popt))
                zfit2 = GrismModel.convolution_gauss2d(zfit,std)   
                self.meta[i]['BKG_LOCAL'] = {}
                self.meta[i]['BKG_LOCAL']['PARAMS'] = {'corner':(xmin,yminout),'shape':zfit2.shape,'conf':(method,apsize,maskin)}
                self.meta[i]['BKG_LOCAL']['VAL'] = copy.deepcopy(zfit2)
        if show:
            self.show(method='bkglocal')
