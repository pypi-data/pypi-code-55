from math import floor, pi

from .iau2000 import _obliquity_iau2006
from ...constants import ARCSEC_TO_RAD, JULIAN_CENTURY
from ...utils.rotation import angles2matrix


def era2000(date):
    """ Earth rotation angle (IAU 2000)

        era: Earth Rotation Angle [rad]
        eradot: Earth Rotation angular velocity [rad/s]
    """
    date_ut1 = date.change_scale("UT1")
    jd_d, jd_fod = date_ut1.julian_date()
    t = (jd_d - 2451545) + jd_fod
    f = (jd_d - floor(jd_d)) + (jd_fod - floor(jd_fod))
    # formula 5.15
    era = (2 * pi * (f + 0.7790572732640 + 0.00273781191135448 * t)) % (2 * pi)
    eradot = 2 * pi * 1.00273781191135448 / 86400
    return era, eradot


def _bias2006():
    """Bias matrix (IAU2006) from the GCRS frame to the EME2000 frame.
        u_EME2000 = B * u_GCRS
    """
    gamb, phib, psib, epsa = _prec2006([2451545, 0])
    return angles2matrix([3, 1, 3, 1], [gamb, phib, -psib, -epsa])


def _prec2006(jd):
    """ Precession angles(IAU2006) Compute the 4 angles of Fukushima - Williams precession:
     - epsa is the mean obliquity of date
     - gamb(gamma bar) is the GCRS right ascension of the intersection of the ecliptic of date with the GCRS equator
     - phib(phi bar) is the obliquity of the ecliptic of date on the GCRS equator
     - psib(psi bar) is the precession angle plus bias in longitude along the ecliptic of date

         gamb, phib, psib, epsa: precession angles[rad](1xN)
         gambdot, phibdot, psibdot, epsadot: Time derivatives of precession angles[rad / s](1xN)
    """
    t = ((jd[0] - 2451545) + jd[1]) / 36525

    # (eq 5.40, p65, paragraph 5.6.4)
    gamb = (
        -0.052928
        + (
            10.556378
            + (0.4932044 + (-0.00031238 + (-0.000002788 + (0.0000000260) * t) * t) * t)
            * t
        )
        * t
    ) * ARCSEC_TO_RAD
    phib = (
        84381.412819
        + (
            -46.811016
            + (0.0511268 + (0.00053289 + (-0.000000440 + (-0.0000000176) * t) * t) * t)
            * t
        )
        * t
    ) * ARCSEC_TO_RAD
    psib = (
        -0.041775
        + (
            5038.481484
            + (1.5584175 + (-0.00018522 + (-0.000026452 + (-0.0000000148) * t) * t) * t)
            * t
        )
        * t
    ) * ARCSEC_TO_RAD

    # Mean obliquity of the ecliptic, IAU2006 precession model.
    epsa = _obliquity_iau2006(t)

    return gamb, phib, psib, epsa
