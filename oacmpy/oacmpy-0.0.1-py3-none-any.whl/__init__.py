import os
from pathlib import Path

from . import State, oem2czml
from .ccsds import Aem, Apm, Cdm, Oem, Omm, Opm
from .czml import *

CCSDS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / "data"

__author__ = "Joris T. Olympio"
__version__ = "0.1"
__license__ = "MIT"
__description__ = "Parse CCSDS Data Message, including OEM, AEM and CDM, and convert them to a CZML scenario file."

__all__ = ["State", "oem2czml"]
__all__ += [name for name in dir(czml) if not name.startswith("_")]
