# -*- coding: utf8 -*-
# python 3
# (C) Fabrice Sincère

"""An educational module about linear AC electrical circuits"""

import sys
import math
import cmath
import inspect  # isfunction()
import csv
import random
try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import *  # Slider, Button...
    _matplotlib_available = True
except ImportError:
    _matplotlib_available = False
    print("Warning : you should install matplotlib to draw Bode plot")

__version__ = (0, 4, 5)
__author__ = "Fabrice Sincère <fabrice.sincere@ac-grenoble.fr>"

"""Release History
0.4.4 : add widgets back-end
0.4.3 : add plot data cursors, bode_real(), bode_imag(), bode_var()...
0.4.2 : add Bode datas saved in csv file
0.4.1 : add DEFAULT_FREQUENCY
0.4.0 : first publication to pypi (2020-05)
[...]
0.0.1 : initial release (2018-10)
"""

if sys.version_info[0] < 3:
    print('You need to run this with Python 3')
    exit(1)


def PrefixNotation(significand, prefix=''):
    """significand -> float
prefix  -> str
return the corresponding decimal number -> float

prefix is one of :
'p' pico, 'n', 'u' or 'µ' micro, 'm', 'k', 'M' mega, 'G', 'T', '' default

>>> from acelectricity import *
>>> PrefixNotation(0.05, 'M')  # 50000
>>> PrefixNotation(50, 'k')  # 50000
>>> PrefixNotation(10000)    # 10000
"""
    prefixes = {'': 1, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'µ': 1e-6,
                'm': 1e-3, 'k': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12}

    return significand * prefixes[prefix]


def EngineeringNotation(value):
    """value -> float

Return a tuple (significand, prefix)
with significand between 1 and 1000

significand -> float
prefix  -> str

prefix is one of :
'p' pico, 'n', 'u' or 'µ' micro, 'm', 'k', 'M' mega, 'G', 'T', '' default

>>> from acelectricity import *
>>> EngineeringNotation(999)    #  (999, '')
>>> EngineeringNotation(1000)   #  (1.0, 'k')
>>> EngineeringNotation(-1e-6)  #  (-1.0, 'µ')
>>> EngineeringNotation(0)      #  (0, '')
"""
    if value == 0.0:
        return (0, '')

    nbdecimal = math.log10(abs(value))

    if -15.0 <= nbdecimal < -9.0:
        return (value*1e12, 'p')
    elif -9.0 <= nbdecimal < -6.0:
        return (value*1e9, 'n')
    elif -6.0 <= nbdecimal < -3.0:
        return (value*1e6, 'µ')
    elif -3.0 <= nbdecimal < 0.0:
        return (value*1e3, 'm')
    elif 0.0 <= nbdecimal < 3.0:
        return (value, '')
    elif 3.0 <= nbdecimal < 6.0:
        return (value*1e-3, 'k')
    elif 6.0 <= nbdecimal < 9.0:
        return (value*1e-6, 'M')
    elif 9.0 <= nbdecimal < 12.0:
        return (value*1e-9, 'G')
    elif 12.0 <= nbdecimal < 15.0:
        return (value*1e-12, 'T')
    else:
        return (value, '')  # scientific notation


def getfrequency(value, unit):
    """return tuple (frequency, angular frequency)
value : positive float
unit : prefix + 'Hz' or 'rad/s'
prefix is one of :
'p' pico, 'n', 'u' or 'µ' micro, 'm', 'k', 'M' mega, 'G', 'T', '' default

frequency in Hz
angular frequency in rad/s

>>> getfrequency(1000, 'Hz')
(1000, 6283.185307179586)
>>> getfrequency(1, 'kHz')
(1000, 6283.185307179586)
>>> getfrequency(1000, 'rad/s')
(159.15494309189535, 1000)
"""
    if isinstance(value, (int, float)):
        if value < 0:
            raise ValueError("value must be positive")
        if unit[-2:] == "Hz":
            prefix = '' if unit == "Hz" else unit[0:-2]
            frequency = PrefixNotation(value, prefix)
            angularfrequency = frequency*2*math.pi
            return (frequency, angularfrequency)
        if unit[-5:] == "rad/s":
            prefix = '' if unit == "rad/s" else unit[0:-5]
            angularfrequency = PrefixNotation(value, prefix)
            frequency = angularfrequency/(2*math.pi)
            return (frequency, angularfrequency)
        raise ValueError("unit must be Hz or rad/s")
    raise TypeError("number expected")


def compare(a, b):
    """a, b : Impedance, Admittance, Current, Voltage, Power or Ratio instances.
Return True if complex functions are close in value, and False otherwise.
>>> Z1 = Impedance(r=100)
>>> Z2 = Impedance(r=2200)
>>> Z3 = Impedance(r=2300)
>>> compare(Z1+Z2, Z3)
True
>>> compare(1/Z1+1/Z2, 1/Z3)
False
>>> ZL = Impedance(l=0.1)
>>> compare(Z1+ZL, Impedance(fw=lambda w: 100+0.1j*w))
True
"""
    def isclose(x, y, tol=1e-9):
        """x, y : float
Return True if x is close in value to y, and False otherwise
Note : cmath.isclose() only for python >=3.5"""
        if x == 0 or y == 0:
            if abs(x-y) < tol:
                return True
            return False
        else:
            if abs((x-y)/x) < tol:
                return True
            return False

    for i in range(10):
        frequency = 10**random.uniform(-2, 9)
        complex1 = a.fw(frequency, unit='Hz')
        real1, imag1 = complex1.real, complex1.imag
        complex2 = b.fw(frequency, unit='Hz')
        real2, imag2 = complex2.real, complex2.imag
        if not isclose(real1, real2):
            return False
        if not isclose(imag1, imag2):
            return False
    return True


def show():
    """Display all figures.
In non-interactive mode, display all figures and block until
the figures have been closed."""
    if not _matplotlib_available:
        print("You should install matplotlib to draw Bode plot")
        return
    plt.show()


class Wfunction:
    """ Wfunction class provides tools for complex mathematical functions \
w -> f(w) (for internal usage only)."""

    def __init__(self, func):
        """func is a function from a positive real number \
(angular frequency in rad/s) to a complex number.
func represents a complex voltage, current, power, impedance, admittance, \
ratio or transfer function"""

        if inspect.isfunction(func):
            self.func = func
        else:
            raise TypeError("function expected")

    def __call__(self, value, unit='Hz'):
        """
value : positive float
unit : Hz or rad/s, with prefix :
one of 'p' pico, 'n', 'u' or 'µ' micro, 'm', 'k', 'M' mega, 'G', 'T', '' default
return self.func(angularfrequency)

>>> fw = Wfunction(func=lambda w: -1000j*w)
>>> fw(1000)  # Hz
-6283185.307179586j
>>> fw(1, 'kHz')
-6283185.307179586j
>>> fw(1000,'rad/s')
-1000000j
"""
        (frequency, angularfrequency) = getfrequency(value, unit=unit)
        return self.func(angularfrequency)

    def __add__(self, arg):
        """self.__add__(arg) <=> self + arg
arg -> Wfunction instance or complex number value
return Wfunction instance

>>> fw1 = Wfunction(lambda w: 0.1j*w)
>>> fw1(1000)  # Hz
628.3185307179587j
>>> fw2 = Wfunction(lambda w: -1e6j/w)
>>> fw2(1000)  # Hz
(-0-159.15494309189535j)
>>> fw = fw1 + fw2
>>> fw(1000)   # fw(w) = fw1(w) + fw2(w)
469.1635876260633j
>>> fw3 = fw + 500
>>> fw3(1000)  # fw3(w) = fw(w) + 500
(500+469.1635876260633j)
"""
        if isinstance(arg, Wfunction):
            return Wfunction(lambda w: self.func(w) + arg.func(w))
        if isinstance(arg, (int, float, complex)):
            return Wfunction(lambda w: self.func(w) + arg)
        raise TypeError("Wfunction instance or number expected")

    def __radd__(self, value):
        if isinstance(value, (int, float, complex)):
            return self.__add__(value)
        raise TypeError("number expected")

    def __sub__(self, arg):
        """self.__sub__(arg) <=> self - arg
arg -> Wfunction instance or complex number value
return Wfunction instance"""

        if isinstance(arg, Wfunction):
            return Wfunction(lambda w: self.func(w) - arg.func(w))
        if isinstance(arg, (int, float, complex)):
            return Wfunction(lambda w: self.func(w) - arg)
        raise TypeError("Wfunction instance or number expected")

    def __rsub__(self, value):
        if isinstance(value, (int, float, complex)):
            return Wfunction(lambda w: value - self.func(w))
        raise TypeError("number expected")

    def __pos__(self):
        return Wfunction(self.func)  # new instance

    def __neg__(self):
        return Wfunction(lambda w: -self.func(w))

    def __mul__(self, arg):
        """self.__mul__(arg) <=> self * arg
arg -> Wfunction instance or complex number value
return Wfunction instance"""
        if isinstance(arg, Wfunction):
            return Wfunction(lambda w: self.func(w) * arg.func(w))
        if isinstance(arg, (int, float, complex)):
            return Wfunction(lambda w: self.func(w) * arg)
        raise TypeError("Wfunction instance or number expected")

    def __rmul__(self, value):
        if isinstance(value, (int, float, complex)):
            return self.__mul__(value)
        raise TypeError("number expected")

    def __truediv__(self, arg):
        """self.__truediv__(arg) <=> self / arg
arg -> Wfunction instance or complex number value
return Wfunction instance"""
        if isinstance(arg, Wfunction):
            return Wfunction(lambda w: self.func(w) / arg.func(w))
        if isinstance(arg, (int, float, complex)):
            return Wfunction(lambda w: self.func(w) / arg)
        raise TypeError("Wfunction instance or number expected")

    def __rtruediv__(self, value):
        if isinstance(value, (int, float, complex)):
            return Wfunction(lambda w: value/self.func(w))
        raise TypeError("number expected")

    def conjugate(self):
        "return Wfunction instance with complex conjugate function"
        return Wfunction(lambda w: self.func(w).conjugate())

    def real(self):
        "return Wfunction instance with complex real part function"
        return Wfunction(lambda w: self.func(w).real)

    def imag(self):
        "return Wfunction instance with complex imaginary part function"
        return Wfunction(lambda w: self.func(w).imag)

    def abs(self):
        """return Wfunction instance with complex modulus (absolute value) function
>>> fw1 = Wfunction(lambda w: 100 + 0.1j*w)
>>> fw1(1000)  # Hz
(100+628.3185307179587j)
>>> fw2 = fw1.abs()
>>> fw2(1000)  # Hz
636.2265131567328
"""
        return Wfunction(lambda w: abs(self.func(w)))

    def phase_deg(self):
        "return Wfunction instance with complex argument (degrees) function"
        return Wfunction(lambda w: math.degrees(cmath.phase(self.func(w))))

    def phase_rad(self):
        "return Wfunction instance with complex argument (radians) function"
        return Wfunction(lambda w: cmath.phase(self.func(w)))

    def db(self):
        "return Wfunction instance with dB function (20*log10(absolute value))"
        return Wfunction(lambda w: 20*math.log10(abs(self.func(w))))

    def dbw(self):
        "return Wfunction instance with dBW function (10*log10(absolute value))"
        return Wfunction(lambda w: 10*math.log10(abs(self.func(w))))


class Component:
    "Component serves as a base class for Impedance and \
Admittance classes"

    def __init__(self):
        pass

    # from complex impedance Z = Rs +jX
    @staticmethod
    def get_parallel_conductance(rs, x):
        """x : reactance (ohm)
rs : series resistance (ohm)
return parallel conductance G (S) if not infinite"""
        if rs == 0 and x == 0:
            return None
        return rs/(rs*rs+x*x)

    # from complex impedance Z = Rs +jX
    @staticmethod
    def get_parallel_resistance(rs, x):
        """x : reactance (ohm)
rs : series resistance (ohm)
return parallel resistance Rp=1/G (ohm) if not infinite"""
        if rs == 0:
            return None
        return (rs*rs+x*x)/rs

    # from complex impedance Z = Rs +jX
    @staticmethod
    def get_susceptance(rs, x):
        """x : reactance (ohm)
rs : series resistance (ohm)
return susceptance B (S) if not infinite"""
        if rs == 0 and x == 0:
            return None
        return -x/(rs*rs+x*x)

    # from complex admittance Y = G +jB
    @staticmethod
    def get_series_resistance(g, b):
        """g : conductance (S)
b : susceptance (S)
return series resistance Rs (ohm) if not infinite"""
        if g == 0 and b == 0:
            return None
        return g/(g*g+b*b)

    # from complex admittance Y = G +jB
    @staticmethod
    def get_reactance(g, b):
        """g : conductance (S)
b : susceptance (S)
return reactance X (ohm) if not infinite"""
        if g == 0 and b == 0:
            return None
        return -b/(g*g+b*b)

    @staticmethod
    def get_series_capacitance(x, w):
        """x : reactance (ohm)
w : angular frequency (rad/s)
return series capacitance Cs (farad) if defined"""
        if x is None or x >= 0:
            return None
        return -1/(x*w)

    @staticmethod
    def get_series_inductance(x, w):
        """x : reactance (ohm)
w : angular frequency (rad/s)
return series inductance Ls (henry) if defined"""
        if x is None or x <= 0:
            return None
        return x/w

    @staticmethod
    def get_parallel_capacitance(b, w):
        """b : susceptance (siemens)
w : angular frequency (rad/s)
return parallel capacitance Cp (farad) if defined"""
        if b is None or b <= 0:
            return None
        return b/w

    @staticmethod
    def get_parallel_inductance(b, w):
        """b : susceptance (siemens)
w : angular frequency (rad/s)
return parallel inductance Lp (henry) if defined"""
        if b is None or b >= 0:
            return None
        return -1/(b*w)

    def bode(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
             xscale='log', yscale='linear',
             magnitude_label='Magnitude',
             phase_unit='degrees', title='Bode plot', filename=None,
             draw_phase=True, **kwarg):
        """Save datas and draw Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
phase_unit= ['degrees' | 'radians']
filename (str) : save datas to csv format file
draw_phase (bool)

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> Zc = Impedance(c=100e-9)
>>> Zc.bode(yscale='log', title='Zc frequency response', filename='zc.csv')
>>> Yc = 1/Zc
>>> Yc.bode(yscale='log', title='Yc frequency response', filename='yc.csv')
>>> show()
"""
        # attribut used here : self.unit

        if n < 10:
            raise ValueError('10 points minimum')

        # f = frequency (Hz) ; w = angular frequency (rad/s)
        if xmin > xmax:
            xmin, xmax = xmax, xmin
        if xmin < 0 or xmax < 0:
            raise ValueError("xmin and xmax must be positive")
        if xscale == 'log' and xmin == 0:
            xmin = xmax*1e-4  # 4 decades
            print("Warning : xmin (0) set to {}".format(xmin))
        (fmin, wmin) = getfrequency(value=xmin, unit=xunit)
        (fmax, wmax) = getfrequency(value=xmax, unit=xunit)

        unit = 'Hz' if 'Hz' in xunit else 'rad/s'

        # xvalues
        if xscale == 'log':
            if unit == 'Hz':
                xvalues = list(np.geomspace(fmin, fmax, n))
            elif unit == 'rad/s':
                xvalues = list(np.geomspace(wmin, wmax, n))
        elif xscale == 'linear':
            if unit == 'Hz':
                xvalues = list(np.linspace(fmin, fmax, n))
            elif unit == 'rad/s':
                xvalues = list(np.linspace(wmin, wmax, n))
        else:
            raise ValueError('log or linear expected')

        # magnitudes
        if isinstance(self, (Impedance, Admittance)):
            if 'mode' in kwarg:
                if kwarg['mode'] == 'real':
                    # bode_real()
                    magnitudes = [self.real(x, unit=unit) for x in xvalues]
                elif kwarg['mode'] == 'imag':
                    # bode_imag()
                    magnitudes = [self.imag(x, unit=unit) for x in xvalues]
                else:
                    raise ValueError('mode argument : real or imag expected')
            else:
                # bode()
                magnitudes = [self.abs(x, unit=unit) for x in xvalues]
        else:
            raise TypeError

        # phases
        if phase_unit == 'degrees':
            phases = [self.phase_deg(x, unit=unit) for x in xvalues]
        elif phase_unit == 'radians':
            phases = [self.phase_rad(x, unit=unit) for x in xvalues]
        else:
            raise ValueError('degrees or radians expected')

        # save datas to csv format file
        if filename is not None:
            with open(filename, 'w') as f:
                writer = csv.writer(f)
                if draw_phase:
                    for datas in zip(xvalues, magnitudes, phases):
                        writer.writerow(data for data in datas)
                else:
                    for datas in zip(xvalues, magnitudes):
                        writer.writerow(data for data in datas)
            print('Save datas to {} file [DONE]'.format(filename))

        # matplotlib
        if not _matplotlib_available:
            print("You should install matplotlib to draw Bode plot")
            return

        fig, ax1 = plt.subplots()
        fig.tight_layout()
        fig.subplots_adjust(left=0.15, bottom=0.1, right=0.85,
                            top=0.9, wspace=0.2, hspace=0.2)
        ax2 = ax1.twinx()
        ax2.set_visible(draw_phase)

        print("Plot figure {} {}".format(plt.get_fignums()[-1], title))
        if draw_phase:
            for i in zip(xvalues[:5], magnitudes[:5], phases[:5]):
                print("{:g} {:g} {:g}".format(*i))
            print("[...]")
            for i in zip(xvalues[-5:], magnitudes[-5:], phases[-5:]):
                print("{:g} {:g} {:g}".format(*i))
        else:
            for i in zip(xvalues[:5], magnitudes[:5]):
                print("{:g} {:g}".format(*i))
            print("[...]")
            for i in zip(xvalues[-5:], magnitudes[-5:]):
                print("{:g} {:g}".format(*i))

        def mouse_move(event):
            # draw cursors
            if not event.inaxes:
                txt.set_text('')
                lx.set_visible(False)
                ly.set_visible(False)
                lp.set_visible(False)
                ax1.figure.canvas.draw()
                ax2.figure.canvas.draw()
                return
            x, y = event.xdata, event.ydata
            indx = min(np.searchsorted(xvalues, x), len(xvalues) - 1)

            x = l1.get_xdata()[indx]
            y = l1.get_ydata()[indx]
            p = l2.get_ydata()[indx]

            # update the line positions
            lx.set_visible(True)
            ly.set_visible(True)
            lp.set_visible(True)

            lx.set_xdata(x)
            ly.set_ydata(y)
            lp.set_ydata(p)

            if draw_phase:
                txt.set_text('{:f} {}{}, {:f} {}{}, {:g} {}'.
                             format(*EngineeringNotation(x), unit,
                                    *EngineeringNotation(y), self.unit,
                                    p, phase_unit))
            else:
                txt.set_text('{:f} {}{}, {:f} {}{}'.
                             format(*EngineeringNotation(x), unit,
                                    *EngineeringNotation(y), self.unit))

            ax1.figure.canvas.draw()
            ax2.figure.canvas.draw()

        # cursors
        # x vertical line
        lx = ax1.axvline(color='k', linewidth=1, linestyle='--',
                         visible=False)
        # magnitude horizontal line
        ly = ax1.axhline(color='b', linewidth=1, linestyle='--',
                         visible=False)
        # phase horizontal line
        lp = ax2.axhline(color='r', linewidth=1, linestyle='--',
                         visible=False)
        # text location in axes coords
        txt = ax1.text(0.1, 0.95, '', transform=ax1.transAxes)

        if unit == 'Hz':
            ax1.set_xlabel('Frequency [Hz]')
        elif unit == 'rad/s':
            ax1.set_xlabel('Angular frequency [rad/s]')

        ax1.set_ylabel('{} [{}]'.format(magnitude_label, self.unit), color='b')

        if xscale == 'log':
            if yscale == 'linear':
                l1, = ax1.semilogx(xvalues, magnitudes, 'b', linewidth=3)
            elif yscale == 'log':
                l1, = ax1.loglog(xvalues, magnitudes, 'b', linewidth=3)
            else:
                raise ValueError('linear or log expected')
            l2, = ax2.semilogx(xvalues, phases, '--r')

        elif xscale == 'linear':
            if yscale == 'linear':
                l1, = ax1.plot(xvalues, magnitudes, 'b', linewidth=3)
            elif yscale == 'log':
                l1, = ax1.semilogy(xvalues, magnitudes, 'b', linewidth=3)
            else:
                raise ValueError('linear or log expected')
            l2, = ax2.plot(xvalues, phases, '--r')

        if phase_unit == 'degrees':
            ax2.set_ylabel('Phase [degrees]', color='r')
        elif phase_unit == 'radians':
            ax2.set_ylabel('Phase [radians]', color='r')

        ax1.tick_params(axis='y', labelcolor='b')
        ax2.tick_params(axis='y', labelcolor='r')
        ax1.grid(True, which='both')

        fig.canvas.mpl_connect('motion_notify_event', mouse_move)
        ax1.set_title(title)

        return fig, ax1, ax2, l1, l2

    def bode_real(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
                  xscale='log', yscale='linear',
                  magnitude_label='Complex real part',
                  title='Complex real part Bode plot', filename=None):
        """Save datas and draw complex real part Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
Note : cannot be log-scaled if data has no positive values.
filename (str) : save datas to csv format file

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> Z = Impedance(c=100e-9)+Impedance(r=1000)+Impedance(l=0.1)
>>> Z.bode();Z.bode_real();Z.bode_imag()
>>> Y = 1/Z
>>> Y.bode();Y.bode_real();Y.bode_imag()
>>> show()
"""
        return self.bode(xmin=xmin, xmax=xmax, xunit=xunit, n=n,
                         xscale=xscale, yscale=yscale,
                         magnitude_label=magnitude_label,
                         title=title, filename=filename,
                         draw_phase=False, mode='real')

    def bode_imag(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
                  xscale='log', yscale='linear',
                  magnitude_label='Complex imaginary part',
                  title='Complex imaginary part Bode plot', filename=None):
        """Save datas and draw complex imaginary part Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
Note : cannot be log-scaled if data has no positive values.
filename (str) : save datas to csv format file

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> Z = Impedance(c=100e-9)+Impedance(r=1000)+Impedance(l=0.1)
>>> Z.bode();Z.bode_real();Z.bode_imag()
>>> Y = 1/Z
>>> Y.bode();Y.bode_real();Y.bode_imag()
>>> show()
"""
        return self.bode(xmin=xmin, xmax=xmax, xunit=xunit, n=n,
                         xscale=xscale, yscale=yscale,
                         magnitude_label=magnitude_label,
                         title=title, filename=filename,
                         draw_phase=False, mode='imag')


class Impedance(Component):
    "The complex Impedance class."

    def __init__(self, **kwargs):
        """Creates Impedance instance

kwargs = ['r' | 'l' | 'c'] | 'fw'
You can define pure resistance, inductance, capacitance complex impedance :

>>> from acelectricity import *
>>> Zr1 = Impedance(r=2200)  # r -> resistance (Ω)
>>> Zl1 = Impedance(l=100e-3) # l -> inductance (H)
>>> Zc1 = Impedance(c=470e-9) # c -> capacitance (F)
>>> Z = Zr1+Zl1+Zc1
>>> Z
Complex impedance (Ω) : 2200+289.691j @ 1 kHz
>>> Zc1.c = 330e-9
>>> Z
Complex impedance (Ω) : 2200+146.031j @ 1.0 kHz

or a user-defined complex impedance function :

>>> def z(w):  # w -> rad/s
        return 1000 + 10j*w  #  complex impedance (Ω)
>>> Z = Impedance(fw=z)  # or Z = Impedance(fw=lambda w: 1000+10j*w)
>>> Z
Complex impedance (Ω) : 1000+62831.9j @ 1 kHz
"""
        Component.__init__(self)
        self.unit = 'Ω'
        self.__r, self.__l, self.__c = None, None, None

        if "r" in kwargs:
            if not isinstance(kwargs["r"], (int, float)):
                raise TypeError("number expected")
            self.__r = kwargs["r"]
            if self.__r <= 0:
                raise ValueError("positive resistance expected")
            self.fw = Wfunction(lambda w: self.__r)
        elif "c" in kwargs:
            if not isinstance(kwargs["c"], (int, float)):
                raise TypeError("number expected")
            self.__c = kwargs["c"]
            if self.__c <= 0:
                raise ValueError("positive capacitance expected")
            self.fw = Wfunction(lambda w: 1/(1j*self.__c*w))
        elif "l" in kwargs:
            if not isinstance(kwargs["l"], (int, float)):
                raise TypeError("number expected")
            self.__l = kwargs["l"]
            if self.__l <= 0:
                raise ValueError("positive inductance expected")
            self.fw = Wfunction(lambda w: 1j*self.__l*w)
        elif "fw" in kwargs:
            if isinstance(kwargs["fw"], Wfunction):
                self.fw = kwargs["fw"]
            elif inspect.isfunction(kwargs["fw"]):
                self.fw = Wfunction(kwargs["fw"])
            else:
                raise TypeError("function expected")
        else:
            raise TypeError("wrong arguments")

        # WFunction instances
        # impedance magnitude (complex modulus, absolute value)
        self.fw_abs = self.fw.abs()
        # impedance phase in degrees (complex argument)
        self.fw_phase_deg = self.fw.phase_deg()
        # impedance phase in radians (complex argument)
        self.fw_phase_rad = self.fw.phase_rad()
        # reactance (ohm) Z = Rs +jX
        self.fw_imag = self.fw.imag()
        # series resistance (ohm) Z = Rs +jX
        self.fw_real = self.fw.real()

    @property
    def r(self):
        # getter
        if self.__r is None:
            raise AttributeError("Impedance object has no attribute 'r'")
        return self.__r

    @r.setter
    def r(self, value):
        if self.__r is None:
            raise AttributeError("Impedance object has no attribute 'r'")
        if not isinstance(value, (int, float)):
            raise TypeError("number expected")
        if value <= 0:
            raise ValueError("positive resistance expected")
        self.__r = value

    @property
    def l(self):
        # getter
        if self.__l is None:
            raise AttributeError("Impedance object has no attribute 'l'")
        return self.__l

    @l.setter
    def l(self, value):
        if self.__l is None:
            raise AttributeError("Impedance object has no attribute 'l'")
        if not isinstance(value, (int, float)):
            raise TypeError("number expected")
        if value <= 0:
            raise ValueError("positive inductance expected")
        self.__l = value

    @property
    def c(self):
        # getter
        if self.__c is None:
            raise AttributeError("Impedance object has no attribute 'c'")
        return self.__c

    @c.setter
    def c(self, value):
        if self.__c is None:
            raise AttributeError("Impedance object has no attribute 'c'")
        if not isinstance(value, (int, float)):
            raise TypeError("number expected")
        if value <= 0:
            raise ValueError("positive capacitance expected")
        self.__c = value

    def __call__(self, value, unit='Hz'):
        """Return the complex impedance (measured in ohms)
value : positive float
unit : prefix + 'Hz' or 'rad/s'

>>> Zl1 = Impedance(l=100e-3)
>>> Zl1(1000)  # Hz default
628.3185307179587j
>>> Zl1(2,'kHz')
1256.6370614359173j
>>> Zl1(10000, 'rad/s')
1000j
"""
        return self.fw(value, unit=unit)

    def properties(self, value, unit='Hz', message=''):
        "Displays the complex impedance properties"

        # f : frequency (Hz) ; w : angular frequency (rad/s)
        (f, w) = getfrequency(value=value, unit=unit)
        rs = self.rs(f, 'Hz')
        x = self.x(f, 'Hz')
        b = Component.get_susceptance(rs, x)

        affichage = '' if message is '' else message + '\n'
        affichage += """Frequency (Hz) : {:g}
Angular frequency (rad/s) : {:g}

Complex impedance (Ω) : {:g}
Impedance magnitude (Ω) : {:g}
Phase (degrees) : {:+g}
Phase (radians) : {:+g}
Equiv. series resistance (Ω) : {:g}

Reactance (Ω) : {:g}
Equiv. series capacitance (F) : {}
Equiv. series inductance (H) : {}

Equiv. parallel conductance (S) : {}
Equiv. parallel resistance (Ω) : {}
Susceptance (S) : {}
Equiv. parallel capacitance (F) : {}
Equiv. parallel inductance (H) : {}
""".format(f, w, self(f, 'Hz'),
           self.abs(f, 'Hz'), self.phase_deg(f, 'Hz'),
           self.phase_rad(f, 'Hz'), rs, x,
           Component.get_series_capacitance(x, w),
           Component.get_series_inductance(x, w),
           Component.get_parallel_conductance(rs, x),
           Component.get_parallel_resistance(rs, x), b,
           Component.get_parallel_capacitance(b, w),
           Component.get_parallel_inductance(b, w))
        print(affichage)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Complex impedance (Ω) : {:g} @ {} {}Hz".format(
            self(value=ElectricalQuantity.DEFAULT_FREQUENCY, unit='Hz'),
            *EngineeringNotation(ElectricalQuantity.DEFAULT_FREQUENCY))

    def __add__(self, impedance):
        """self.__add__(impedance) <=> self + impedance
Impedances in series
>>> Z1 = Z2 + Z3
"""
        return Law().Zserie(self, impedance)

    def __sub__(self, impedance):
        """self.__sub__(impedance) <=> self - impedance
Return Impedance"""
        if isinstance(impedance, Impedance) is False:
                raise TypeError("Impedance expected")
        return Impedance(fw=self.fw - impedance.fw)

    def __pos__(self):
        "self.__pos__() <=> +self"
        return Impedance(fw=self.fw)  # new instance

    def __neg__(self):
        "self.__neg__() <=> -self"
        return Impedance(fw=-self.fw)

    def __floordiv__(self, impedance):
        """self.__floordiv__(impedance) <=> self // impedance
Impedances in parallel
>>> Z1 = Z2//Z3  # or Z1 = 1/(1/Z2 + 1/Z3)
"""
        return Law().Zparallel(self, impedance)

    def __mul__(self, arg):
        """self.__mul__(arg) <=> self * arg
arg is a Current, Admittance, Ratio or a float

arg -> Current object :
Ohm's law
Return a Voltage object

arg -> float :
Multiplication
Return a Impedance object

arg -> Admittance
return Ratio

arg -> Ratio
return Impedance
"""
        if isinstance(arg, Current) is True:
            return Law().Ohm(z=self, i=arg)
        if isinstance(arg, Ratio) is True:
            return Impedance(fw=self.fw * arg.fw)
        if isinstance(arg, Admittance) is True:
            return Ratio(fw=self.fw * arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Impedance(fw=self.fw * arg)

    def __rmul__(self, value):
        """self.__rmul__(value) <=> value * self
value -> complex number
Return a Impedance object
"""
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        return Impedance(fw=self.fw*value)

    def __rtruediv__(self, value):
        """self.__rmul__(value) <=> value / self
value -> complex number
Return a Admittance object
"""
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        return Admittance(fw=value / self.fw)

    def __truediv__(self, arg):
        """self.__truediv__(arg) <=> self / arg

arg is Impedance, Ratio or complex number.

arg -> Impedance
Return a ratio instance

arg -> complex
Return a Impedance instance

arg -> Ratio
Return a Impedance instance
"""
        if isinstance(arg, Ratio) is True:
            return Impedance(fw=self.fw/arg.fw)
        if isinstance(arg, Impedance) is True:
            return Ratio(fw=self.fw/arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Impedance(fw=self.fw/arg)

    def abs(self, value, unit='Hz'):
        """Z = Rs +jX
return impedance magnitude |Z| (ohm)"""
        return self.fw_abs(value, unit=unit)

    def phase_deg(self, value, unit='Hz'):
        """Z = Rs +jX
return impedance phase in degrees (complex impedance argument)"""
        return self.fw_phase_deg(value, unit=unit)

    def phase_rad(self, value, unit='Hz'):
        """Z = Rs +jX
return impedance phase in radians (complex impedance argument)"""
        return self.fw_phase_rad(value, unit=unit)

    def rs(self, value, unit='Hz'):
        """Z = Rs +jX
return series resistance Rs (ohm)"""
        return self.fw_real(value, unit=unit)

    def x(self, value, unit='Hz'):
        """Z = Rs +jX
return reactance X (ohm)"""
        return self.fw_imag(value, unit=unit)

    def real(self, value, unit='Hz'):
        "return complex impedance real part"
        return self.fw_real(value, unit=unit)

    def imag(self, value, unit='Hz'):
        "return complex impedance real part"
        return self.fw_imag(value, unit=unit)


class Admittance(Component):
    "The complex Admittance class"

    def __init__(self, **kwargs):
        """Creates complex Admittance instance

kwargs = ['r' | 'l' | 'c'] | 'fw'
You can define pure resistance, inductance or capacitance complex admittance :

>>> from acelectricity import *
>>> Yr1 = Admittance(r=2200)  # r -> resistance (Ω)
>>> Yl1 = Admittance(l=100e-3) # l -> inductance (H)
>>> Yc1 = Admittance(c=470e-9) # c -> capacitance (F)
>>> Yt = Yr1+Yl1+Yc1
>>> Yt
Complex admittance (S) : 0.000454545+0.00136155j @ 1 kHz
>>> Yl1.l = 200e-3
>>> Yt
Complex admittance (S) : 0.000454545+0.00215732j @ 1.0 kHz

or a user-defined complex admittance function :

>>> def y(w):  # w -> rad/s
        return 0.001+0.002j*w  # complex admittance (siemens)
>>> Y = Admittance(fw=y)  # or Y = Admittance(fw=lambda w: 0.001+0.002j*w)
>>> Y
Complex admittance (S) : 0.001+12.5664j @ 1 kHz
"""
        Component.__init__(self)
        self.unit = "S"    # siemens
        self.__r, self.__l, self.__c = None, None, None

        if "r" in kwargs:
            if not isinstance(kwargs["r"], (int, float)):
                raise TypeError("number expected")
            self.__r = kwargs["r"]
            if self.__r <= 0:
                raise ValueError("positive resistance expected")
            self.fw = Wfunction(lambda w: 1/self.__r)
        elif "c" in kwargs:
            if not isinstance(kwargs["c"], (int, float)):
                raise TypeError("number expected")
            self.__c = kwargs["c"]
            if self.__c <= 0:
                raise ValueError("positive capacitance expected")
            self.fw = Wfunction(lambda w: 1j*self.__c*w)
        elif "l" in kwargs:
            if not isinstance(kwargs["l"], (int, float)):
                raise TypeError("number expected")
            self.__l = kwargs["l"]
            if self.__l <= 0:
                raise ValueError("positive inductance expected")
            self.fw = Wfunction(lambda w: 1/(1j*self.__l*w))
        elif "fw" in kwargs:
            if isinstance(kwargs["fw"], Wfunction):
                self.fw = kwargs["fw"]
            elif inspect.isfunction(kwargs["fw"]):
                self.fw = Wfunction(kwargs["fw"])
            else:
                raise TypeError("function expected")
        else:
            raise TypeError("wrong arguments")

        # WFunction instances
        # admittance magnitude (complex modulus, absolute value)
        self.fw_abs = self.fw.abs()
        # admittance phase in degrees (complex argument)
        self.fw_phase_deg = self.fw.phase_deg()
        # admittance phase in radians (complex argument)
        self.fw_phase_rad = self.fw.phase_rad()
        # susceptance (B) : Y = G +jB
        self.fw_imag = self.fw.imag()
        # parallel conductance (G) : Y = G +jB
        self.fw_real = self.fw.real()

    @property
    def r(self):
        # getter
        if self.__r is None:
            raise AttributeError("Admittance object has no attribute 'r'")
        return self.__r

    @r.setter
    def r(self, value):
        if self.__r is None:
            raise AttributeError("Admittance object has no attribute 'r'")
        if not isinstance(value, (int, float)):
            raise TypeError("number expected")
        if value <= 0:
            raise ValueError("positive resistance expected")
        self.__r = value

    @property
    def l(self):
        # getter
        if self.__l is None:
            raise AttributeError("Admittance object has no attribute 'l'")
        return self.__l

    @l.setter
    def l(self, value):
        if self.__l is None:
            raise AttributeError("Admittance object has no attribute 'l'")
        if not isinstance(value, (int, float)):
            raise TypeError("number expected")
        if value <= 0:
            raise ValueError("positive inductance expected")
        self.__l = value

    @property
    def c(self):
        # getter
        if self.__c is None:
            raise AttributeError("Admittance object has no attribute 'c'")
        return self.__c

    @c.setter
    def c(self, value):
        if self.__c is None:
            raise AttributeError("Admittance object has no attribute 'c'")
        if not isinstance(value, (int, float)):
            raise TypeError("number expected")
        if value <= 0:
            raise ValueError("positive capacitance expected")
        self.__c = value

    def __call__(self, value, unit='Hz'):
        """Return the complex admittance (measured in siemens)
value : positive float
unit : prefix + 'Hz' or 'rad/s'

>>> Yl1 = Admittance(l=100e-3)
>>> Yl1(1000)  # Hz default
-0.0015915494309189533j
>>> Yl1(2,'kHz')
-0.0007957747154594767j
>>> Yl1(10000, 'rad/s')
-0.001j
"""
        return self.fw(value, unit=unit)

    def properties(self, value, unit='Hz', message=''):
        "Displays the complex admittance properties"

        # f : frequency (Hz) ; w : angular frequency (rad/s)
        (f, w) = getfrequency(value, unit=unit)
        g = self.g(f, 'Hz')
        try:
            rp = 1/g
        except ZeroDivisionError:
            rp = None
        b = self.b(f, 'Hz')
        x = Component.get_reactance(g, b)

        affichage = '' if message is '' else message + '\n'
        affichage += """Frequency (Hz) : {:g}
Angular frequency (rad/s) : {:g}

Complex admittance (S) : {:g}
Admittance magnitude (S) : {:g}
Phase (degrees) : {:+g}
Phase (radians) : {:+g}
Equiv. parallel conductance (S) : {:g}
Equiv. parallel resistance (Ω) : {}

Susceptance (S) : {:g}
Equiv. parallel capacitance (F) : {}
Equiv. parallel inductance (H) : {}

Equiv. series resistance (Ω) : {}
Reactance (Ω) : {}
Equiv. series capacitance (F) : {}
Equiv. series inductance (H) : {}
""".format(f, w, self(f, 'Hz'),
           self.abs(f, 'Hz'), self.phase_deg(f, 'Hz'),
           self.phase_rad(f, 'Hz'), g, rp, b,
           Component.get_parallel_capacitance(b, w),
           Component.get_parallel_inductance(b, w),
           Component.get_series_resistance(g, b), x,
           Component.get_series_capacitance(x, w),
           Component.get_series_inductance(x, w))
        print(affichage)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Complex admittance (S) : {:g} @ {} {}Hz".format(
            self(value=ElectricalQuantity.DEFAULT_FREQUENCY, unit='Hz'),
            *EngineeringNotation(ElectricalQuantity.DEFAULT_FREQUENCY))

    def __add__(self, admittance):
        "self.__add__(admittance) <=> self + admittance"
        if isinstance(admittance, Admittance) is False:
                raise TypeError("Admittance expected")
        return Admittance(fw=self.fw + admittance.fw)

    def __sub__(self, admittance):
        """self.__sub__(admittance) <=> self - admittance
Return Admittance"""
        if isinstance(admittance, Admittance) is False:
                raise TypeError("Admittance expected")
        return Admittance(fw=self.fw - admittance.fw)

    def __pos__(self):
        "self.__pos__() <=> +self"
        return Admittance(fw=self.fw)  # new object

    def __neg__(self):
        "self.__neg__() <=> -self"
        return Admittance(fw=-self.fw)

    def __mul__(self, arg):
        """self.__mul__(arg) <=> self * arg

arg is Voltage, Impedance, Ratio or complex number

arg -> Voltage :
Ohm's law
Return Current

arg -> complex :
Multiplication
Return Admittance

arg -> Impedance
return Ratio

arg -> Ratio
return Admittance
"""
        if isinstance(arg, Voltage) is True:
            return Current(fw=self.fw * arg.fw)
        if isinstance(arg, Impedance) is True:
            return Ratio(fw=self.fw * arg.fw)
        if isinstance(arg, Ratio) is True:
            return Admittance(fw=self.fw * arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Admittance(fw=self.fw * arg)

    def __rmul__(self, value):
        """self.__rmul__(value) <=> value * self
value -> complex number
Return Admittance
"""
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        return Admittance(fw=value * self.fw)

    def __rtruediv__(self, value):
        """self.__rtruediv__(arg) <=> value / self
value -> complex number
Return Impedance
"""
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        return Impedance(fw=value/self.fw)

    def __truediv__(self, arg):
        """self.__truediv__(arg) <=> self / arg

arg is Admittance, Ratio or complex number.
>>> x = Y1/Y2  # ratio
>>> Y2 = Y1/x
>>> Y1 = Y2/10
"""
        if isinstance(arg, Admittance) is True:
            return Ratio(fw=self.fw/arg.fw)
        if isinstance(arg, Ratio) is True:
            return Admittance(fw=self.fw/arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Admittance(fw=self.fw/arg)

    def __floordiv__(self, admittance):
        """self.__floordiv__(admittance) <=> self // admittance
admittances in parallel
Return Admittance
>>> Y = Y1//Y2  # or Y = Y1 + Y2
"""
        return self.__add__(admittance)

    def abs(self, value, unit='Hz'):
        """Y = G +jB
return admittance magnitude |Y| in siemens"""
        return self.fw_abs(value, unit=unit)

    def phase_deg(self, value, unit='Hz'):
        """Y = G +jB
return admittance phase in degrees (complex admittance argument)"""
        return self.fw_phase_deg(value, unit=unit)

    def phase_rad(self, value, unit='Hz'):
        """Y = G +jB
return admittance phase in radians (complex admittance argument)"""
        return self.fw_phase_rad(value, unit=unit)

    def g(self, value, unit='Hz'):
        """Y = G +jB
return parallel conductance G (siemens)"""
        return self.fw_real(value, unit=unit)

    def b(self, value, unit='Hz'):
        """Y = G +jB
return susceptance B (siemens)"""
        return self.fw_imag(value, unit=unit)

    def real(self, value, unit='Hz'):
        "return complex admittance real part"
        return self.fw_real(value, unit=unit)

    def imag(self, value, unit='Hz'):
        "return complex admittance real part"
        return self.fw_imag(value, unit=unit)


class Law:
    """The Law class

- Kirchhoff’s current law (KCL)
- Kirchhoff’s voltage law (KVL)
- Ohm's law
- Admittances and impedances in series and parallel
- Voltage divider and current divider
- Millman's theorem
- Electrical complex power : S = V*conj(I)
- Joule's first law : S = |I|²Z = |V|²/conj(Z)

>>> from acelectricity import *
>>> law = Law()
>>> v1 = Voltage(5)
>>> z1 = Impedance(r=1000)
>>> i1 = law.Ohm(v=v1, z=z1)
"""

    def KVL(self, signs, *voltages):
        """Kirchhoff’s voltage law

signs -> str
*voltages -> Voltage
return Voltage

# v = v1 + v2 - v3
>>> law = Law()
>>> v = law.KVL('++-', v1, v2, v3)
"""
        if len(voltages) == 0:
            raise ValueError("at least one Voltage")

        for voltage in voltages:
            if isinstance(voltage, Voltage) is False:
                raise TypeError("Voltage expected")

        if not isinstance(signs, str):
            raise TypeError("string expected")

        if len(voltages) != len(signs):
            raise ValueError("signs length is wrong")
        else:
            for sign in signs:
                if sign not in "+-":
                    raise ValueError("signs string wrong format")

        fw = 0
        for index, voltage in enumerate(voltages):
            if signs[index] == "+":
                fw += voltage.fw
            elif signs[index] == "-":
                fw -= voltage.fw
        return Voltage(fw=fw)

    def KCL(self, signs, *currents):
        """Kirchhoff’s current law
signs -> str
*currents -> Current
return Current

# i4 = -i1 + i2 - i3
>>> law = Law()
>>> i4 = law.KCL('-+-', i1, i2, i3)
"""

        if len(currents) == 0:
            raise ValueError("Current expected")

        for current in currents:
            if isinstance(current, Current) is False:
                raise TypeError("Current expected")

        if not isinstance(signs, str):
            raise TypeError("string expected")

        if len(currents) != len(signs):
            raise ValueError("signs length is wrong")
        else:
            for sign in signs:
                if sign not in "+-":
                    raise ValueError("signs string wrong format")

        fw = 0
        for index, current in enumerate(currents):
            if signs[index] == "+":
                fw += current.fw
            elif signs[index] == "-":
                fw -= current.fw
        return Current(fw=fw)

    def Ohm(self, **kwargs):
        """Ohm's law

As the case may be : v = z*i, i = v/z or z = v/i

**kwargs -> two of v, z, i
v -> Voltage
i -> Current
z -> Impedance

>>> v1 = Voltage(5, phase=30)
>>> i1 = Current(20e-6)
>>> law = Law()
>>> z1 = law.Ohm(v=v1, i=i1)
>>> z1
Complex impedance (Ω) : 216506+125000j @ 1.0 kHz
>>> i1.phase = 30
>>> z1
Complex impedance (Ω) : 250000+0j @ 1.0 kHz
"""
        grandeurs_attendus = ['v', 'z', 'i']

        if len(kwargs) != 2:
            raise ValueError("two arguments are expected")

        else:
            # liste des paramètres
            cles = list(kwargs)
            if (cles[0] not in grandeurs_attendus or
                    cles[1] not in grandeurs_attendus):
                raise ValueError("expected arguments are z, v or i")

        # v = z*i
        if 'v' not in cles:
            if isinstance(kwargs['i'], Current) is False:
                raise TypeError("Current expected")
            if isinstance(kwargs['z'], Impedance) is False:
                raise TypeError("Impedance expected")
            return Voltage(fw=kwargs['z'].fw * kwargs['i'].fw)

        # i = v/z
        if 'i' not in cles:
            if isinstance(kwargs['v'], Voltage) is False:
                raise TypeError("Voltage expected")
            if isinstance(kwargs['z'], Impedance) is False:
                raise TypeError("Impedance expected")
            return Current(fw=kwargs['v'].fw / kwargs['z'].fw)

        # z =v/i
        if 'z' not in cles:
            if isinstance(kwargs['v'], Voltage) is False:
                raise TypeError("Voltage expected")
            if isinstance(kwargs['i'], Current) is False:
                raise TypeError("Current expected")
            return Impedance(fw=kwargs['v'].fw / kwargs['i'].fw)

    def Zserie(self, *impedances):
        """Impedances in series

*impedances -> Impedance
return Impedance

# zeq = z1+z2+z3
>>> law = Law()
>>> Zeq = law.Zserie(z1, z2, z3)
"""
        if len(impedances) == 0:
            raise TypeError("at least one argument")

        fw = 0
        for impedance in impedances:
            if isinstance(impedance, Impedance) is False:
                raise TypeError("Impedance expected")
            fw += impedance.fw
        return Impedance(fw=fw)

    def Zparallel(self, *impedances):
        """Impedances in parallel

*impedances -> Impedance
return Impedance

# zeq = 1/(1/z1 + 1/z2 + 1/z3)
>>> law = Law()
>>> zeq = law.Zparallel(z1, z2, z3)
"""
        if len(impedances) == 0:
            raise TypeError("at least one argument")
        fw = 0
        for impedance in impedances:
            if isinstance(impedance, Impedance) is False:
                raise TypeError("Impedance expected")
            fw += 1/impedance.fw
        return Impedance(fw=1/fw)

    def VoltageDivider(self, vtotal, z, z2):
        """Voltage divider

        vtotal
--------------------->

----[z]-----[z2]-----

   ----->
     v

vtotal -> Voltage
z, z2  -> Impedance
return v Voltage

# v1 = vsource*(z1/(z1+z2))
>>> law = Law()
>>> v1 = law.VoltageDivider(vtotal=vsource, z=z1, z2=z2)
"""

        if isinstance(z, Impedance) is False:
                raise TypeError("Impedance expected")
        if isinstance(z2, Impedance) is False:
                raise TypeError("Impedance expected")
        if isinstance(vtotal, Voltage) is False:
                raise TypeError("Voltage expected")
        return Voltage(fw=vtotal.fw*z.fw / (z.fw + z2.fw))

    def CurrentDivider(self, itotal, z, z2):
        """Current divider

                i
   +----[z]----<--+     itotal
---|              |---<----
   +----[z2]---<--+

itotal -> Current
z, z2  -> Impedance
return i Current

# i1 = isource*(z2/(z1+z2))
>>> law = Law()
>>> i1 = law.CurrentDivider(itotal=isource, z=z1, z2=z2)
"""

        if isinstance(z, Impedance) is False:
            raise TypeError("Impedance expected")
        if isinstance(z2, Impedance) is False:
            raise TypeError("Impedance expected")
        if isinstance(itotal, Current) is False:
            raise TypeError("Current expected")
        return Current(fw=itotal.fw*z2.fw/(z.fw + z2.fw))

    def Millman(self, v_z, i=[]):
        """Millman's theorem
v_z -> list of tuples (voltage, impedance)
i -> list of currents
return Voltage

>>> law = Law()
>>> v = law.Millman([(v1, z1), (v2, z2), (v3, z3)], i=[i4, i5])
"""
        if isinstance(v_z, list) is False:
                raise TypeError("list expected for v_r argument")

        if len(v_z) == 0:
            raise TypeError("v_r must contain at least one item")

        somme_v_sur_R = 0
        somme_1_sur_R = 0
        for elt in v_z:
            if isinstance(elt, tuple) is False:
                raise TypeError("tuple expected")
            if len(elt) != 2:
                raise TypeError("tuple must contain two items")
            if isinstance(elt[0], Voltage) is False:
                raise TypeError("Voltage expected")
            if isinstance(elt[1], Impedance) is False:
                raise TypeError("Impedance expected")
            somme_v_sur_R += elt[0].fw / elt[1].fw
            somme_1_sur_R += 1/elt[1].fw

        if isinstance(i, list) is False:
            raise TypeError("list expected")

        itotal = 0
        for current in i:
            if isinstance(current, Current) is False:
                raise TypeError("Current expected")
            itotal += current.fw
        return Voltage(fw=(somme_v_sur_R + itotal)/somme_1_sur_R)

    def Power(self, v, i):
        """Complex power S = V*conj(I)
v -> Voltage
i -> Current
return complex Power

Note : don't confuse Law.Power() and Power()

>>> law = Law()
>>> p1 = law.Power(v=v1, i=i1)
"""
        if isinstance(v, Voltage) is False:
                    raise TypeError("Voltage expected")
        if isinstance(i, Current) is False:
                    raise TypeError("Current expected")
        return Power(fw=v.fw * i.fw.conjugate())

    def Joule(self, z, **kwarg):
        """Joule's first law

s = z*|i|² or s = |v|²/conj(z)

**kwarg -> v or i
v -> Voltage
i -> Current
z -> Impedance
return complex Power

>>> law = Law()
>>> s1 = law.Joule(z=z1, i=i1)
"""
        grandeurs_attendus = ['v', 'i']
        if len(kwarg) != 1:
            raise TypeError("one argument expected")
        else:
            cle = list(kwarg)
            if cle[0] not in grandeurs_attendus:
                raise TypeError("argument v or i expected")
        if isinstance(z, Impedance) is False:
            raise TypeError("Impedance expected")

        # s = z*|i|²
        if 'i' in cle:
            if isinstance(kwarg['i'], Current) is False:
                raise TypeError("Current expected")
            fw = kwarg['i'].fw.abs()*kwarg['i'].fw.abs()*z.fw
            return Power(fw=fw)

        # s = |v|²/conj(z)
        elif 'v' in cle:
            if isinstance(kwarg['v'], Voltage) is False:
                raise TypeError("Voltage expected")
            fw = kwarg['v'].fw.abs()*kwarg['v'].fw.abs()/z.fw.conjugate()
            return Power(fw=fw)


class ElectricalQuantity:
    """ElectricalQuantity serves as a base class for Voltage, Current,
Power and Ratio classes"""

    # class attribut
    DEFAULT_FREQUENCY = 1000  # Hz

    def __init__(self):
        pass

    def bode(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
             xscale='log', yscale='linear',
             magnitude_label='Magnitude', magnitude_unit='db',
             phase_unit='degrees', title='Bode plot',
             filename=None, draw_phase=True, **kwarg):
        """Save datas and draw Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
magnitude_unit = ['db' | 'default']
phase_unit= ["degrees" | 'radians']
filename (str) : save datas to csv format file
draw_phase (bool)

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude/dB), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> Vin = Voltage(5)
>>> Zr = Impedance(r=1000)
>>> Zc = Impedance(c=100e-9)
>>> Vout = Vin*(Zc/(Zr+Zc))  # low-pass RC
>>> H = Vout/Vin  #  transfer function
>>> H.bode(filename='h.csv')
>>> show()
"""
        # attribut used here : self.unit, self.db_unit
        unite = self.unit

        if n < 10:
            raise ValueError('10 points minimum')

        # f = frequency (Hz) ; w = angular frequency (rad/s)
        if xmin > xmax:
            xmin, xmax = xmax, xmin
        if xmin < 0 or xmax < 0:
            raise ValueError("xmin and xmax must be positive")
        if xscale == 'log' and xmin == 0:
            xmin = xmax*1e-4  # 4 decades
            print("Warning : xmin (0) set to {}".format(xmin))
        (fmin, wmin) = getfrequency(value=xmin, unit=xunit)
        (fmax, wmax) = getfrequency(value=xmax, unit=xunit)

        # xvalues
        unit = 'Hz' if 'Hz' in xunit else 'rad/s'
        if xscale == 'log':
            if unit == 'Hz':
                xvalues = list(np.geomspace(fmin, fmax, n))
            elif unit == 'rad/s':
                xvalues = list(np.geomspace(wmin, wmax, n))
        elif xscale == 'linear':
            if unit == 'Hz':
                xvalues = list(np.linspace(fmin, fmax, n))
            elif unit == 'rad/s':
                xvalues = list(np.linspace(wmin, wmax, n))
        else:
            raise ValueError('log or linear expected')

        # magnitudes
        if magnitude_unit == 'db':
            if isinstance(self, Ratio):
                magnitudes = [self.db(x, unit=unit) for x in xvalues]
            elif isinstance(self, Power):
                magnitudes = [self.dbw(x, unit=unit) for x in xvalues]
            elif isinstance(self, Voltage):
                magnitudes = [self.dbv(x, unit=unit) for x in xvalues]
            elif isinstance(self, Current):
                magnitudes = [self.dba(x, unit=unit) for x in xvalues]
            else:
                raise TypeError

        elif magnitude_unit == 'default':
            if isinstance(self, (Voltage, Current, Ratio)):
                if 'mode' in kwarg:
                    if kwarg['mode'] == 'real':
                        # bode_real()
                        magnitudes = [self.real(x, unit=unit)
                                      for x in xvalues]
                    elif kwarg['mode'] == 'imag':
                        # bode_imag()
                        magnitudes = [self.imag(x, unit=unit)
                                      for x in xvalues]
                    else:
                        raise ValueError('mode argument: real or imag expected')
                else:
                    # bode()
                    if isinstance(self, Ratio):
                        magnitudes = [self.abs(x, unit=unit) for x in xvalues]
                    elif isinstance(self, (Voltage, Current)):
                        magnitudes = [self.rms(x, unit=unit) for x in xvalues]

            elif isinstance(self, Power):
                if 'mode' in kwarg:
                    if kwarg['mode'] == 'va':
                        # bode_va()
                        unite = 'VA'
                        magnitudes = [self.va(x, unit=unit) for x in xvalues]
                    elif kwarg['mode'] == 'var':
                        # bode_var()
                        unite = 'var'
                        magnitudes = [self.var(x, unit=unit)
                                      for x in xvalues]
                    elif kwarg['mode'] == 'pf':
                        # bode_pf()
                        unite = ''
                        magnitudes = [self.pf(x, unit=unit) for x in xvalues]
                    else:
                        raise ValueError('mode argument: va,var or pf expected')
                else:
                    # bode() active power
                    magnitudes = [self.w(x, unit=unit) for x in xvalues]
            else:
                raise TypeError
        else:
            raise ValueError('db or default expected')

        # phases
        if phase_unit == 'degrees':
            phases = [self.phase_deg(x, unit=unit) for x in xvalues]
        elif phase_unit == 'radians':
            phases = [self.phase_rad(x, unit=unit) for x in xvalues]
        else:
            raise ValueError('degrees or radians expected')

        # save datas to csv format file
        if filename is not None:
            with open(filename, 'w') as f:
                writer = csv.writer(f)
                if draw_phase:
                    for datas in zip(xvalues, magnitudes, phases):
                        writer.writerow(data for data in datas)
                else:
                    for datas in zip(xvalues, magnitudes):
                        writer.writerow(data for data in datas)
            print('Save datas to {} file [DONE]'.format(filename))

        # matplotlib
        if not _matplotlib_available:
            print("You should install matplotlib to draw Bode plot")
            return

        fig, ax1 = plt.subplots()
        fig.tight_layout()
        fig.subplots_adjust(left=0.15, bottom=0.1, right=0.85,
                            top=0.9, wspace=0.2, hspace=0.2)
        ax2 = ax1.twinx()
        ax2.set_visible(draw_phase)

        print("Plot figure {} {}".format(plt.get_fignums()[-1], title))
        if draw_phase:
            for i in zip(xvalues[:5], magnitudes[:5], phases[:5]):
                print("{:g} {:g} {:g}".format(*i))
            print("[...]")
            for i in zip(xvalues[-5:], magnitudes[-5:], phases[-5:]):
                print("{:g} {:g} {:g}".format(*i))
        else:
            for i in zip(xvalues[:5], magnitudes[:5]):
                print("{:g} {:g}".format(*i))
            print("[...]")
            for i in zip(xvalues[-5:], magnitudes[-5:]):
                print("{:g} {:g}".format(*i))

        def mouse_move(event):
            # draw cursors
            if not event.inaxes:
                txt.set_text('')
                lx.set_visible(False)
                ly.set_visible(False)
                lp.set_visible(False)
                ax1.figure.canvas.draw()
                ax2.figure.canvas.draw()
                return
            x, y = event.xdata, event.ydata
            indx = min(np.searchsorted(xvalues, x), len(xvalues) - 1)

            x = l1.get_xdata()[indx]
            y = l1.get_ydata()[indx]
            p = l2.get_ydata()[indx]

            # update the line positions
            lx.set_visible(True)
            ly.set_visible(True)
            lp.set_visible(True)

            lx.set_xdata(x)
            ly.set_ydata(y)
            lp.set_ydata(p)

            if draw_phase:
                if magnitude_unit == 'db':
                    txt.set_text('{:f} {}{}, {:g} {}, {:g} {}'.
                                 format(*EngineeringNotation(x), unit, y,
                                        self.db_unit, p, phase_unit))
                else:
                    txt.set_text('{:f} {}{}, {:f} {}{}, {:g} {}'.
                                 format(*EngineeringNotation(x), unit,
                                        *EngineeringNotation(y), unite, p,
                                        phase_unit))
            else:
                if magnitude_unit == 'db':
                    txt.set_text('{:f} {}{}, {:g} {}'.
                                 format(*EngineeringNotation(x), unit, y,
                                        self.db_unit))
                else:
                    txt.set_text('{:f} {}{}, {:f} {}{}'.
                                 format(*EngineeringNotation(x), unit,
                                        *EngineeringNotation(y), unite))

            ax1.figure.canvas.draw()
            ax2.figure.canvas.draw()

        # cursors
        # x vertical line
        lx = ax1.axvline(color='k', linewidth=1, linestyle='--',
                         visible=False)
        # magnitude horizontal line
        ly = ax1.axhline(color='b', linewidth=1, linestyle='--',
                         visible=False)
        # phase horizontal line
        lp = ax2.axhline(color='r', linewidth=1, linestyle='--',
                         visible=False)
        # text location in axes coords
        txt = ax1.text(0.1, 0.95, '', transform=ax1.transAxes)

        if unit == 'Hz':
            ax1.set_xlabel('Frequency [Hz]')
        elif unit == 'rad/s':
            ax1.set_xlabel('Angular frequency [rad/s]')

        if magnitude_unit == 'db':
            ax1.set_ylabel('{} [{}]'.format(
                magnitude_label, self.db_unit), color='b')
        elif magnitude_unit == 'default':
            ax1.set_ylabel('{} [{}]'.format(
                magnitude_label, unite), color='b')

        if xscale == 'log':
            if yscale == 'linear':
                l1, = ax1.semilogx(xvalues, magnitudes, 'b', linewidth=3)
            elif yscale == 'log':
                if magnitude_unit == 'default':
                    l1, = ax1.loglog(xvalues, magnitudes, 'b', linewidth=3)
                else:
                    raise ValueError('yscale must be linear if \
magnitude_unit is dB')
            else:
                raise ValueError('linear or log expected')
            l2, = ax2.semilogx(xvalues, phases, '--r')

        elif xscale == 'linear':
            if yscale == 'linear':
                l1, = ax1.plot(xvalues, magnitudes, 'b', linewidth=3)
            elif yscale == 'log':
                if magnitude_unit == 'default':
                    l1, = ax1.semilogy(xvalues, magnitudes, 'b', linewidth=3)
                else:
                    raise ValueError('yscale must be linear if \
magnitude_unit is dB')
            else:
                raise ValueError('linear or log expected')
            l2, = ax2.plot(xvalues, phases, '--r')

        if phase_unit == 'degrees':
            ax2.set_ylabel('Phase [degrees]', color='r')
        elif phase_unit == 'radians':
            ax2.set_ylabel('Phase [radians]', color='r')

        ax1.tick_params(axis='y', labelcolor='b')
        ax2.tick_params(axis='y', labelcolor='r')
        ax1.grid(True, which='both')

        fig.canvas.mpl_connect('motion_notify_event', mouse_move)
        ax1.set_title(title)

        return fig, ax1, ax2, l1, l2


class Ratio(ElectricalQuantity):
    "The complex Ratio and transfer function class"
    def __init__(self, ratio=1+0j, **kwargs):
        """
Constant ratio (no unit)
------------------------
>>> x = Ratio(100+1000j)


Electrical quantities ratio (no unit)
-------------------------------------

>>> x = v1/v2   # complex voltage ratio
>>> x = i1/i2   # complex current ratio
>>> x = z1/z2   # complex impedance ratio
>>> x = y1/y2   # complex admittance ratio
>>> x = s1/s2   # complex power ratio

User-defined transfer function
------------------------------
Example 1 : second order band-pass filter

>>> # static gain, damping value, normal angular frequency
>>> a, z, wn = 10, 0.1, 1000*2*math.pi
>>> H = Ratio(fw=lambda w: a*(2*z*1j*w/wn)/(1+2*z*1j*w/wn-(w/wn)**2))
>>> # or : H = Ratio.transfer_function(numerator=[0, a*(2*z*1j/wn)],
    denominator=[1, 2*z*1j/wn, -1/wn**2])
>>> H.bode()
>>> show()

Example 2 : cascaded series, parallel filters

>>> # first order low-pass filter
>>> wn = 10000
>>> Hlp = Ratio(fw=lambda w: 1/(1+1j*w/wn))
>>> # first order high-pass filter
>>> Hhp = Ratio(fw=lambda w: 1/(1+1j*wn/w))
>>> Hs = Hlp*Hhp  # cascaded series filters
>>> Hs.bode()
>>> Hp = Hlp+Hhp  # parallel filters
>>> Hp.bode()
>>> show()

Example 3 : linear control system

          +      +------+
     -->---(X)---| G(w) |----+--->--
          - |    +------+    |
            |                |
            |    +------+    |
            +----| H(w) |-<--+
                 +------+

>>> # feedforward transfer function
>>> # first order low-pass filter
>>> wn = 10000
>>> G = Ratio.transfer_function([1], [1, 1j/wn])
>>> # feedback transfer function
>>> H = Ratio.transfer_function([10])  # constant
>>> # open-loop transfer function
>>> Hopenloop = G*H
>>> Hopenloop.bode()
>>> # closed-loop transfer function
>>> Hcloseloop = G/(1+G*H)
>>> Hcloseloop.bode()
>>> show()

Example 4 : digital filter frequency response

y(n) = 0.1x(n) +1.6y(n-1) -0.7y(n-2)

>>> fs = 100000  # sampling rate (Hz)
>>> H = Ratio.digital_filter(fs=fs, b=[0.1], a=[1, -1.6, 0.7])
>>> H.bode(xmin=fs*0.001, xmax=fs/2, xscale='linear')
>>> show()
"""
        self.unit = ''  # no unit
        self.db_unit = 'dB'
        ElectricalQuantity.__init__(self)
        self.__ratio = None

        if "fw" in kwargs:
            if isinstance(kwargs["fw"], Wfunction):
                self.fw = kwargs["fw"]
            elif inspect.isfunction(kwargs["fw"]):
                self.fw = Wfunction(kwargs["fw"])
            else:
                raise TypeError("function expected")
        else:
            if not isinstance(ratio, (int, float, complex)):
                raise TypeError("number expected")
            self.__ratio = ratio
            self.fw = Wfunction(lambda w: self.__ratio)

        # WFunction instances
        # magnitude (complex modulus, absolute value)
        self.fw_abs = self.fw.abs()
        # phase in degrees (complex argument)
        self.fw_phase_deg = self.fw.phase_deg()
        # phase in radians (complex argument)
        self.fw_phase_rad = self.fw.phase_rad()
        # dB
        self.fw_db = self.fw.db()
        # dBw
        self.fw_dbw = self.fw.dbw()
        # complex ratio imaginary part
        self.fw_imag = self.fw.imag()
        # complex ratio real part
        self.fw_real = self.fw.real()

    @property
    def ratio(self):
        # getter
        if self.__ratio is None:
            raise AttributeError("Ratio object has no attribute 'ratio'")
        return self.__ratio

    @ratio.setter
    def ratio(self, value):
        if self.__ratio is None:
            raise AttributeError("Ratio object has no attribute 'ratio'")
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        self.__ratio = value

    def __call__(self, value, unit='Hz'):
        """Return the complex Ratio or transfer function
value : positive float
unit : prefix + 'Hz' or 'rad/s'
"""
        return self.fw(value, unit=unit)

    def properties(self, value, unit='Hz', message=''):
        "Displays the Ratio or transfer function properties"
        # f : frequency (Hz) ; w : angular frequency (rad/s)
        (f, w) = getfrequency(value, unit=unit)
        affichage = '' if message is '' else message + '\n'
        affichage += """Frequency (Hz) : {:g}
Angular frequency (rad/s) : {:g}

Complex value : {:g}
Magnitude : {:g}
Magnitude (dB) : {}
Phase (degrees) : {:+g}
Phase (radians) : {:+g}
""".format(f, w, self(f, 'Hz'),
           self.abs(f, 'Hz'), self.db(f, 'Hz'),
           self.phase_deg(f, 'Hz'), self.phase_rad(f, 'Hz'))
        print(affichage)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Ratio : {:g} @ {} {}Hz".format(
            self(value=ElectricalQuantity.DEFAULT_FREQUENCY, unit='Hz'),
            *EngineeringNotation(ElectricalQuantity.DEFAULT_FREQUENCY))

    def __add__(self, arg):
        if isinstance(arg, Ratio) is True:
            return Ratio(fw=self.fw + arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Ratio(fw=self.fw + arg)

    def __radd__(self, value):
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        return Ratio(fw=value + self.fw)

    def __mul__(self, arg):
        if isinstance(arg, Impedance) is True:
            return Impedance(fw=self.fw * arg.fw)
        if isinstance(arg, Admittance) is True:
            return Admittance(fw=self.fw * arg.fw)
        if isinstance(arg, Voltage) is True:
            return Voltage(fw=self.fw * arg.fw)
        if isinstance(arg, Current) is True:
            return Current(fw=self.fw * arg.fw)
        if isinstance(arg, Power) is True:
            return Power(fw=self.fw * arg.fw)
        if isinstance(arg, Ratio) is True:
            return Ratio(fw=self.fw * arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Ratio(fw=self.fw * arg)

    def __rmul__(self, value):
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        return Ratio(fw=value*self.fw)

    def __truediv__(self, arg):
        if isinstance(arg, Impedance) is True:
            return Admittance(fw=self.fw / arg.fw)
        if isinstance(arg, Admittance) is True:
            return Impedance(fw=self.fw / arg.fw)
        if isinstance(arg, Ratio) is True:
            return Ratio(fw=self.fw / arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Ratio(fw=self.fw / arg)

    def __rtruediv__(self, value):
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        return Ratio(fw=value/self.fw)

    def __sub__(self, arg):
        if isinstance(arg, Ratio) is True:
            return Ratio(fw=self.fw - arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Ratio(fw=self.fw - arg)

    def __rsub__(self, value):
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        return Ratio(fw=value - self.fw)

    def __pos__(self):
        return Ratio(fw=self.fw)

    def __neg__(self):
        return Ratio(fw=-self.fw)

    def abs(self, value, unit='Hz'):
        "return magnitude (complex modulus, absolute value)"
        return self.fw_abs(value, unit=unit)

    def db(self, value, unit='Hz'):
        "return dB (relative to 1) : 20*log10(|ratio|)"
        try:
            db = self.fw_db(value, unit=unit)
        except ValueError:
            db = None
        return db

    def dbw(self, value, unit='Hz'):
        "return dBW (relative to 1) : 10*log10(|ratio|)"
        try:
            dbw = self.fw_dbw(value, unit=unit)
        except ZeroDivisionError:
            dbw = None
        return dbw

    def phase_rad(self, value, unit='Hz'):
        "return phase in radians (complex argument)"
        return self.fw_phase_rad(value, unit=unit)

    def phase_deg(self, value, unit='Hz'):
        "return phase in degrees (complex argument)"
        return self.fw_phase_deg(value, unit=unit)

    def real(self, value, unit='Hz'):
        "return complex ratio real part"
        return self.fw_real(value, unit=unit)

    def imag(self, value, unit='Hz'):
        "return complex ratio imaginary part"
        return self.fw_imag(value, unit=unit)

    def bode_real(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
                  xscale='log', yscale='linear',
                  magnitude_label='Complex real part',
                  title='Complex real part Bode plot', filename=None):
        """Save datas and draw complex real part Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
Note : cannot be log-scaled if data has no positive values.
filename (str) : save datas to csv format file

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> vin = Voltage(5)
>>> Zr = Impedance(r=1000)
>>> Zt = Impedance(c=100e-9)+Impedance(l=0.1)+Zr
>>> i = vin/Zt;vout = i*Zr;H = vout/vin
>>> i.bode();i.bode_real();i.bode_imag()
>>> vout.bode();vout.bode_real();vout.bode_imag()
>>> H.bode();H.bode_real();H.bode_imag()
>>> show()
"""
        return self.bode(xmin=xmin, xmax=xmax, xunit=xunit, n=n,
                         xscale=xscale, yscale=yscale,
                         magnitude_label=magnitude_label,
                         magnitude_unit='default',
                         title=title, filename=filename,
                         draw_phase=False, mode='real')

    def bode_imag(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
                  xscale='log', yscale='linear',
                  magnitude_label='Complex imaginary part',
                  title='Complex imaginary part Bode plot', filename=None):
        """Save datas and draw complex imaginary part Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
Note : cannot be log-scaled if data has no positive values.
filename (str) : save datas to csv format file

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> vin = Voltage(5)
>>> Zr = Impedance(r=1000)
>>> Zt = Impedance(c=100e-9)+Impedance(l=0.1)+Zr
>>> i = vin/Zt;vout = i*Zr;H = vout/vin
>>> i.bode();i.bode_real();i.bode_imag()
>>> vout.bode();vout.bode_real();vout.bode_imag()
>>> H.bode();H.bode_real();H.bode_imag()
>>> show()
"""
        return self.bode(xmin=xmin, xmax=xmax, xunit=xunit, n=n,
                         xscale=xscale, yscale=yscale,
                         magnitude_label=magnitude_label,
                         magnitude_unit='default',
                         title=title, filename=filename,
                         draw_phase=False, mode='imag')

    @staticmethod
    def transfer_function(numerator=[1], denominator=[1]):
        """
         b0 + b1.w + b2.w² + ...
H(w) =  -------------------------
         a0 + a1.w + a2.w² + ...

w -> rad/s
numerator = [b0, b1, b2,...] -> list of complex numbers
denominator = [a0, a1, a2,...] -> list of complex numbers
return Ratio instance

>>> # first order low-pass filter
>>> # H(w) = 10/(1+1j*w/wn)
>>> wn = 10000
>>> H = Ratio.transfer_function(numerator=[10], denominator=[1, 1j/wn])
>>> H(10000)  # Hz
(0.24704523031857634-1.552230961346476j)
>>> H.bode()
>>> show()
"""
        # transfer function
        # w -> rad/s
        fw = Wfunction(
            lambda w: sum([coeff*w**i for i, coeff in enumerate(numerator)]) /
            sum([coeff*w**i for i, coeff in enumerate(denominator)]))
        return Ratio(fw=fw)

    @staticmethod
    def digital_filter(fs, b=[1], a=[1]):
        """
b = [b0, b1, b2, ...]  -> list of real numbers
a = [1, a1, a2, ...]  -> list of real numbers

y(n) = b0.x(n) + b1.x(n-1) + b2.x(n-2) + ...
       -a1.y(n-1) - a2.y(n-2)  ...

         b0 + b1.z^-1 + b2.z^-2 + ...
H(z) =  -----------------------------
          1 + a1.z^-1 + a2.z^-2 + ...

z = exp(jw/fs)
w -> rad/s
fs = sampling rate (Hz)

return Ratio instance

>>> fs = 100000  # sampling rate (Hz)
>>> H = Ratio.digital_filter(fs=fs, b=[0.1], a=[1, -1.6, 0.7])
>>> H.bode(xmin=fs*0.001, xmax=fs/2, xscale='linear')
>>> show()
"""
        # transfer function
        # w -> rad/s
        fw = Wfunction(
            lambda w: sum([coeff*cmath.exp(1j*w/fs)**-i for i,
                          coeff in enumerate(b)]) /
            sum([coeff*cmath.exp(1j*w/fs)**-i for i, coeff in enumerate(a)]))
        return Ratio(fw=fw)


class Voltage(ElectricalQuantity):
    "The complex Voltage class"

    def __init__(self, RMS=1, phase=0, **kwargs):
        """Creates Voltage object

RMS : positive float (Vrms)
phase in degrees (float)

>>> v1 = Voltage(5, 30)
>>> v1.properties(1000)
Frequency (Hz) : 1000
Angular frequency (rad/s) : 6283.19

Complex voltage : 4.33013+2.5j
Amplitude (Vrms) : 5
Amplitude (V) : 7.07107
Amplitude (dB ref 1 Vrms) : 13.979400086720377
Phase (degrees) : +30
Phase (radians) : +0.523599
v(t) = 7.07107×sin(6283.19×t +0.523599)

>>> v1.RMS = 0.5
>>> v1.phase = -30
>>> v1
Complex voltage (Vrms) : 0.433013-0.25j @ 1.0 kHz

User-defined complex voltage
----------------------------

>>> v2 = Voltage(fw=lambda w: 5/(1+1j*w/1000))
>>> v2(100)  # Hz
(3.5847840016244885-2.252386216841943j)
>>> v2(1000)
(0.12352261515928822-0.7761154806732381j)
"""
        self.unit = 'Vrms'
        self.db_unit = 'dBV'
        ElectricalQuantity.__init__(self)
        self.__RMS, self.__phase = None, None

        if "fw" in kwargs:
            if isinstance(kwargs["fw"], Wfunction):
                self.fw = kwargs["fw"]
            elif inspect.isfunction(kwargs["fw"]):
                self.fw = Wfunction(kwargs["fw"])
            else:
                raise TypeError("function expected")
        else:
            if not isinstance(RMS, (int, float)):
                raise TypeError("number expected")
            if RMS < 0:
                raise ValueError("positive amplitude expected")
            if not isinstance(phase, (int, float)):
                raise TypeError("number expected")
            self.__RMS = RMS
            self.__phase = phase % 360  # degrees
            self.fw = Wfunction(lambda w: cmath.rect(self.__RMS,
                                math.radians(self.__phase)))

        # WFunction instances
        # rms (complex voltage modulus, absolute value)
        self.fw_rms = self.fw.abs()
        # amplitude
        self.fw_amplitude = math.sqrt(2) * self.fw.abs()
        # db ref 1 Vrms
        self.fw_db = self.fw.db()
        # phase in degrees (complex voltage argument)
        self.fw_phase_deg = self.fw.phase_deg()
        # phase in radians (complex voltage argument)
        self.fw_phase_rad = self.fw.phase_rad()
        # complex voltage imaginary part
        self.fw_imag = self.fw.imag()
        # complex voltage real part
        self.fw_real = self.fw.real()

    @property
    def RMS(self):
        # getter
        if self.__RMS is None:
            raise AttributeError("Voltage object has no attribute 'RMS'")
        return self.__RMS

    @RMS.setter
    def RMS(self, value):
        if self.__RMS is None:
            raise AttributeError("Voltage object has no attribute 'RMS'")
        if not isinstance(value, (int, float)):
            raise TypeError("number expected")
        if value < 0:
            raise ValueError("positive amplitude expected")
        self.__RMS = value

    @property
    def phase(self):
        # getter
        if self.__phase is None:
            raise AttributeError("Voltage object has no attribute 'phase'")
        return self.__phase

    @phase.setter
    def phase(self, value):
        if self.__phase is None:
            raise AttributeError("Voltage object has no attribute 'phase'")
        if not isinstance(value, (int, float)):
            raise TypeError("number expected")
        self.__phase = value % 360

    def __call__(self, value, unit='Hz'):
        """ Return the complex voltage (measured in volts)
value : positive float
unit : prefix + 'Hz' or 'rad/s'
"""
        return self.fw(value, unit=unit)

    def properties(self, value, unit='Hz', message=''):
        "Displays the complex voltage properties"
        # f : frequency (Hz) ; w : angular frequency (rad/s)
        (f, w) = getfrequency(value=value, unit=unit)

        affichage = '' if message is '' else message + '\n'
        affichage += """Frequency (Hz) : {:g}
Angular frequency (rad/s) : {:g}

Complex voltage : {:g}
Amplitude (Vrms) : {:g}
Amplitude (V) : {:g}
Amplitude (dBV ref 1 Vrms) : {}
Phase (degrees) : {:+g}
Phase (radians) : {:+g}
v(t) = {:g}×sin({:g}×t {:+f})
""".format(f, w, self(f, 'Hz'),
           self.rms(f, 'Hz'), self.amplitude(f, 'Hz'),
           self.dbv(f, 'Hz'),
           self.phase_deg(f, 'Hz'), self.phase_rad(f, 'Hz'),
           self.amplitude(f, 'Hz'), w, self.phase_rad(f, 'Hz'))
        print(affichage)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Complex voltage (Vrms) : {:g} @ {} {}Hz".format(
            self(value=ElectricalQuantity.DEFAULT_FREQUENCY, unit='Hz'),
            *EngineeringNotation(ElectricalQuantity.DEFAULT_FREQUENCY))

    def __add__(self, voltage):
        """self.__add__(voltage) <=> self + voltage
Kirchhoff’s voltage law
Return Voltage
>>> v3 = v1+v2
"""
        return Law().KVL('++', self, voltage)

    def __sub__(self, voltage):
        """self.__sub__(voltage) <=> self - voltage
Kirchhoff’s voltage law
Return Voltage
>>> v3 = v1-v2
"""
        return Law().KVL('+-', self, voltage)

    def __pos__(self):
        """self.__pos__() <=> +self
Return Voltage """
        return Voltage(fw=self.fw)  # new object

    def __neg__(self):
        """self.__neg__() <=> -self
Return Voltage"""
        return Voltage(fw=-self.fw)

    def __truediv__(self, arg):
        """self.__truediv__(arg) <=> self / arg

arg is Impedance, Current, Voltage, Ratio or complex number.

arg -> Impedance :
Ohm's law
Return Current
>>> i1 = v1/z1

arg -> Current :
Ohm's law
Return Impedance
>>> z1 = v1/i1

arg -> complex number :
Return Voltage
>>> v2 = v1/10

arg -> Voltage :
Return Ratio
>>> x = v1/v2

arg -> Ratio :
Return Voltage
>>> x = z1/z2
>>> v2 = v1/x
"""
        if isinstance(arg, Impedance) is True:
            return Law().Ohm(v=self, z=arg)
        if isinstance(arg, Ratio) is True:
            return Voltage(fw=self.fw / arg.fw)
        if isinstance(arg, Voltage) is True:
            return Ratio(fw=self.fw / arg.fw)
        if isinstance(arg, Current) is True:
            return Law().Ohm(v=self, i=arg)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Voltage(fw=self.fw / arg)

    def __mul__(self, arg):
        """self.__mul__(arg) <=> self * arg

arg is Admittance, Current, Ratio or complex number.

arg ->  Admittance :
Ohm's law
Return Current
>>> i1 = v1*y1

arg -> Current :
Return complex Power
>>> s1 = v1*i1

arg -> complex number :
Return Voltage
>>> v2 = v1*0.1

arg -> Ratio :
Return Voltage
"""
        if isinstance(arg, Admittance) is True:
            return Current(fw=self.fw*arg.fw)
        if isinstance(arg, Current) is True:
            return Law().Power(v=self, i=arg)
        if isinstance(arg, Ratio) is True:
            return Voltage(fw=self.fw*arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Voltage(fw=self.fw*arg)

    def __rmul__(self, value):
        """self.__rmul__(value) <=> value * self
value -> complex number
Return Voltage
>>> v2 = 0.1*v1
"""
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        return Voltage(fw=value * self.fw)

    def rms(self, value, unit='Hz'):
        "return rms (V)"
        return self.fw_rms(value, unit=unit)

    def amplitude(self, value, unit='Hz'):
        "return amplitude = rms*sqrt(2) (V)"
        return self.fw_amplitude(value, unit=unit)

    def dbv(self, value, unit='Hz'):
        "return dBV (relative to 1 Vrms) : 20*log10(Vrms)"
        try:
            db = self.fw_db(value, unit=unit)
        except ValueError:
            db = None
        return db

    def phase_deg(self, value, unit='Hz'):
        "return phase in degrees (complex impedance argument)"
        return self.fw_phase_deg(value, unit=unit)

    def phase_rad(self, value, unit='Hz'):
        "return phase in radians (complex impedance argument)"
        return self.fw_phase_rad(value, unit=unit)

    def real(self, value, unit='Hz'):
        "return complex voltage real part"
        return self.fw_real(value, unit=unit)

    def imag(self, value, unit='Hz'):
        "return complex voltage imaginary part"
        return self.fw_imag(value, unit=unit)

    def bode_real(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
                  xscale='log', yscale='linear',
                  magnitude_label='Complex real part',
                  title='Complex real part Bode plot', filename=None):
        """Save datas and draw complex real part Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
Note : cannot be log-scaled if data has no positive values.
filename (str) : save datas to csv format file

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> vin = Voltage(5)
>>> Zr = Impedance(r=1000)
>>> Zt = Impedance(c=100e-9)+Impedance(l=0.1)+Zr
>>> i = vin/Zt;vout = i*Zr;H = vout/vin
>>> i.bode();i.bode_real();i.bode_imag()
>>> vout.bode();vout.bode_real();vout.bode_imag()
>>> H.bode();H.bode_real();H.bode_imag()
>>> show()
"""
        return self.bode(xmin=xmin, xmax=xmax, xunit=xunit, n=n,
                         xscale=xscale, yscale=yscale,
                         magnitude_label=magnitude_label,
                         magnitude_unit='default',
                         title=title, filename=filename,
                         draw_phase=False, mode='real')

    def bode_imag(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
                  xscale='log', yscale='linear',
                  magnitude_label='Complex imaginary part',
                  title='Complex imaginary part Bode plot', filename=None):
        """Save datas and draw complex imaginary part Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
Note : cannot be log-scaled if data has no positive values.
filename (str) : save datas to csv format file

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> vin = Voltage(5)
>>> Zr = Impedance(r=1000)
>>> Zt = Impedance(c=100e-9)+Impedance(l=0.1)+Zr
>>> i = vin/Zt;vout = i*Zr;H = vout/vin
>>> i.bode();i.bode_real();i.bode_imag()
>>> vout.bode();vout.bode_real();vout.bode_imag()
>>> H.bode();H.bode_real();H.bode_imag()
>>> show()
"""
        return self.bode(xmin=xmin, xmax=xmax, xunit=xunit, n=n,
                         xscale=xscale, yscale=yscale,
                         magnitude_label=magnitude_label,
                         magnitude_unit='default',
                         title=title, filename=filename,
                         draw_phase=False, mode='imag')


class Current(ElectricalQuantity):
    "The complex Current class"

    def __init__(self, RMS=1, phase=0, **kwargs):
        """Creates Current object

RMS : positive float (Arms)
phase in degrees (float)

>>> i1 = Current(0.2, -60)
>>> i1
Complex current (Arms) : 0.1-0.173205j @ 1 kHz
>>> i1.RMS = 0.5
>>> i1.phase = 30
>>> i1
Complex current (Arms) : 0.433013+0.25j @ 1.0 kHz

User-defined complex current
----------------------------

>>> i2 = Current(fw=lambda w: 5/(1+1000j/w))
>>> i2(10000)  # Hz
(4.998733805935174-0.0795573194415146j)
>>> i2(100)
(1.415215998375511-2.252386216841943j)
"""
        ElectricalQuantity.__init__(self)
        self.unit = 'Arms'
        self.db_unit = 'dBA'
        self.__RMS, self.__phase = None, None

        if "fw" in kwargs:
            if isinstance(kwargs["fw"], Wfunction):
                self.fw = kwargs["fw"]
            elif inspect.isfunction(kwargs["fw"]):
                self.fw = Wfunction(kwargs["fw"])
            else:
                raise TypeError("function expected")
        else:
            if not isinstance(RMS, (int, float)):
                raise TypeError("number expected")
            if RMS < 0:
                raise ValueError("positive amplitude expected")
            if not isinstance(phase, (int, float)):
                raise TypeError("number expected")
            self.__RMS = RMS
            self.__phase = phase % 360  # degrees
            self.fw = Wfunction(lambda w: cmath.rect(self.__RMS,
                                math.radians(self.__phase)))

        # WFunction instances
        # rms (complex current modulus, absolute value)
        self.fw_rms = self.fw.abs()
        # db ref 1 Arms
        self.fw_db = self.fw.db()
        # amplitude (complex current modulus, absolute value)
        self.fw_amplitude = math.sqrt(2) * self.fw.abs()
        # phase in degrees (complex current argument)
        self.fw_phase_deg = self.fw.phase_deg()
        # phase in radians (complex current argument)
        self.fw_phase_rad = self.fw.phase_rad()
        # complex current imaginary part
        self.fw_imag = self.fw.imag()
        # complex current real part
        self.fw_real = self.fw.real()

    @property
    def RMS(self):
        # getter
        if self.__RMS is None:
            raise AttributeError("Current object has no attribute 'RMS'")
        return self.__RMS

    @RMS.setter
    def RMS(self, value):
        if self.__RMS is None:
            raise AttributeError("Current object has no attribute 'RMS'")
        if not isinstance(value, (int, float)):
            raise TypeError("number expected")
        if value < 0:
            raise ValueError("positive amplitude expected")
        self.__RMS = value

    @property
    def phase(self):
        # getter
        if self.__phase is None:
            raise AttributeError("Current object has no attribute 'phase'")
        return self.__phase

    @phase.setter
    def phase(self, value):
        if self.__phase is None:
            raise AttributeError("Current object has no attribute 'phase'")
        if not isinstance(value, (int, float)):
            raise TypeError("number expected")
        self.__phase = value % 360

    def __call__(self, value, unit='Hz'):
        """Return the complex current (measured in amperes)
value : positive float
unit : prefix + 'Hz' or 'rad/s'
"""
        return self.fw(value, unit=unit)

    def properties(self, value, unit='Hz', message=''):
        "Displays the Current properties"

        # f : frequency (Hz) ; w : angular frequency (rad/s)
        (f, w) = getfrequency(value=value, unit=unit)

        affichage = '' if message is '' else message + '\n'
        affichage += """Frequency (Hz) : {:g}
Angular frequency (rad/s) : {:g}

Complex current : {:g}
Amplitude (Arms) : {:g}
Amplitude (A) : {:g}
Amplitude (dBA ref 1 Arms) : {}
Phase (degrees) : {:+g}
Phase (radians) : {:+g}
i(t) = {:g}×sin({:g}×t {:+f})
""".format(f, w, self(f, 'Hz'),
           self.rms(f, 'Hz'), self.amplitude(f, 'Hz'),
           self.dba(f, 'Hz'),
           self.phase_deg(f, 'Hz'), self.phase_rad(f, 'Hz'),
           self.amplitude(f, 'Hz'), w, self.phase_rad(f, 'Hz'))
        print(affichage)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Complex current (Arms) : {:g} @ {} {}Hz".format(
            self(value=ElectricalQuantity.DEFAULT_FREQUENCY, unit='Hz'),
            *EngineeringNotation(ElectricalQuantity.DEFAULT_FREQUENCY))

    def __add__(self, current):
        """self.__add__(current) <=> self + current
Kirchhoff’s current law
Return Current
>>> i3 = i1+i2
"""
        return Law().KCL('++', self, current)

    def __sub__(self, current):
        """self.__sub__(current) <=> self - current
Kirchhoff’s current law
Return Current
>>> i3 = i1-i2
"""
        return Law().KCL('+-', self, current)

    def __pos__(self):
        """self.__pos__() <=> +self
Return Current"""
        return Current(fw=self.fw)  # new instance

    def __neg__(self):
        """self.__neg__() <=> -self
Return Current"""
        return Current(fw=-self.fw)

    def __truediv__(self, arg):
        """self.__truediv__(arg) <=> self / arg

arg is Current, Admittance, Voltage, Ratio or complex number.

arg -> Admittance :
Ohm's law
Return Voltage
>>> v1 = i1/y1

arg -> Voltage :
Ohm's law
Return Admittance
>>> y1 = i1/v1

arg -> complex number :
Return Current
>>> i2 = i1/10

arg -> Current :
Return Ratio
>>> x = i1/i2

arg -> Ratio :
Return Current
>>> x = z1/z2
>>> i2 = i1/x
"""
        if isinstance(arg, Admittance) is True:
            return Voltage(fw=self.fw/arg.fw)
        if isinstance(arg, Current) is True:
            return Ratio(fw=self.fw/arg.fw)
        if isinstance(arg, Voltage) is True:
            return Admittance(fw=self.fw/arg.fw)
        if isinstance(arg, Ratio) is True:
            return Current(fw=self.fw/arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Current(fw=self.fw/arg)

    def __mul__(self, arg):
        """self.__mul__(arg) <=> self * arg

arg is Impedance, Voltage, Ratio or complex number.

arg -> Impedance :
Ohm's law
Return Voltage
>>> v1 = i1*z1

arg -> Voltage :
Return complex Power
>>> p1 = i1*v1

arg -> complex number :
Return Current
>>> i2 = i1*10

arg -> Ratio :
Return Current
>>> x = z2/z1
>>> i2 = i1*x
"""
        if isinstance(arg, Impedance) is True:
            return Voltage(fw=self.fw * arg.fw)
        if isinstance(arg, Voltage) is True:
            return Law().Power(v=arg, i=self)
        if isinstance(arg, Ratio) is True:
            return Current(fw=self.fw * arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Current(fw=self.fw * arg)

    def __rmul__(self, value):
        """self.__rmul__(value) <=> value * self
value -> complex number
Return Current
>>> i2 = 10*i1
"""
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        return Current(fw=value * self.fw)

    def rms(self, value, unit='Hz'):
        "return rms (A)"
        return self.fw_rms(value, unit=unit)

    def dba(self, value, unit='Hz'):
        "return dBA (relative to 1 Arms) : 20*log10(|Irms|)"
        try:
            db = self.fw_db(value, unit=unit)
        except ValueError:
            db = None
        return db

    def amplitude(self, value, unit='Hz'):
        "return amplitude : rms*sqrt(2) (A)"
        return self.fw_amplitude(value, unit=unit)

    def phase_deg(self, value, unit='Hz'):
        "return phase in degrees (complex current argument)"
        return self.fw_phase_deg(value, unit=unit)

    def phase_rad(self, value, unit='Hz'):
        "return phase in radians (complex current argument)"
        return self.fw_phase_rad(value, unit=unit)

    def real(self, value, unit='Hz'):
        "return complex current real part"
        return self.fw_real(value, unit=unit)

    def imag(self, value, unit='Hz'):
        "return complex current imaginary part"
        return self.fw_imag(value, unit=unit)

    def bode_real(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
                  xscale='log', yscale='linear',
                  magnitude_label='Complex real part',
                  title='Complex real part Bode plot', filename=None):
        """Save datas and draw complex real part Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
Note : cannot be log-scaled if data has no positive values.
filename (str) : save datas to csv format file

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> vin = Voltage(5)
>>> Zr = Impedance(r=1000)
>>> Zt = Impedance(c=100e-9)+Impedance(l=0.1)+Zr
>>> i = vin/Zt;vout = i*Zr;H = vout/vin
>>> i.bode();i.bode_real();i.bode_imag()
>>> vout.bode();vout.bode_real();vout.bode_imag()
>>> H.bode();H.bode_real();H.bode_imag()
>>> show()
"""
        return self.bode(xmin=xmin, xmax=xmax, xunit=xunit, n=n,
                         xscale=xscale, yscale=yscale,
                         magnitude_label=magnitude_label,
                         magnitude_unit='default',
                         title=title, filename=filename,
                         draw_phase=False, mode='real')

    def bode_imag(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
                  xscale='log', yscale='linear',
                  magnitude_label='Complex imaginary part',
                  title='Complex imaginary part Bode plot', filename=None):
        """Save datas and draw complex imaginary part Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
Note : cannot be log-scaled if data has no positive values.
filename (str) : save datas to csv format file

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> vin = Voltage(5)
>>> Zr = Impedance(r=1000)
>>> Zt = Impedance(c=100e-9)+Impedance(l=0.1)+Zr
>>> i = vin/Zt;vout = i*Zr;H = vout/vin
>>> i.bode();i.bode_real();i.bode_imag()
>>> vout.bode();vout.bode_real();vout.bode_imag()
>>> H.bode();H.bode_real();H.bode_imag()
>>> show()
"""
        return self.bode(xmin=xmin, xmax=xmax, xunit=xunit, n=n,
                         xscale=xscale, yscale=yscale,
                         magnitude_label=magnitude_label,
                         magnitude_unit='default',
                         title=title, filename=filename,
                         draw_phase=False, mode='imag')


class Power(ElectricalQuantity):
    """The complex Power class
S = V.I* = P +jQ"""

    def __init__(self, power=1+0j, **kwargs):
        """Creates complex Power object
>>> s = Power(1000-100j)

User-defined complex power function
-----------------------------------
>>> s = Power(fw=lambda w: 1/(1+1000j/w))
"""
        ElectricalQuantity.__init__(self)
        self.unit = 'W'
        self.db_unit = 'dBW'
        self.__power = None

        if "fw" in kwargs:
            if isinstance(kwargs["fw"], Wfunction):
                self.fw = kwargs["fw"]
            elif inspect.isfunction(kwargs["fw"]):
                self.fw = Wfunction(kwargs["fw"])
            else:
                raise TypeError("function expected")
        else:
            if not isinstance(power, (int, float, complex)):
                raise TypeError("number expected")
            self.__power = power
            self.fw = Wfunction(lambda w: self.__power)

        # WFunction instances
        self.fw_w = self.fw.real()
        self.fw_dbw = self.fw_w.dbw()
        self.fw_va = self.fw.abs()
        self.fw_var = self.fw.imag()
        self.fw_phase_deg = self.fw.phase_deg()
        self.fw_phase_rad = self.fw.phase_rad()
        self.fw_pf = self.fw_w/self.fw_va

    @property
    def power(self):
        # getter
        if self.__power is None:
            raise AttributeError("Power object has no attribute 'power'")
        return self.__power

    @power.setter
    def power(self, value):
        if self.__power is None:
            raise AttributeError("Power object has no attribute 'power'")
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        self.__power = value

    def __call__(self, value, unit='Hz'):
        """Return the complex power (measured in watts)
value : positive float
unit : prefix + 'Hz' or 'rad/s'
"""
        return self.fw(value, unit=unit)

    def properties(self, value, unit='Hz', message=''):
        "Displays the complex power properties"
        # f : frequency (Hz) ; w : angular frequency (rad/s)
        (f, w) = getfrequency(value=value, unit=unit)

        affichage = '' if message is '' else message + '\n'
        affichage += """Frequency (Hz) : {:g}
Angular frequency (rad/s) : {:g}

Complex power : {:g}

Active power P (W) : {:+g}
Reactive power Q (var) : {:+g}
Apparent power S (VA) : {:g}

Phase (degrees) : {:+g}
Phase (radians) : {:+g}
Power factor PF : {}

Active power (dBW ref 1 W) : {}
""".format(f, w, self(f, 'Hz'),
           self.w(f, 'Hz'), self.var(f, 'Hz'),
           self.va(f, 'Hz'),
           self.phase_deg(f, 'Hz'), self.phase_rad(f, 'Hz'),
           self.pf(f, 'Hz'), self.dbw(f, 'Hz'))
        print(affichage)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Complex power (W): {:g} @ {} {}Hz".format(
            self(value=ElectricalQuantity.DEFAULT_FREQUENCY, unit='Hz'),
            *EngineeringNotation(ElectricalQuantity.DEFAULT_FREQUENCY))

    def __add__(self, power):
        """self.__add__(power) <=> self + power
Return Power"""
        if isinstance(power, Power) is False:
                raise TypeError("Power expected")
        return Power(fw=self.fw + power.fw)

    def __sub__(self, power):
        """self.__sub__(power) <=> self - power
Return Power"""
        if isinstance(power, Power) is False:
                raise TypeError("Power expected")
        return Power(fw=self.fw - power.fw)

    def __pos__(self):
        """self.__pos__() <=> +self
Return Power"""
        return Power(fw=self.fw)  # new object

    def __neg__(self):
        """self.__neg__() <=> -self
Return Power"""
        return Power(fw=-self.fw)

    def __truediv__(self, arg):
        """self.__truediv__(arg) <=> self / arg

arg is a Voltage, Current, Power, Ratio or complex number

>>> i1 = s1/v1
>>> s2 = s1/5
>>> v1 = s1/i1
>>> x = s1/s2  # complex ratio
>>> s2 = s1/x
"""
        if isinstance(arg, Voltage) is True:
            return Current(fw=(self.fw/arg.fw).conjugate())
        if isinstance(arg, Current) is True:
            return Voltage(fw=self.fw/(arg.fw.conjugate()))
        if isinstance(arg, Ratio) is True:
            return Power(fw=self.fw/arg.fw)
        if isinstance(arg, Power) is True:
            return Ratio(fw=self.fw/arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Power(fw=self.fw/arg)

    def __mul__(self, arg):
        """self.__mul__(arg) <=> self * arg
>>> s2 = s1*10
>>> x = s2/s1  # complex ratio
>>> s2 = s1*x
"""
        if isinstance(arg, Ratio) is True:
            return Power(fw=self.fw * arg.fw)
        if not isinstance(arg, (int, float, complex)):
            raise TypeError("number expected")
        return Power(fw=self.fw * arg)

    def __rmul__(self, value):
        """self.__rmul__(value) <=> value * self
>>> s2 = 10*s1
"""
        if not isinstance(value, (int, float, complex)):
            raise TypeError("number expected")
        return Power(fw=value * self.fw)

    def w(self, value, unit='Hz'):
        """S = P +jQ
return active power P (real power) in watts (W)"""
        return self.fw_w(value, unit=unit)

    def dbw(self, value, unit='Hz'):
        "return active power P (real power) in dBW (relative to 1 W)"
        try:
            dbw = self.fw_dbw(value, unit=unit)
        except ValueError:
            dbw = None
        return dbw

    def var(self, value, unit='Hz'):
        """S = P +jQ
return reactive power Q in volt-ampere reactive (var)"""
        return self.fw_var(value, unit=unit)

    def va(self, value, unit='Hz'):
        "return apparent power S (magnitude of complex power) \
in volt-ampere (VA)"
        return self.fw_va(value, unit=unit)

    def phase_deg(self, value, unit='Hz'):
        "return phase of voltage relative to current φ in degrees : \
the angle of difference between current and voltage"
        return self.fw_phase_deg(value, unit=unit)

    def phase_rad(self, value, unit='Hz'):
        "return phase of voltage relative to current φ in radians : \
the angle of difference between current and voltage"
        return self.fw_phase_rad(value, unit=unit)

    def pf(self, value, unit='Hz'):
        "return power factor cos(φ): \
the ratio of active power P to apparent power S"
        try:
            pf = self.fw_pf(value, unit=unit)
        except ZeroDivisionError:
            pf = None
        return pf

    def bode_va(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
                xscale='log', yscale='linear',
                magnitude_label='Apparent power',
                title='Apparent power Bode plot', filename=None):
        """Save datas and draw apparent power S (VA) Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
Note : cannot be log-scaled if data has no positive values.
filename (str) : save datas to csv format file

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> vin = Voltage(5)
>>> Zt = Impedance(c=100e-9)+Impedance(l=0.1)+Impedance(r=1000)
>>> i = vin/Zt
>>> S = i*vin
>>> S.bode();S.bode(magnitude_unit='default')
>>> S.bode_va();S.bode_var();S.bode_pf()
>>> show()
"""
        return self.bode(xmin=xmin, xmax=xmax, xunit=xunit, n=n,
                         xscale=xscale, yscale=yscale,
                         magnitude_label=magnitude_label,
                         magnitude_unit='default',
                         title=title, filename=filename,
                         draw_phase=False, mode='va')

    def bode_var(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
                 xscale='log', yscale='linear',
                 magnitude_label='Reactive power',
                 title='Reactive power Bode plot', filename=None):
        """Save datas and draw reactive power Q (var) Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
Note : cannot be log-scaled if data has no positive values.
filename (str) : save datas to csv format file

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> vin = Voltage(5)
>>> Zt = Impedance(c=100e-9)+Impedance(l=0.1)+Impedance(r=1000)
>>> i = vin/Zt
>>> S = i*vin
>>> S.bode();S.bode(magnitude_unit='default')
>>> S.bode_va();S.bode_var();S.bode_pf()
>>> show()
"""
        return self.bode(xmin=xmin, xmax=xmax, xunit=xunit, n=n,
                         xscale=xscale, yscale=yscale,
                         magnitude_label=magnitude_label,
                         magnitude_unit='default',
                         title=title, filename=filename,
                         draw_phase=False, mode='var')

    def bode_pf(self, xmin=10, xmax=100000, xunit='Hz', n=1000,
                xscale='log', yscale='linear',
                magnitude_label='Power factor',
                title='Power factor Bode plot', filename=None):
        """Save datas and draw power factor Bode plot
xunit = prefix + ['Hz' | 'rad/s']
n = number of points (int)
xscale = ['log' | 'linear']
yscale = ['log' | 'linear']
Note : cannot be log-scaled if data has no positive values.
filename (str) : save datas to csv format file

return fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

>>> vin = Voltage(5)
>>> Zt = Impedance(c=100e-9)+Impedance(l=0.1)+Impedance(r=1000)
>>> i = vin/Zt
>>> S = i*vin
>>> S.bode();S.bode(magnitude_unit='default')
>>> S.bode_va();S.bode_var();S.bode_pf()
>>> show()
"""
        return self.bode(xmin=xmin, xmax=xmax, xunit=xunit, n=n,
                         xscale=xscale, yscale=yscale,
                         magnitude_label=magnitude_label,
                         magnitude_unit='default',
                         title=title, filename=filename,
                         draw_phase=False, mode='pf')


if __name__ == '__main__':
    import acelectricity as ac
    help(ac)
