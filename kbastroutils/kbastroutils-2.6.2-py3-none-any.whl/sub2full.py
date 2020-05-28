def sub2full(spt):
    """
    Example:
    coords = sub2full('ic5u01i2q_spt.fits')
    coords >>> [(0, 4095, 1282, 2049)]
    ----------
    sub2full.py is a function mapping a subarray image back to its full frame. The function returns four corners of in the full frame.
    Note: you can get ic5u01i2q_spt.fits used in the example from the MAST archive.
    Note: pixel index starts at (0,0).
    Note: this routine is modified from sub2full.py from wfc3tools (https://wfc3tools.readthedocs.io/en/latest/wfc3tools/sub2full.html). Therefore, this function works properly with HST/WFC3 data.
    ----------
    rootname_spt.fits associated to a science file (e.g., rootname_flt.fits) is the only input.
    """
    import os
    from astropy.io import fits
    import numpy as np
    
    coords = list()    
    uvis_x_size = 2051
    serial_over = 25.0
    ir_overscan = 5.0

    try:
        fd2 = fits.open(spt)
    except (ValueError, IOError) as e:
        raise ValueError('%s ' % (e))

    try:
        detector = fd2[0].header['SS_DTCTR']
        subarray = fd2[0].header['SS_SUBAR']
        xcorner = int(fd2[1].header['XCORNER'])
        ycorner = int(fd2[1].header['YCORNER'])
        numrows = int(fd2[1].header['NUMROWS'])
        numcols = int(fd2[1].header['NUMCOLS'])
        fd2.close()
    except KeyError as e:
        raise KeyError("Required header keyword missing; %s" % (e))

    if "NO" in subarray:
        raise ValueError("Image is not a subarray: %s" % (f))

    sizaxis1 = numcols
    sizaxis2 = numrows

    if (xcorner == 0 and ycorner == 0):
        cornera1 = 0
        cornera2 = 0
        cornera1a = cornera1
        cornera1b = cornera1a + sizaxis1 - 1
        cornera2a = cornera2
        cornera2b = cornera2a + sizaxis2 - 1
    else:
        if 'UVIS' in detector:
            cornera1 = ycorner
            cornera2 = uvis_x_size - xcorner - sizaxis2
            if xcorner >= uvis_x_size:
                cornera2 = cornera2 + uvis_x_size

            cornera1a = cornera1 - serial_over
            cornera1b = cornera1a + sizaxis1 - 1
            cornera2a = cornera2
            cornera2b = cornera2a + sizaxis2 - 1
            
            if cornera1a < 0:
                cornera1a = 0
            if cornera1b > 4095:
                cornera1b = 4095

        else:
            cornera1 = ycorner - ir_overscan
            cornera2 = xcorner - ir_overscan
            cornera1a = cornera1
            cornera1b = cornera1a + sizaxis1 - 11
            cornera2a = cornera2
            cornera2b = cornera2a + sizaxis2 - 11

    coords.append((int(cornera1a), int(cornera1b), int(cornera2a),
                   int(cornera2b)))

    return coords