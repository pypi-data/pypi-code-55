##################
## __init__.py  ##
##################


# Version of rktools package. It is updated by bumpversion (see https://pypi.org/project/bumpversion/)

# Ex. to update both version.txt and rktools/__init__.py files  
# $ bumpversion --current-version 0.0.2 patch version.txt rktools/__init__.py 

__version__ = "0.0.1"

# Import the python top file/modules for this package.
# When this package is loaded, we want the following modules to be
# automatically imported

import rktools.loggers
import rktools.monitors

