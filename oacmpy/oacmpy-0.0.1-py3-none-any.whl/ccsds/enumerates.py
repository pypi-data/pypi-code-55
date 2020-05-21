"""List of allowable frame for ADM"""
from enum import Enum


class FileFormat(Enum):
    """
    KVN     Keyword Value Notation
    XML     eXtensible Markup Language
    """

    KVN = "KVN"
    XML = "XML"


class ReferenceFrame(Enum):
    """
    List of reference frame for ephemerides

    EME2000     Earth Mean Equator and Equinox of J2000
    GTOD        Greenwich True of Date ICRF International Celestial Reference Frame
    ITRF2000    International Terrestrial Reference Frame 2000
    ITRF-93     International Terrestrial Reference Frame 1993
    ITRF-97     International Terrestrial Reference Frame 1997
    J2000       Earth Mean Equator and Equinox of J2000
    LVLH        Local Vertical Local Horizontal
    RTN         QSW Radial, Transverse, Normal Orbital Frame
    QSW         Radial, Transverse, Normal Orbital Frame
    TOD         True of Date
    TNW         Tangential, Normal, Omega (W) Orbital Frame
    NTW         Tangential, Normal, Omega (W) Orbital Frame
    RSW         Relative Orbit Frame describing the relative motion of two satellites (Clohessy-Wiltshire Equations)
    TEME        True Equator Mean Equinox
    SC_BODY_1
    """

    EME2000 = "EME2000"
    GTOD = "GTOD"
    ICRF = "ICRF"
    ITRF2000 = "ITRF2000"
    ITRF93 = "ITRF-93"
    ITRF97 = "ITRF-97"
    J2000 = "J2000"
    LVLH = "LVLH"
    RTN = "RTN"
    QSW = "QSW"
    TOD = "TOD"
    TNW = "TNW"
    NTW = "NTW"
    RSW = "RSW"
    TDR = "TDR"
    GRC = "GRC"
    TEME = "TEME"


class AttitudeFrame(Enum):
    ICRF = "ICRF"
    ITRF93 = "ITRF - 93"
    ITRF97 = "ITRF - 97"
    ITRF2000 = "ITRF2000"
    ITRFxxxx = "ITRFxxxx"
    TOD = "TOD"
    EME2000 = "EME2000"
    J2000 = "J2000"  # added, it often confuse with EME2000
    LVLH = "LVLH"
    NTW = "NTW"
    SC_BODY_1 = "SC_BODY_1"
    INSTRUMENT_A = "INSTRUMENT_A"
    STARTRACKER_1 = "STARTRACKER_1"


class LocalSpacecraftFrame(Enum):
    """Reference frame specifying frame B of the transformation"""

    ACTUATOR_0 = "SC_BODY_1"
    CSS_00 = "CSS_00"
    DSS_0 = "DSS_0"
    GYRO = "GYRO"
    INSTRUMENT_0 = "INSTRUMENT_0"
    SC_BODY_0 = "SC_BODY_0"
    SC_BODY_A = "SC_BODY_A"
    SENSOR_0 = "SENSOR_0"
    STARTRACKER_1 = "STARTRACKER_1"
    TAM_0 = "TAM_0"


class TimeSystem(Enum):
    """Time system.
    GMST
      Greenwich Mean Sidereal Time
    GPS
      Global Positioning System
    MET
      Mission Elapsed Time (note)
    MRT
      Mission Relative Time (note)
    SCLK
      Spacecraft Clock (receiver)
    TAI
      International Atomic Time
    TCB
      Barycentric Coordinate Time
    TDB
      Barycentric Dynamical Time
    TCG
      Geocentric Coordinate Time
    TT
      Terrestrial Time
    UT1
      Universal Time
    UTC
      Coordinated Universal Time
    """

    GMST = "GMST"  # Greenwich Mean Sidereal Time
    GPS = "GPS"
    MET = "MET"
    MRT = "MRT"
    SCLK = "SCLK"
    TAI = "TAI"
    TCB = "TCB"
    TDB = "TDB"
    TCG = "TCG"
    TT = "TT"  # Terrestrial Time
    UT1 = "UT1"
    UTC = "UTC"  # Coordinated Universal Tim


class InterpolationMethod(Enum):
    LINEAR = "LINEAR"
    HERMITE = "HERMITE"
    LAGRANGE = "LAGRANGE"


class AttitudeType(Enum):
    QUATERNION = "QUATERNION"
    QUATERNION_DERIVATIVE = "QUATERNION/DERIVATIVE"
    QUATERNION_RATE = "QUATERNION/RATE"
    EULER_ANGLE = "EULER_ANGLE"
    EULER_ANGLE_RATE = "EULER_ANGLE/RATE"
    SPIN = "SPIN"
    SPIN_NUTATION = "SPIN/NUTATION"


class EulerDir(Enum):
    A2B = "A2B"
    B2A = "B2A"


class RateFrame(Enum):
    EULER_FRAME_A = "EULER_FRAME_A"
    EULER_FRAME_B = "EULER_FRAME_B"


class QuaternionConvention(Enum):
    FIRST = "FIRST"
    LAST = "LAST"


class ConjunctionObject(Enum):
    OBJECT1 = "OBJECT1"
    OBJECT2 = "OBJECT2"
