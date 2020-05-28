def mag2flux(mag,wave):
    import numpy as np
    return 10**(-0.4 * (mag + 2.406 + 5.*np.log10(wave)))