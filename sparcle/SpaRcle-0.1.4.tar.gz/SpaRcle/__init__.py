print("[Python] Importing SpaRcle library...")

import os
import sys

path_fo_init = __file__

lib_dir = path_fo_init.rpartition('\\')[0]
print("[Python] Library directory is "+lib_dir)
sys.path.insert(0, lib_dir)

import PySpaRcle


#def LoadLibrary():
#    print("Loading SpaRcle library...")
input("Press any key for exit...")
    