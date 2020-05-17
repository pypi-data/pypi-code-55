from .pygad import * # Relative import.
from .nn import nn # When PyGAD is used, it is enough to import pygad and pygad.nn will also be imported. No need for "import pygad.nn" when "import pygad" exists.
from .gann import gann #  When PyGAD is used, it is enough to import pygad and pygad.gann will also be imported. No need for "import pygad.gann" when "import pygad" exists.

__version__ = "2.2.0"
nn.__version__ = "1.0.0"
gann.__version__ = "1.0.0"