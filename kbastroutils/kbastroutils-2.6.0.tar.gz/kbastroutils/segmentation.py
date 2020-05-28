class Segmentation:
    """
    Example:
    file = 'abc.fits'
    x = Segmentation(file) >>> instantiate
    x.make_thr(do_mask=True) >>> make x.detect_thr container
    x.make_kernel() >>> make x.kernel container
    x.make_segmentation(do_mask=True,do_kernel=True,do_deblend=True) >>> make x.segmentation container
    x.make_properties() >>> make x.properties from x.segmentation
    x.properties.to_table() >>> show properties
    ----------
    Segmentation is a wrapper for making a segmentation map. This includes:
        - taking data from .fits file with ['SCI'] and ['DQ'] extensions
        - creating mask using dqmask.py
        - detecting sources using threshold algorithm, smoothing kernel, and mask
    ----------
    Ref:
        - Image Segmentation: https://photutils.readthedocs.io/en/stable/segmentation.html
    """
    def __init__(self,file):
        from astropy.io import fits
        from kbastroutils.dqmask import DQMask
        from kbastroutils.container import Container
        self.name = file
        self.data = fits.open(file)['SCI'].data
        self.mask = DQMask()
        self.mask.make_mask(fits.open(file)['DQ'].data)
        self.detect_thr = Container(keys={'params','value'})
        self.detect_thr.params = Container({'nsigma','do_mask'})
        self.kernel = Container(keys={'method','params','value'})
        self.segmentation = Container(keys={'params','value'})
        self.segmentation.params = Container(keys={'npixels','nlevels','contrast'
                                              ,'do_mask','do_kernel','do_deblend'})
        self.properties = None
        self.phot = None
################################################################        
    def make_thr(self,nsigma=None,do_mask=None):
        """
        make a threshold array for source detection
        """
        from photutils import detect_threshold
        if nsigma:
            self.detect_thr.params.nsigma = nsigma
        if not self.detect_thr.params.nsigma:
            self.detect_thr.params.nsigma = 2.
        if do_mask:
            self.detect_thr.params.do_mask = do_mask
        if not self.detect_thr.params.do_mask:
            self.detect_thr.params.do_mask = False

        data = self.data
        nsigma = self.detect_thr.params.nsigma
        mask = None
        if self.detect_thr.params.do_mask:
            mask = ~self.mask.mask
            
        self.detect_thr.value = detect_threshold(data,nsigma=nsigma,mask=mask)
################################################################        
    def make_kernel(self,method=None,params=None):
        """
        make a smoothing kernel for source detection
        Note: only method='Gaussian2D' is available
        """
        from kbastroutils.container import Container
        if method:
            self.kernel.method = method
        if not self.kernel.method:
            self.kernel.method = 'Gaussian2D'
            
        if self.kernel.method=='Gaussian2D':
            from astropy.convolution import Gaussian2DKernel
            from astropy.stats import gaussian_fwhm_to_sigma as F2S
            default_pars = {'fwhm':3.
                            ,'x_size':5
                            ,'y_size':5}
            pars = default_pars
            if params:
                for i in default_pars.keys():
                    try:
                        pars[i] = params[i]
                    except:
                        pass
            self.kernel.params = Container(keys=list(pars.keys()),values=list(pars.values()))
            
            fwhm = self.kernel.params.fwhm
            x_size = self.kernel.params.x_size
            y_size = self.kernel.params.y_size
            
            self.kernel.value = Gaussian2DKernel(fwhm*F2S,x_size=x_size,y_size=y_size,).normalize()    
            
        else:
            print("Only method='Gaussian2D' is available.")
################################################################        
    def make_segmentation(self,npixels=None,nlevels=None,contrast=None
                          ,do_mask=None,do_kernel=None,do_deblend=None):
        """
        make a segmentation map given a threshold array (from Segmentation.make_thr), a kernel (from Segmentation.make_kernel), and a mask (from DQMask.make_mask).
        deblending of sources is implemented.
        ----------
        Ref:
            - Image Segmentation: https://photutils.readthedocs.io/en/stable/segmentation.html
        """
        from photutils import detect_sources, deblend_sources
        if npixels:
            self.segmentation.params.npixels = npixels
        if not self.segmentation.params.npixels:
            self.segmentation.params.npixels = 5
        if nlevels:
            self.segmentation.params.nlevels = nlevels
        if not self.segmentation.params.nlevels:
            self.segmentation.params.nlevels = 32
        if contrast:
            self.segmentation.params.contrast = contrast
        if not self.segmentation.params.contrast:
            self.segmentation.params.contrast = 1e-3
        if do_mask:
            self.segmentation.params.do_mask = do_mask
        if not self.segmentation.params.do_mask:
            self.segmentation.params.do_mask = False
        if do_kernel:
            self.segmentation.params.do_kernel = do_kernel
        if not self.segmentation.params.do_kernel:
            self.segmentation.params.do_kernel = False
        if do_deblend:
            self.segmentation.params.do_deblend = do_deblend
        if not self.segmentation.params.do_deblend:
            self.segmentation.params.do_deblend = False
            
        data = self.data
        thr = self.detect_thr.value
        npixels = self.segmentation.params.npixels
        nlevels = self.segmentation.params.nlevels
        contrast = self.segmentation.params.contrast
        mask = None
        if self.segmentation.params.do_mask:
            mask = ~self.mask.mask
        kernel = None
        if self.segmentation.params.do_kernel:
            kernel = self.kernel.value
            
        self.segmentation.value = detect_sources(data,thr,npixels=npixels,filter_kernel=kernel,mask=mask)
        if self.segmentation.params.do_deblend:
            self.segmentation.value = deblend_sources(data,self.segmentation.value
                                                      ,npixels=npixels,filter_kernel=kernel
                                                      ,nlevels=nlevels,contrast=contrast)
################################################################        
    def make_properties(self):
        """
        characterize source properties given a segmentation map (from Segmentation.make_segmentation)
        """
        from photutils import source_properties
        data = self.data
        segmentation = self.segmentation.value
        self.properties = source_properties(data,segmentation)
        