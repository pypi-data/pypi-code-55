import numpy as np
from astropy.convolution import Gaussian2DKernel,convolve
class GrismModel:
    def poly2ddeg3(x,y,p):
        X,Y = np.meshgrid(x,y,copy=True)
        Z = p[0] + \
            p[1]*X + p[2]*Y + \
            p[3]*X**2 + p[4]*X*Y + p[5]*Y**2 + \
            p[6]*X**3 + p[7]*(X**2)*Y + p[8]*X*(Y**2) + p[9]*Y**3
        return(Z)
    def convolution_gauss2d(img,std=1.):
        kernel = Gaussian2DKernel(x_stddev=std)
        out = convolve(img,kernel)
        return out
    def polynomial1d(x,*p):
        deg = len(p)-1
        out = np.full_like(x,0.,dtype=float)
        for i in np.arange(0,deg+1):
            out += p[i]*x**i
        return out