import numpy as np
from scipy.signal import residue, residuez
from scipy.special import factorial
from rwth_nb.misc.signals import eps, find_ind_least_diff, unitstep


def dft(s, fs, NFFT=0):
    """Calculate discrete fourier transform of vector s

        Parameters
        ----------
        s : array_like
            vector to be transformed
        fs : float
            sampling frequency, is used to calculate frequency vector f
        NFFT : float, optional
            number of frequency coefficients

        Returns
        -------
        S : ndarray
            resulting discrete fourier transform
        f : ndarray
            frequency vector

        Examples
        --------
        For examples see primer at rwth_nb/RWTH Transforms.ipynb
        """
    if NFFT==0: 
        NFFT = len(s) # int(2**np.ceil(np.log2(len(bla))))
    
    S = np.fft.fftshift(np.fft.fft(s, NFFT))/NFFT
    f = np.linspace(-fs/2,fs/2, NFFT)
    
    return S, f


def idft(S, Ntime=0, NFFT=0):
    """Calculate inverse discrete fourier transform of vector S

        Parameters
        ----------
        S : array_like
            vector to be transformed
        Ntime : float, optional
            number of time bins, is used to crop the output of NumPy's ifft function
        NFFT : float, optional
            number of frequency coefficients

        Returns
        -------
        s : ndarray
            resulting inverse discrete fourier transform

        Examples
        --------
        For examples see primer at rwth_nb/RWTH Transforms.ipynb
    """
    if NFFT == 0: NFFT = len(S)
    
    s = np.fft.ifft(np.fft.ifftshift(S*NFFT), NFFT)
    
    if not Ntime == 0:
        s = s[0:Ntime]
    
    return s


def ilaplace_ht(t=np.linspace(-6, 6, num=1024), H0=1, pp=np.array([]), pz=np.array([]), ord_p=np.array([]),
                     ord_z=np.array([]), roc=[-12, 12]):
    """Calculate inverse laplace transform h(t) of H(p) defined by its gain factor, poles and zeroes

        Parameters
        ----------
        t : array_like
            array of t-domain to be transformed to
        H0 : float
            gain factor
        pp : array_like
            poles on pz-plane
            (exclude conjugated poles)
        pz : array_like
            zeroes on pz-plane
            (exclude conjugated zeroes)
        ord_p : array_like
            poles' orders
        ord_z : array_like
            zeroes' orders
        roc : array_like
            region of convergence
            (range from -infinity to infinity)

        Returns
        -------
        h : ndarray
            calculated inverse Laplace-transform according to t-domain
        td: ndarray
            dirac's x coordinate if existing, empty otherwise
        sd: ndarray
            dirac's gain factor if existing, empty otherwise

        Examples
        --------
        Calculate inverse Laplace-transform with gain H0 = 1
            poles:
                p_p1 = -3 (order 1)
                p_p2 = +1 (order 2)
            zeroes:
                p_n1 = 0 (order 1)
            region of convergence:
                1 to infinity

        >>> from rwth_nb.misc.transforms import ilaplace_ht
        >>>
        >>> t = numpy.linspace(-5, 5, 1024)
        >>> H0 = 1
        >>> poles = [-3, 1]
        >>> poles_order = [1, 2]
        >>> zeroes = [0]
        >>> zeroes_order = [1]
        >>> roc = [1, numpy.inf]
        >>>
        >>> h_t, td, sd = ilaplace_ht(t, H0, poles, zeroes, poles_order, zeroes_order, roc)

        For more examples see primer at rwth_nb/RWTH Transforms.ipynb
        """
    # check for correct input
    pp = np.array(pp)
    pz = np.array(pz)
    ord_p = np.array(ord_p)
    ord_z = np.array(ord_z)

    if pp.size != ord_p.size or pz.size != ord_z.size:
        raise ValueError('Poles/Zeroes array must be of the same size as their orders.')

    if np.any(np.logical_and(roc[0] < np.real(pp), np.real(pp) < roc[1])):
        raise ValueError('The ROC cannot contain any poles.')

    # declare arrays for dirac delta function
    td = sd = np.array([])

    # append conjugated poles and zeroes and their orders to existing arrays
    poles = np.array([])
    for ind, p in enumerate(pp):
        for i in range(0, ord_p[ind]):
            poles = np.append(poles, p)

    zeroes = np.array([])
    for ind, p in enumerate(pz):
        for i in range(0, ord_z[ind]):
            zeroes = np.append(zeroes, p)

    poles = np.append(poles, np.conj(poles[np.where(poles.imag != 0)]))
    zeroes = np.append(zeroes, np.conj(zeroes[np.where(zeroes.imag != 0)]))

    # configure numerator and denominator for partial fraction
    numerator = H0 * np.poly(zeroes)
    denominator = np.poly(poles)

    if poles.size >= zeroes.size:

        r, p, k = residue(numerator, denominator)

        # round decimals
        r = np.around(r, 5)
        p = np.around(p, 5)

        # determine (anti-)causal poles
        causal = np.real(p) <= roc[0]

        # alpha = -p
        p = -p

        # inverse laplace transform
        h = np.zeros(t.shape)
        n = 1
        for ind, alpha in enumerate(p):
            # determine order
            if ind > 0:
                if p[ind] == p[ind - 1]:
                    n += 1
                else:
                    n = 1

            coeff = r[ind] * np.exp(-alpha * t) * t ** (n - 1) / factorial(n - 1)

            if causal[ind]:  # if pole is causal
                tmp = coeff * unitstep(t)
            else:
                tmp = (-1) * coeff * unitstep(-t - 0.0001)

            h = np.add(h, tmp)

        # add rest as k[0] * delta(t)
        if k.size > 0:
            td = np.array([0])
            sd = np.array([k[0]])

    else:
        # Zaehlergrad größer als Nennergrad. Keine Partialbruchzerlegung möglich
        h = np.ones(t.shape) * np.nan

    return h, td, sd


def ilaplace_Hf(f=np.linspace(-6, 6, num=1024), H0=1, pp=np.array([]), pz=np.array([]), ord_p=np.array([]),
                     ord_z=np.array([]), dB=False):
    """Calculate frequency response H(f) of H(p) defined by its gain factor, poles and zeroes

        Parameters
        ----------
        f : array_like
            array of f-domain to be transformed to
        H0 : float
            gain factor
        pp : array_like
            poles on pz-plane
            (exclude conjugated poles)
        pz : array_like
            zeroes on pz-plane
            (exclude conjugated zeroes)
        ord_p : array_like
            poles' orders
        ord_z : array_like
            zeroes' orders
        dB : bool
            return frq response in dB if true

        Returns
        -------
        _ : ndarray
            calculated frequency response (in dB if parameter dB is true)

        Examples
        --------
        Calculate frequency response of H(p) with gain H0 = 1
            poles:
                p_p1 = +j, -j (order 1) Note: Exclude conjugated poles!
            zeroes:
                p_n1 = 0 (order 1)
        and return in dB

        >>> from rwth_nb.misc.transforms import ilaplace_Hf
        >>>
        >>> f = numpy.linspace(-6, 6, 1024)
        >>> H0 = 1
        >>> poles = [1j]  # Exclude conjugated pole
        >>> poles_order = [1]
        >>> zeroes = [0]
        >>> zeroes_order = [1]
        >>> dB = True
        >>>
        >>> H_f = ilaplace_Hf(f, H0, poles, zeroes, poles_order, zeroes_order, dB)

        For more examples see primer at rwth_nb/RWTH Transforms.ipynb
        """

    numerator = H0 * np.ones(f.shape)

    for ind, ppz in enumerate(pz):
        for _ in range(1, ord_z[ind] + 1):
            numerator = numerator * (1j * f - ppz)
            if np.abs(np.imag(ppz)):
                numerator = numerator * (1j * f - np.conj(ppz))

    denominator = np.ones(f.shape)

    for ind, ppp in enumerate(pp):
        for _ in range(1, ord_p[ind] + 1):
            denominator = denominator * (1j * f - ppp)
            if np.abs(np.imag(ppp)):
                denominator = denominator * (1j * f - np.conj(ppp))
    if dB:
        return 20 * np.log10(np.maximum(eps, np.abs(numerator / denominator)))
    else:
        return np.abs(numerator / denominator)


def iz_hn(n=np.linspace(-6, 6, num=13), H0=1, pp=np.array([]), pz=np.array([]), ord_p=np.array([]),
               ord_z=np.array([]), roc=[0, 12]):
    """Calculate inverse z-transform h(n) of H(z) defined by its gain factor, poles and zeroes

    Parameters
    ----------
    n : array_like
        array of n-domain to be transformed to
    H0 : float
        gain factor
    pp : array_like
        poles on pz-plane
        (exclude conjugated poles)
    pz : array_like
        zeroes on pz-plane
        (exclude conjugated zeroes)
    ord_p : array_like
        poles' orders
    ord_z : array_like
        zeroes' orders
    roc : array_like
        region of convergence
        (range from 0 to infinity)

    Returns
    -------
    h : ndarray
        calculated inverse z-transform according to n-domain

    Examples
    --------
    Calculate inverse z-transform with gain H0 = 1
        poles:
            z_p1 = +0.5 (order 1)
            z_p2 = +1 (order 2)
        zeroes:
            z_n1 = +2 (order 1)
        region of convergence:
            0.5 to 1

    >>> from rwth_nb.misc.transforms import iz_hn
    >>>
    >>> n = [-3, -2, -1, 0, 1, 2, 3]
    >>> H0 = 1
    >>> poles = [0.5, 1]
    >>> poles_order = [1, 2]
    >>> zeroes = [2]
    >>> zeroes_order = [1]
    >>> roc = [0.5, 1]
    >>>
    >>> h_n = iz_hn(n, H0, poles, zeroes, poles_order, zeroes_order, roc)

    """
    # check for correct input
    pp = np.array(pp)
    pz = np.array(pz)
    ord_p = np.array(ord_p)
    ord_z = np.array(ord_z)

    if np.isinf(roc[0]):
        raise ValueError('Region of convergence must start at 0 or pole (=[0, b] anti-causal or =[b, inf] causal).')

    if pp.size != ord_p.size or pz.size != ord_z.size:
        raise ValueError('Poles/Zeroes array must be of the same size as their orders.')

    # append conjugated poles and zeroes and their orders to existing arrays
    poles = np.array([])
    for ind, p in enumerate(pp):
        for i in range(0, ord_p[ind]):
            poles = np.append(poles, p)

    zeroes = np.array([])
    for ind, p in enumerate(pz):
        for i in range(0, ord_z[ind]):
            zeroes = np.append(zeroes, p)

    poles = np.append(poles, np.conj(poles[np.where(poles.imag != 0)]))
    zeroes = np.append(zeroes, np.conj(zeroes[np.where(zeroes.imag != 0)]))

    if poles.size >= zeroes.size:
        # configure numerator and denominator for partial fraction
        numerator = H0 * np.poly(zeroes)
        denominator = np.poly(poles)
        for i in range(0, int(poles.size - zeroes.size)):
            numerator = np.insert(numerator, 0, 0)

        # calculate residue
        r, p, k = residuez(numerator, denominator)

        # round decimals
        r = np.around(r, 5)
        p = np.around(p, 5)

        # determine (anti-)causal poles
        causal = np.around(np.abs(p), 5) <= np.abs(roc[0])

        # inverse z-transform
        h = np.zeros(n.shape)
        m = 1
        for ind, b in enumerate(p):
            # determine order
            if ind > 0:
                if p[ind] == p[ind-1]:
                    m += 1
                else:
                    m = 1

            coeff = 1
            for i in range(1, m):
                coeff *= (n + i) / factorial(m - 1)
            coeff = r[ind] * coeff * b**n

            if causal[ind]:  # if pole is causal
                tmp = coeff * unitstep(n)
            else:
                tmp = (-1) * coeff * unitstep(-n - m)

            h = np.add(h, tmp)

        # add k[i] * z**(-i) as k[i] * delta(n-i) to h(n)
        if k.size > 0:
            for ind, kk in enumerate(k):
                h = np.add(h, kk * np.where(n == ind, 1, 0))
    else:
        # partial fraction not possible: return nan array
        h = np.ones(n.shape) * np.nan

    return h


def iz_Hf(f=np.linspace(-6, 6, num=1024), H0=1, pp=np.array([]), pz=np.array([]), ord_p=np.array([]),
                     ord_z=np.array([]), dB=False):
    """Calculate frequency response H(f) of z-transformed H(z) defined by its gain factor, poles and zeroes

        Parameters
        ----------
        f : array_like
            array of f-domain to be transformed to
        H0 : float
            gain factor
        pp : array_like
            poles on pz-plane
            (exclude conjugated poles)
        pz : array_like
            zeroes on pz-plane
            (exclude conjugated zeroes)
        ord_p : array_like
            poles' orders
        ord_z : array_like
            zeroes' orders
        dB : bool
            return frq response in dB if true

        Returns
        -------
        _ : ndarray
            calculated frequency response (in dB if parameter dB is true)

        Examples
        --------
        Calculate frequency response of H(z) with gain H0 = 1
            poles:
                z_p1/2 = +j, -j (order 1) Note: Exclude conjugated poles!
            zeroes:
                z_n1 = 0 (order 1)
        and return in dB

        >>> from rwth_nb.misc.transforms import iz_Hf
        >>>
        >>> f = numpy.linspace(-6, 6, 1024)
        >>> H0 = 1
        >>> poles = [1j]  # Exclude conjugated pole
        >>> poles_order = [1]
        >>> zeroes = [0]
        >>> zeroes_order = [1]
        >>> dB = True
        >>>
        >>> H_f = iz_Hf(f, H0, poles, zeroes, poles_order, zeroes_order, dB)

        For more examples see primer at rwth_nb/RWTH Transforms.ipynb
        """
    numerator = H0 * np.ones(f.shape)

    for ind, ppz in enumerate(pz):
        for _ in range(1, ord_z[ind] + 1):
            numerator = numerator * (np.exp(1j * 2 * np.pi * f) - ppz)
            if np.abs(np.imag(ppz)):
                numerator = numerator * (np.exp(1j * 2 * np.pi * f) - np.conj(ppz))

    denominator = np.ones(f.shape)

    for ind, ppp in enumerate(pp):
        for _ in range(1, ord_p[ind] + 1):
            denominator = denominator * (np.exp(1j * 2 * np.pi * f) - ppp)
            if np.abs(np.imag(ppp)):
                denominator = denominator * (np.exp(1j * 2 * np.pi * f) - np.conj(ppp))
    if dB:
        return 20 * np.log10(np.maximum(eps, np.abs(numerator / denominator)))
    else:
        return np.abs(numerator / denominator)


def ideal_sample(x, y, T):
    def x_mirrored_around_zero(maxval, inc=1):
        x = np.arange(inc, maxval + inc, inc)
        return np.r_[-x[::-1], 0, x]
    xf = x_mirrored_around_zero(np.amax(x), T)
    yf = y[find_ind_least_diff(x, xf)]
    return xf, yf


def real_sample(x, y, T, T0):
    yf = np.zeros(x.shape)
    indices = np.where(np.mod(x + T0 / 2, T) <= T0)
    yf[indices[0]] = y[indices[0]]
    return x, yf


def sample(x, y, T, T0=0):
    if T0:
        return real_sample(x, y, T, T0)
    else:
        return ideal_sample(x, y, T)
