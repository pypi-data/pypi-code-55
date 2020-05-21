import numpy as np

from ...constants import ARCSEC_TO_RAD, TWO_PI


def _luni_solar(tjc):
    # formula Eq.5.43
    # F1, Mean anomaly of the Moon, arcsec
    M_moon = 485868.249036 + tjc * (1717915923.2178 + tjc * (31.8792 + tjc * (0.051635 + tjc * (-0.0002447))))

    # F2, Mean anomaly of the sun, arcsec
    M_sun = 1287104.79305 + tjc * (129596581.0481 + tjc * (-0.5532 + tjc * (0.000136 + tjc * (-0.00001149 ))))

    u_M_moon = (335779.526232 + tjc * (1739527262.8478 + tjc * (-12.7512 + tjc * (-0.001037 + tjc * 0.00000417))))

    # F4, Mean elongation of the Moon from the Sun, arcsec
    D_sun = 1072260.70369 + tjc * (1602961601.209 + tjc * (-6.3706 + tjc * (0.006593 + tjc * (-0.00003169))))

    # F5, Mean longitude of the ascending node of the Moon, arcsec
    Omega_moon = 450160.398036 + tjc * (-6962890.5431 + tjc * (7.4722 + tjc * (0.007702 + tjc * (-0.00005939))))

    ls = np.array(
        [
            M_moon * ARCSEC_TO_RAD,
            M_sun * ARCSEC_TO_RAD,
            u_M_moon * ARCSEC_TO_RAD,
            D_sun * ARCSEC_TO_RAD,
            Omega_moon * ARCSEC_TO_RAD,
        ]
    )
    return ls % TWO_PI


def _planets(tjc):
    # formula 5.44. All in radians
    lambda_M_mercury = 4.402608842 + 2608.7903141574 * tjc
    lambda_M_venus = 3.176146697 + 1021.3285546211 * tjc
    lambda_M_earth = 1.753470314 + 628.3075849991 * tjc
    lambda_M_mars = 6.203480913 + 334.06124267 * tjc
    lambda_M_jupiter = 0.599546497 + 52.9690962641 * tjc
    lambda_M_saturn = 0.874016757 + 21.3299104960 * tjc
    lambda_M_uranus = 5.481293872 + 7.4781598567 * tjc
    lambda_M_neptune = 5.311886287 + 3.8133035638 * tjc
    p_lambda = 0.02438175 * tjc + 0.00000538691 * tjc ** 2

    #
    planets = np.array(
        [
            lambda_M_mercury,
            lambda_M_venus,
            lambda_M_earth,
            lambda_M_mars,
            lambda_M_jupiter,
            lambda_M_saturn,
            lambda_M_uranus,
            lambda_M_neptune,
            p_lambda,
        ]
    )
    return planets % TWO_PI


def nut_argument(tjc, p_coefs):
    """Fundamental argument of the nutation theory, radians"""
    lunisol = _luni_solar(tjc)
    planets = _planets(tjc)
    arg = np.dot(p_coefs, np.concatenate((lunisol, planets), axis=None))
    return arg
