# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 22:54:57 2019

@author: jazzn
"""

import nglview as ng
from pubchempy import download

def molecul(name,typ='SDF'):
    file_name=get_mol_file(name,typ)
    #download(typ,file_name,name,'name',overwrite=True)
    a = ng.show_file(file_name)
    a.representations = [{"type": "ball+stick", "params": {"sele": "hetero"}}]
    return a

def get_mol_file(name,typ='SDF'):
    """
    name (str): name of molecule
    typ (str):  >SDF 3d file
                >PNG 2d file 
    """
    file_name=name+'.'+typ.lower()
    try:
        download(typ,file_name,name,'name',overwrite=True)
        print(f"file {file_name} downloaded")
        return file_name
    except:
        print("failed")