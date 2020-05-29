#!/usr/bin/env python3

# Copyright 2020 Lam Nguyen

import sys
import json
import numpy as np

def get_stats(var, var_name="unknown", depth=0):

    stats = {}
    stats['var_name'] = var_name
    stats['size'] = str(sys.getsizeof(var)/1024) + " KB"
    stats['type'] = str(type(var))

    if type(var) is list:
        stats['len'] = str(len(var))
        stats['1st item'] = get_stats(var[0], var_name=var_name+'[0]', depth=depth+1)

    if type(var) is dict:
        stats['key_count'] = str(len(var.keys()))
        stats['1st item'] = get_stats(var[list(var.keys())[0]], var_name=var_name+'[' + list(var.keys())[0] +']', depth=depth+1)

    if type(var) is np.ndarray:
        stats['shape'] = str(var.shape)
        stats['dtype'] = str(var.dtype)

    if type(var) is np.lib.npyio.NpzFile:
        stats['files'] = str(var.files)
        for f in var.files:
            stats[var_name+'['+f+']'] = get_stats(var[f], var_name=var_name+'['+f+']', depth=depth+1)

    return stats


def print_stats(var, var_name="unknown"):
    
    stats = get_stats(var, var_name)
    print(json.dumps(stats, indent=4))

    return
