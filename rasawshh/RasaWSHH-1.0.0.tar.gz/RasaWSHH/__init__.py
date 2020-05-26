import logging

from RasaWSHH import version

# define the version before the other imports since these need it
__version__ = version.__version__

from RasaWSHH.run import run
from RasaWSHH.train import train
from RasaWSHH.test import test

logging.getLogger(__name__).addHandler(logging.NullHandler())
