import numpy as np

import materia

from .dataseries import ReflectanceSpectrum


class CIE1995TestColorSample01(ReflectanceSpectrum):
    def __init__(self):
        # data taken from https://web.archive.org/web/20090211042805/http://photometry.kriss.re.kr/wiki/img_auth.php/4/47/CIE_TCS.csv
        x = materia.Qty(value=np.linspace(360, 830, 95), unit=materia.nanometer)

        tcs01 = [
            0.116,
            0.136,
            0.159,
            0.19,
            0.219,
            0.239,
            0.252,
            0.256,
            0.256,
            0.254,
            0.252,
            0.248,
            0.244,
            0.24,
            0.237,
            0.232,
            0.23,
            0.226,
            0.225,
            0.222,
            0.22,
            0.218,
            0.216,
            0.214,
            0.214,
            0.214,
            0.216,
            0.218,
            0.223,
            0.225,
            0.226,
            0.226,
            0.225,
            0.225,
            0.227,
            0.23,
            0.236,
            0.245,
            0.253,
            0.262,
            0.272,
            0.283,
            0.298,
            0.318,
            0.341,
            0.367,
            0.39,
            0.409,
            0.424,
            0.435,
            0.442,
            0.448,
            0.45,
            0.451,
            0.451,
            0.451,
            0.451,
            0.451,
            0.45,
            0.45,
            0.451,
            0.451,
            0.453,
            0.454,
            0.455,
            0.457,
            0.458,
            0.46,
            0.462,
            0.463,
            0.464,
            0.465,
            0.466,
            0.466,
            0.466,
            0.466,
            0.467,
            0.467,
            0.467,
            0.467,
            0.467,
            0.467,
            0.467,
            0.467,
            0.467,
            0.467,
            0.467,
            0.466,
            0.466,
            0.466,
            0.466,
            0.466,
            0.465,
            0.464,
            0.464,
        ]
        y = materia.Qty(value=tcs01, unit=materia.unitless)

        super().__init__(x=x, y=y)


class CIE1995TestColorSample02(ReflectanceSpectrum):
    def __init__(self):
        # data taken from https://web.archive.org/web/20090211042805/http://photometry.kriss.re.kr/wiki/img_auth.php/4/47/CIE_TCS.csv
        x = materia.Qty(value=np.linspace(360, 830, 95), unit=materia.nanometer)

        tcs02 = [
            0.053,
            0.055,
            0.059,
            0.064,
            0.07,
            0.079,
            0.089,
            0.101,
            0.111,
            0.116,
            0.118,
            0.12,
            0.121,
            0.122,
            0.122,
            0.122,
            0.123,
            0.124,
            0.127,
            0.128,
            0.131,
            0.134,
            0.138,
            0.143,
            0.15,
            0.159,
            0.174,
            0.19,
            0.207,
            0.225,
            0.242,
            0.253,
            0.26,
            0.264,
            0.267,
            0.269,
            0.272,
            0.276,
            0.282,
            0.289,
            0.299,
            0.309,
            0.322,
            0.329,
            0.335,
            0.339,
            0.341,
            0.341,
            0.342,
            0.342,
            0.342,
            0.341,
            0.341,
            0.339,
            0.339,
            0.338,
            0.338,
            0.337,
            0.336,
            0.335,
            0.334,
            0.332,
            0.332,
            0.331,
            0.331,
            0.33,
            0.329,
            0.328,
            0.328,
            0.327,
            0.326,
            0.325,
            0.324,
            0.324,
            0.324,
            0.323,
            0.322,
            0.321,
            0.32,
            0.318,
            0.316,
            0.315,
            0.315,
            0.314,
            0.314,
            0.313,
            0.313,
            0.312,
            0.312,
            0.311,
            0.311,
            0.311,
            0.311,
            0.311,
            0.31,
        ]
        y = materia.Qty(value=tcs02, unit=materia.unitless)

        super().__init__(x=x, y=y)


class CIE1995TestColorSample03(ReflectanceSpectrum):
    def __init__(self):
        # data taken from https://web.archive.org/web/20090211042805/http://photometry.kriss.re.kr/wiki/img_auth.php/4/47/CIE_TCS.csv
        x = materia.Qty(value=np.linspace(360, 830, 95), unit=materia.nanometer)

        tcs03 = [
            0.058,
            0.059,
            0.061,
            0.063,
            0.065,
            0.068,
            0.07,
            0.072,
            0.073,
            0.073,
            0.074,
            0.074,
            0.074,
            0.073,
            0.073,
            0.073,
            0.073,
            0.073,
            0.074,
            0.075,
            0.077,
            0.08,
            0.085,
            0.094,
            0.109,
            0.126,
            0.148,
            0.172,
            0.198,
            0.221,
            0.241,
            0.26,
            0.278,
            0.302,
            0.339,
            0.37,
            0.392,
            0.399,
            0.4,
            0.393,
            0.38,
            0.365,
            0.349,
            0.332,
            0.315,
            0.299,
            0.285,
            0.272,
            0.264,
            0.257,
            0.252,
            0.247,
            0.241,
            0.235,
            0.229,
            0.224,
            0.22,
            0.217,
            0.216,
            0.216,
            0.219,
            0.224,
            0.23,
            0.238,
            0.251,
            0.269,
            0.288,
            0.312,
            0.34,
            0.366,
            0.39,
            0.412,
            0.431,
            0.447,
            0.46,
            0.472,
            0.481,
            0.488,
            0.493,
            0.497,
            0.5,
            0.502,
            0.505,
            0.51,
            0.516,
            0.52,
            0.524,
            0.527,
            0.531,
            0.535,
            0.539,
            0.544,
            0.548,
            0.552,
            0.555,
        ]
        y = materia.Qty(value=tcs03, unit=materia.unitless)

        super().__init__(x=x, y=y)


class CIE1995TestColorSample04(ReflectanceSpectrum):
    def __init__(self):
        # data taken from https://web.archive.org/web/20090211042805/http://photometry.kriss.re.kr/wiki/img_auth.php/4/47/CIE_TCS.csv
        x = materia.Qty(value=np.linspace(360, 830, 95), unit=materia.nanometer)

        tcs04 = [
            0.057,
            0.059,
            0.062,
            0.067,
            0.074,
            0.083,
            0.093,
            0.105,
            0.116,
            0.121,
            0.124,
            0.126,
            0.128,
            0.131,
            0.135,
            0.139,
            0.144,
            0.151,
            0.161,
            0.172,
            0.186,
            0.205,
            0.229,
            0.254,
            0.281,
            0.308,
            0.332,
            0.352,
            0.37,
            0.383,
            0.39,
            0.394,
            0.395,
            0.392,
            0.385,
            0.377,
            0.367,
            0.354,
            0.341,
            0.327,
            0.312,
            0.296,
            0.28,
            0.263,
            0.247,
            0.229,
            0.214,
            0.198,
            0.185,
            0.175,
            0.169,
            0.164,
            0.16,
            0.156,
            0.154,
            0.152,
            0.151,
            0.149,
            0.148,
            0.148,
            0.148,
            0.149,
            0.151,
            0.154,
            0.158,
            0.162,
            0.165,
            0.168,
            0.17,
            0.171,
            0.17,
            0.168,
            0.166,
            0.164,
            0.164,
            0.165,
            0.168,
            0.172,
            0.177,
            0.181,
            0.185,
            0.189,
            0.192,
            0.194,
            0.197,
            0.2,
            0.204,
            0.21,
            0.218,
            0.225,
            0.233,
            0.243,
            0.254,
            0.264,
            0.274,
        ]
        y = materia.Qty(value=tcs04, unit=materia.unitless)

        super().__init__(x=x, y=y)


class CIE1995TestColorSample05(ReflectanceSpectrum):
    def __init__(self):
        # data taken from https://web.archive.org/web/20090211042805/http://photometry.kriss.re.kr/wiki/img_auth.php/4/47/CIE_TCS.csv
        x = materia.Qty(value=np.linspace(360, 830, 95), unit=materia.nanometer)

        tcs05 = [
            0.143,
            0.187,
            0.233,
            0.269,
            0.295,
            0.306,
            0.31,
            0.312,
            0.313,
            0.315,
            0.319,
            0.322,
            0.326,
            0.33,
            0.334,
            0.339,
            0.346,
            0.352,
            0.36,
            0.369,
            0.381,
            0.394,
            0.403,
            0.41,
            0.415,
            0.418,
            0.419,
            0.417,
            0.413,
            0.409,
            0.403,
            0.396,
            0.389,
            0.381,
            0.372,
            0.363,
            0.353,
            0.342,
            0.331,
            0.32,
            0.308,
            0.296,
            0.284,
            0.271,
            0.26,
            0.247,
            0.232,
            0.22,
            0.21,
            0.2,
            0.194,
            0.189,
            0.185,
            0.183,
            0.18,
            0.177,
            0.176,
            0.175,
            0.175,
            0.175,
            0.175,
            0.177,
            0.18,
            0.183,
            0.186,
            0.189,
            0.192,
            0.195,
            0.199,
            0.2,
            0.199,
            0.198,
            0.196,
            0.195,
            0.195,
            0.196,
            0.197,
            0.2,
            0.203,
            0.205,
            0.208,
            0.212,
            0.215,
            0.217,
            0.219,
            0.222,
            0.226,
            0.231,
            0.237,
            0.243,
            0.249,
            0.257,
            0.265,
            0.273,
            0.28,
        ]
        y = materia.Qty(value=tcs05, unit=materia.unitless)

        super().__init__(x=x, y=y)


class CIE1995TestColorSample06(ReflectanceSpectrum):
    def __init__(self):
        # data taken from https://web.archive.org/web/20090211042805/http://photometry.kriss.re.kr/wiki/img_auth.php/4/47/CIE_TCS.csv
        x = materia.Qty(value=np.linspace(360, 830, 95), unit=materia.nanometer)

        tcs06 = [
            0.079,
            0.081,
            0.089,
            0.113,
            0.151,
            0.203,
            0.265,
            0.339,
            0.41,
            0.464,
            0.492,
            0.508,
            0.517,
            0.524,
            0.531,
            0.538,
            0.544,
            0.551,
            0.556,
            0.556,
            0.554,
            0.549,
            0.541,
            0.531,
            0.519,
            0.504,
            0.488,
            0.469,
            0.45,
            0.431,
            0.414,
            0.395,
            0.377,
            0.358,
            0.341,
            0.325,
            0.309,
            0.293,
            0.279,
            0.265,
            0.253,
            0.241,
            0.234,
            0.227,
            0.225,
            0.222,
            0.221,
            0.22,
            0.22,
            0.22,
            0.22,
            0.22,
            0.223,
            0.227,
            0.233,
            0.239,
            0.244,
            0.251,
            0.258,
            0.263,
            0.268,
            0.273,
            0.278,
            0.281,
            0.283,
            0.286,
            0.291,
            0.296,
            0.302,
            0.313,
            0.325,
            0.338,
            0.351,
            0.364,
            0.376,
            0.389,
            0.401,
            0.413,
            0.425,
            0.436,
            0.447,
            0.458,
            0.469,
            0.477,
            0.485,
            0.493,
            0.5,
            0.506,
            0.512,
            0.517,
            0.521,
            0.525,
            0.529,
            0.532,
            0.535,
        ]
        y = materia.Qty(value=tcs06, unit=materia.unitless)

        super().__init__(x=x, y=y)


class CIE1995TestColorSample07(ReflectanceSpectrum):
    def __init__(self):
        # data taken from https://web.archive.org/web/20090211042805/http://photometry.kriss.re.kr/wiki/img_auth.php/4/47/CIE_TCS.csv
        x = materia.Qty(value=np.linspace(360, 830, 95), unit=materia.nanometer)

        tcs07 = [
            0.15,
            0.177,
            0.218,
            0.293,
            0.378,
            0.459,
            0.524,
            0.546,
            0.551,
            0.555,
            0.559,
            0.56,
            0.561,
            0.558,
            0.556,
            0.551,
            0.544,
            0.535,
            0.522,
            0.506,
            0.488,
            0.469,
            0.448,
            0.429,
            0.408,
            0.385,
            0.363,
            0.341,
            0.324,
            0.311,
            0.301,
            0.291,
            0.283,
            0.273,
            0.265,
            0.26,
            0.257,
            0.257,
            0.259,
            0.26,
            0.26,
            0.258,
            0.256,
            0.254,
            0.254,
            0.259,
            0.27,
            0.284,
            0.302,
            0.324,
            0.344,
            0.362,
            0.377,
            0.389,
            0.4,
            0.41,
            0.42,
            0.429,
            0.438,
            0.445,
            0.452,
            0.457,
            0.462,
            0.466,
            0.468,
            0.47,
            0.473,
            0.477,
            0.483,
            0.489,
            0.496,
            0.503,
            0.511,
            0.518,
            0.525,
            0.532,
            0.539,
            0.546,
            0.553,
            0.559,
            0.565,
            0.57,
            0.575,
            0.578,
            0.581,
            0.583,
            0.585,
            0.587,
            0.588,
            0.589,
            0.59,
            0.59,
            0.59,
            0.591,
            0.592,
        ]
        y = materia.Qty(value=tcs07, unit=materia.unitless)

        super().__init__(x=x, y=y)


class CIE1995TestColorSample08(ReflectanceSpectrum):
    def __init__(self):
        # data taken from https://web.archive.org/web/20090211042805/http://photometry.kriss.re.kr/wiki/img_auth.php/4/47/CIE_TCS.csv
        x = materia.Qty(value=np.linspace(360, 830, 95), unit=materia.nanometer)

        tcs08 = [
            0.075,
            0.078,
            0.084,
            0.09,
            0.104,
            0.129,
            0.17,
            0.24,
            0.319,
            0.416,
            0.462,
            0.482,
            0.49,
            0.488,
            0.482,
            0.473,
            0.462,
            0.45,
            0.439,
            0.426,
            0.413,
            0.397,
            0.382,
            0.366,
            0.352,
            0.337,
            0.325,
            0.31,
            0.299,
            0.289,
            0.283,
            0.276,
            0.27,
            0.262,
            0.256,
            0.251,
            0.25,
            0.251,
            0.254,
            0.258,
            0.264,
            0.269,
            0.272,
            0.274,
            0.278,
            0.284,
            0.295,
            0.316,
            0.348,
            0.384,
            0.434,
            0.482,
            0.528,
            0.568,
            0.604,
            0.629,
            0.648,
            0.663,
            0.676,
            0.685,
            0.693,
            0.7,
            0.705,
            0.709,
            0.712,
            0.715,
            0.717,
            0.719,
            0.721,
            0.72,
            0.719,
            0.722,
            0.725,
            0.727,
            0.729,
            0.73,
            0.73,
            0.73,
            0.73,
            0.73,
            0.73,
            0.73,
            0.73,
            0.73,
            0.73,
            0.73,
            0.731,
            0.731,
            0.731,
            0.731,
            0.731,
            0.731,
            0.731,
            0.731,
            0.731,
        ]
        y = materia.Qty(value=tcs08, unit=materia.unitless)

        super().__init__(x=x, y=y)
