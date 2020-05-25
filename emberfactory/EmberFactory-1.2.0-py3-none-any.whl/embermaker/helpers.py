import numpy as np
import logging
import defusedxml
from defusedxml.common import EntitiesForbidden
import zipfile
from xlrd import open_workbook
defusedxml.defuse_stdlib()

"""
This module contains two types of "helper functions" :
- nicelevels: devides a range of value into a set of well-chosen levels for graphics (e.g. axis)
- logging functions mostly aimed at facilitating the reporting of errors into the web interface
- opening xml files safely using defusexml and also checking the uncompressed size.

05/2020: The logging part is adapted from an earlier version of the code, and may not be fully appropriate
and/or well structured. It works and remains needed here, but may change substantially or be removed in the future.
"""

def nicelevels(vmin, vmax, nalevels=5, enclose=True):
    """
    Finds a nice value for the step to devide a range of values in nice levels, given constraints
    :param vmin: minimum value to be represented
    :param vmax: max value to be represented
    :param nalevels: approximative numbers of desired levels (divisions) between min and max
    :param enclose: whether the levels should enclose (default) the range or be within the range
    :return: levels = selected levels so that intervals are [ 5., 2.5, 2.0, 1. ]  *  1.E exponent
             labstp = formatting string for the axis labels

    Copyright (C) 2020  philippe.marbaix@uclouvain.be
    """

    #   Allowed values of the step between levels are (dignificand part, decreasing order):
    aticks = [5., 2.5, 2., 1.]
    #   Corresponding number of 'minor ticks' :
    # pticks = [ 4 , 4  , 3  , 4  ]
    #
    nalevels = max(3, nalevels)

    #   First approximation of the step :
    aStep = (vmax - vmin) / (float(nalevels - 1) * 0.8)
    if (np.abs(aStep) <= 1.E-30):
        aStep = 1.E-30

    #   exponent:
    eStep = np.floor(np.log10(aStep) + 99.) - 99.
    #   significand part of the step (mantissa, see https://en.wikipedia.org/wiki/Significand):
    maStep = aStep / 10 ** eStep
    #   Select the step:
    mStep = [tick for tick in aticks if tick <= maStep][0]
    stp = (10 ** eStep) * mStep
    #
    #   Formatting string for labels
    #  Potential strings:
    lab = ["{:.6f}", "{:.5f}", "{:.4}", "{:.3f}", "{:.2f}", "{:.1f}", "{:.0f}"]
    ilab = int(round(eStep))
    if ((ilab <= 5) and (ilab > 0)):
        labstp = "{:.0f}"
    elif ((ilab >= -5) and (ilab <= 0)):
        labstp = lab[ilab + 6 - (mStep == 2.5)]
    else:
        labstp = "{:.2e}"

    #   Generate levels
    newmin = np.floor(vmin / stp) * stp
    addone = (enclose == True or divmod((vmax - vmin), stp)[1] < 0.01)
    nlevels = np.ceil((vmax - newmin) / stp) + addone
    nlevels = max(2, nlevels)
    levels = np.arange(nlevels) * stp + newmin

    return levels, labstp


def addlogmes(mes):
    """
    This is perhaps temporary: DIY logging for web feedback
    Studying the logging class could perhaps help designing something better & more standard?
    This was designed for the previous version, which worked with mod_python.
    """
    global logmes, webapp
    if webapp:
        logmes["full"].append(rembrackets(mes))
    else:
        logging.debug(mes)

def addlogwarn(mes, critical=False):
    """
    Warning message
    """
    global logmes
    logmes["full"].append(rembrackets(mes))
    if critical:
        logging.critical(mes)
        logmes["critical"].append(rembrackets(mes))
    else:
        logging.warning(mes)
        logmes["warning"].append(rembrackets(mes))

def addlogfail(mes):
    """
    Log message as fatal error and return it to raise exception
    """
    global logmes
    mes = "FATAL ERROR: " + mes
    logging.critical(mes)
    logmes["full"].append(rembrackets(mes))
    logmes["critical"].append(rembrackets(mes))
    return mes

def startlog(web=True):
    global logmes, webapp
    logmes = {"full": [], "warning": [], "critical": []}
    webapp = web

def getlog(level):
    global logmes
    try:
        mes = logmes[level]
    except:
        mes = ['The logging facility failed or did not start!']
    return mes

def rembrackets(instr):
    # This was mostly useful when the code run with mod_python,
    # as Flask probably does it by default. Consider removing.
    return str(instr).replace('<', '&lt;').replace('>', '&gt;')

def secure_open_workbook(file, maxsize=2E6):
    # Attempt at protecting against a real or poential (?) zip bomb:
    # (is it really needed? not sure - see here: https://bugs.python.org/issue36260
    with zipfile.ZipFile(file) as zf:
        if sum(zi.file_size for zi in zf.infolist()) > maxsize:
            raise Exception('Excel file appears too large for reading; please contact app managers')

    # Protect against XML bombs
    # https://pypi.org/project/defusedxml/
    try:
        return open_workbook(file)
    except EntitiesForbidden:
        raise ValueError('Excel file appears invalid')