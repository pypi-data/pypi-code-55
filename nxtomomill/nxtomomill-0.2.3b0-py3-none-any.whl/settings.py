# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2020 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

"""
module to convert from (bliss) .h5 to (nexus tomo compliant) .nx
"""

__authors__ = ["H. Payno", ]
__license__ = "MIT"
__date__ = "13/05/2020"



### HDF5 settings

H5_VALID_CAMERA_NAMES = ('pcolinux', 'basler1',)

H5_ROT_ANGLE_KEYS = ('hrsrot', 'srot')

H5_X_TRANS_KEYS = ("sx",)

H5_Y_TRANS_KEYS = ("sy",)

H5_Z_TRANS_KEYS = ("sz",)

H5_ACQ_EXPO_TIME_KEYS = ('acq_expo_time',)


### EDF settings

EDF_MOTOR_POS = 'motor_pos'

EDF_MOTOR_MNE = 'motor_mne'

EDF_ROT_ANGLE = "srot"

EDF_X_TRANS = "sx"

EDF_Y_TRANS = "sy"

EDF_Z_TRANS = "sz"

#EDF_TO_IGNORE = ['HST', '_slice_']
EDF_TO_IGNORE = ('_slice_',)

EDF_DARK_NAMES = ('darkend', 'dark')

EDF_REFS_NAMES = ('ref', 'refHST')
