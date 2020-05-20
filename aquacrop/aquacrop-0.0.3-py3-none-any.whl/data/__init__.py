import os
import numpy as np

files = os.listdir('.')

def get_data(fname):
    return np.genffromtxt(fname)