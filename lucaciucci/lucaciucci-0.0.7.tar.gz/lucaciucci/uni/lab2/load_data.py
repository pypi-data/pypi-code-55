# ================================================================
# lc.py:  alcune funzioni per lab2
# Date:     XX/XX/2020
# Author:   Luca Ciucci
# Contact:  develop@lucaciucci99.com
# ================================================================

# ================================================================
#                            IMPORTS
# ================================================================

import numpy as np

# ////////////////////////////////////////////////////////////////
# ottieni il nome completo del file
def _path_to(fileName) :
    """
    ottieni il nome completo del file (inserisce .txt se necessario)
    """
    if len(fileName) < 5 :
        return fileName + ".txt"
    if (fileName[-4] == ".") :
        return fileName
    else:
        return fileName + ".txt"

# ////////////////////////////////////////////////////////////////
def loadtxt(filename, comments = '#', **kwargs) :
    """
    Carica un file di dati in formato txt
    """
    return np.loadtxt(_path_to(filename), unpack = True, **kwargs)