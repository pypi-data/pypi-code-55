# -*- coding: utf-8 -*-
"""
Created on Tue May  5 12:51:18 2020

@author: f-ove

all functions by Flo

TO DO: put them into organised .py scripts
"""

import pandas as pd
import os
from os.path import join, isfile
import matplotlib.pyplot as plt


def pickle_rawdata(force_rerun=False):
    """
    Write the following csv Sheets to Pickle Files:
    - POLLUTANTRELEASEANDTRANSFERREPORT
    - FACILITYREPORT
    - POLLUTANTRELEASE

    The script checks if the pickle files exist already.
    If it does, it skips the operation.

    If you set force_rerun to True, it will redo all operations.
    """

    # POLLUTANTRELEASEANDTRANSFERREPORT
    if ((os.path.isfile(os.path.join(os.getcwd(), 'rawdata\\pratr.pkl')) is False) or force_rerun):
        pratr = pd.read_csv(os.path.join(os.getcwd(), 'rawdata\\dbo.PUBLISH_POLLUTANTRELEASEANDTRANSFERREPORT.csv'))
        pratr.to_pickle(os.path.join(os.getcwd(), 'rawdata\\pratr.pkl'))

    # FACILITYREPORT
    if ((os.path.isfile(os.path.join(os.getcwd(), 'rawdata\\fr.pkl')) is False) or force_rerun):
        fr = pd.read_csv(os.path.join(os.getcwd(), 'rawdata\\dbo.PUBLISH_FACILITYREPORT.csv'), encoding='latin-1', low_memory=False)
        fr.to_pickle(os.path.join(os.getcwd(), 'rawdata\\fr.pkl'))

    # POLLUTANTRELEASE
    if ((os.path.isfile(os.path.join(os.getcwd(), 'rawdata\\pr.pkl')) is False) or force_rerun):
        pr = pd.read_csv(os.path.join(os.getcwd(), 'rawdata\\dbo.PUBLISH_POLLUTANTRELEASE.csv'), low_memory=False)
        pr.to_pickle(os.path.join(os.getcwd(), 'rawdata\\pr.pkl'))
    return None


def merge_frompickle(force_rerun=False):
    """
    This function will merge the desired data to one dataframe and stores it as pickle

    The script checks if the pickle files exist already.
    If it does, it skips the operation.

    If you set force_rerun to True, it will redo all operations.
    """
    if (os.path.isfile(os.path.join(os.getcwd(), 'rawdata\\db.pkl')) is False) or force_rerun:
        try:
            fr = pd.read_pickle(os.path.join(os.getcwd(), 'rawdata\\fr.pkl'))
            pr = pd.read_pickle(os.path.join(os.getcwd(), 'rawdata\\pr.pkl'))
            pratr = pd.read_pickle(os.path.join(os.getcwd(), 'rawdata\\pratr.pkl'))
        except FileNotFoundError:
            print('Error. Run function pickle_rawdata')

        try:
            # speed difference for variing merge-order?? Table length differs, merge smart enough to add multiple one row to multiple?
            # problematic to merge by multiple coloum names?
            db01 = pd.merge(fr, pratr, on=['PollutantReleaseAndTransferReportID', 'CountryName', 'CountryCode'])
            db02 = pd.merge(db01, pr, on=['FacilityReportID', 'ConfidentialIndicator', 'ConfidentialityReasonCode', 'ConfidentialityReasonName'])
            db02.to_pickle(os.path.join(os.getcwd(), 'rawdata\\db.pkl'))
        except NameError:
            print('Error. Merging not possible')
    return None












