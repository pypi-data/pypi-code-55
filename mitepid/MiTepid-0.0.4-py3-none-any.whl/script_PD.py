#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:01:11 2020

@author: vbokharaie
"""

if __name__ == '__main__':
    import pandas as pd
    from pathlib import Path

    dir_source = '/data/Cloud_Science/projects/MiTepid_sim/mitepid/'
    file_df_PD = 'Princess_Diamond.csv'
    filename = Path(dir_source, file_df_PD)
    df_PD = pd.read_csv(filename)