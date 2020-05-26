#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
# -----------------------------------------------------------------------------
import logging
import os
import os.path

###############################################################################
# Cool logo (or maybe cool logo, ascii one anyway)
###############################################################################
__logo__ = r"""
                            _              _
                           | |            | |
 _ __ ___ _ __   ___ ______| |_ ___   ___ | |___
| '__/ _ \ '_ \ / _ \______| __/ _ \ / _ \| / __|
| | |  __/ |_) | (_) |     | || (_) | (_) | \__ \
|_|  \___| .__/ \___/       \__\___/ \___/|_|___/
         | |
         |_|
"""


###############################################################################
# Retrive the correct complet path
# This function return a folder or filename with a standard way of writing.
#
# @param folder_or_file_name the folder or file name
# @return the folder or filename normalized.
###############################################################################
def set_correct_path(folder_or_file_name):
    return os.path.abspath(folder_or_file_name)


###############################################################################
# Test a folder
# Test if the folder exist.
#
# @exception RuntimeError if the name is a file or not a folder
#
# @param folder the folder name
# @return the folder normalized.
###############################################################################
def check_folder(folder):
    if os.path.isfile(folder):
        logging.error('%s can not be a folder (it is a file)', folder)
        raise RuntimeError('%s can not be a folder (it is a file)' % folder)

    if not os.path.isdir(folder):
        logging.error('%s is not a folder', folder)
        raise RuntimeError('%s is not a folder' % folder)

    return set_correct_path(folder)


###############################################################################
# Test a folder
# test if the folder exist and create it if possible and necessary.
#
# @exception RuntimeError if the name is a file
#
# @param folder the folder name
# @return the folder normalized.
###############################################################################
def check_create_folder(folder):
    if os.path.isfile(folder):
        logging.error('%s can not be a folder (it is a file)', folder)
        raise RuntimeError('%s can not be a folder (it is a file)' % folder)

    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)

    return set_correct_path(folder)

###############################################################################
# test if this is a file and correct the path
#
# @exception RuntimeError if the name is not a file or if the extension
#                         is not correct
#
# @param filename the file name
# @param filename_ext the file name extension like ".ext" or ".md"
# @return the filename normalized.
###############################################################################
def check_is_file_and_correct_path(filename, filename_ext=None):
    filename = set_correct_path(filename)

    if not os.path.isfile(filename):
        logging.error('"%s" is not a file', (filename))
        raise Exception('"%s" is not a file' % (filename))

    current_ext = os.path.splitext(filename)[1]
    if (filename_ext is not None) and (current_ext != filename_ext):

        raise Exception('The extension of the file %s '
                        'is %s and not %s as expected.' % (
                            filename, current_ext, filename_ext))

    return filename
