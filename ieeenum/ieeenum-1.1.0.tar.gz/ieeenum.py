from cmath import nan,nanj,inf,infj,isnan,isinf
ninf=-inf
ninfj=complex(imag=ninf)
def isinfj(x,/):
    '''return isinf(x.imag)'''
    return isinf(x.imag)
def isnanj(x,/):
    '''return isnan(x.imag)'''
    return isnan(x.imag)
def isninf(x,/):
    '''return isinf(-x) if (x.imag<0 or x<0) else False'''
    return isinf(-x) if (x.imag<0 or x<0) else False
def isninfj(x,/):
    '''return isninf(x.imag)'''
    return isninf(x.imag)
