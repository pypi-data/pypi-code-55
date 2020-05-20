from scipy import signal  # butter


def butter(cutoff, fs, order=5, type='Tiefpass', fdelta=0):
    """Butterworth Filter of order n

        Parameters
        ----------
        cutoff : float
            cutoff frequency
        fs : float
            sampling frequency, is used to calculate nyquist frequency
        order : float, optional
            order of filter
        type: {'Tiefpass', 'Bandpass', 'Hochpass'}, optional
            type of filter.
        fdelta: float, optional
            bandwith of filter


        Returns
        -------
        b : ndarray
            numerator polynomial of the IIR filter
        a : ndarray
            denominator polynomial of the IIR filter

        """
    # bandpass type
    btypes = {'Tiefpass': 'lowpass', 'Bandpass': 'bandpass', 'Hochpass': 'highpass'}
    btype = btypes[type]

    # Nyquist frequency
    nyq = 0.5 * fs

    if btype == 'bandpass':
        # normalized min and max frequency
        normal_min = (cutoff-fdelta/2) / nyq
        normal_max = (cutoff+fdelta/2) / nyq
        # normalized cutoff-frequency
        normal_cutoff = [normal_min, normal_max]
    else:
        # normalized cutoff-frequency
        normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype=btype, analog=False)  # coefficients in z-domain
    return b, a


# Shortcuts
def butter_bandpass(f0, fdelta, fs, order=5):
    """Bandpass Butterworth Filter

    This filter is set as a bandpass filter with f0, fdelta, fs and order set by user.

    See Also
    --------
    butter : Filter design using order and critical points

    """
    b, a = butter(f0, fs, order, 'Bandpass', fdelta)
    return b, a


def butter_lowpass(cutoff, fs, order=5):
    """Lowpass Butterworth Filter

    This filter is set as a lowpass filter with cutoff, fs and order set by user.

    See Also
    --------
    butter : Filter design using order and critical points

    """
    b, a = butter(cutoff, fs, order, 'Tiefpass')
    return b, a


def butter_highpass(cutoff, fs, order=5):
    """Highpass Butterworth Filter

    This filter is set as a highpass filter with cutoff, fs and order set by user.

    See Also
    --------
    butter : Filter design using order and critical points

    """
    b, a = butter(cutoff, fs, order, 'Hochpass')
    return b, a


def filter(s, b, a):
    """Digital Filter
        
        Filter s(n) in z-Domain with filter coefficients a and b:
                            -1              -M
                b[0] + b[1]z  + ... + b[M] z
        G(z) = -------------------------------- S(z)
                            -1              -N
                a[0] + a[1]z  + ... + a[N] z

        Parameters
        ----------
        s : array_like
            n-dimensional input array
        b : array_like
            numerator coefficient vector in a 1-D sequence.
        a : array_like
            denominator coefficient vector in a 1-D sequence.

        Returns
        -------
        g : array
            output of digital filter.
    """
    g = signal.lfilter(b, a, s)
    return g
