#!/usr/bin/env python3

# Copyright (C) Martin Singer <martin.singer@web.de>
#
# This file is part of PDF Chain.
#
# PDF Chain is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PDF Chain is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PDF Chain.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Martin Singer

'''
@brief Project File Path Module.
@details
    This module manages the project file paths
    and contains defined filenames.
'''

from os.path import abspath, dirname, exists, join, sep, split
import xdg.BaseDirectory


def __proof_path_exists(path):
    """
    """
    if exists(path):
        return path
    raise Exception("The path '{}' was not found!".format(path))


def __get_base_dir():
    """
    @brief Finds and returns the data base directory path (`share`).
    @details
        This function searches the data directory belonging to the executed program.
        This works for installations where the data directory is called "share"
        and shares a common directory tree with the execution directory.
    @par Explaining the Algorithm
        This function determines the directory in which it is executed
        and scans the directory tree backwards in a loop step by step.
        At each step it checks if it contains the data directory "share".
        If "share" is found, it is assumed to contain the data directory
        and the path of the data directory is returned.
        If the loop has arrived at the root directory (`/`),
        no data directory was found and the loop is aborted
        and an exception is thrown.
        This simple algorithm should work for different installation paths.
    @code List Data Directories
        import xdg.BaseDirectory
        print(xdg.BaseDirectory.xdg_data_dirs)
    @par Known Installation Cases
        - Development
            - `~/Projects/*/pdfchain/src`
            - `~/Projects/*/pdfchain/share`
        - PIP User Installation
            - `~/.local/lib/python<version>/site-packages`
            - `~/.local/share`
        - Flatpak User Installation
            - `~/.local/share/flatpak/*/exports/bin
            - `~/.local/share/flatpak/*/exports/share`
        - Flatpak System Installation
            - `/var/lib/flatpak/*/exports/bin`
            - `/var/lib/flatpak/*/exports/share`
        - Local System Installation (`sudo make install`)
            - `/usr/local/bin`
            - `/usr/local/share`
        - System Installation (package manager)
            - `/usr/bin`
            - `/usr/share`
    """
    head_path = (split(abspath(dirname(__file__))))[0]
    while head_path != sep:
        base_path = join(head_path, "share")
        if exists(base_path):
            print("BasePath: '{}'".format(base_path))
            return base_path
        head_path = (split(head_path))[0]
    raise Exception("No base directory found!")


def __get_data_dir(base_dir_path, data_dir_name):
    """
    @brief Returns the requested data directory.
    """
    data_dir_path = abspath(join(base_dir_path, data_dir_name))
    if exists(data_dir_path):
        return data_dir_path
    raise Exception("No data directory '{}' in '{}' found!".format(
        data_dir_name, base_dir_path))


def get_locale_dir():
    """
    @brief Returns locale directory path.
    """
    return __LOCALE_DIR


def get_ui_file(filename):
    return __proof_path_exists(join(__UI_DIR, filename))


#def get_icon_file(filename):
#    return __proof_path_exists(join(__ICONS_DIR, filename))


#def get_pixmap_file(filename):
#    return __proof_path_exists(join(__PIXMAPS_DIR, filename))


def get_config_file():
    """
    @brief Returns the path of the users configuration file.
    """
    return __CONFIG_FILE


__BASE_DIR    = __get_base_dir()
__UI_DIR      = __get_data_dir(__BASE_DIR, join("pdfchain", "ui"))
# __LOCALE_DIR  = __get_data_dir(__BASE_DIR, "locale")
__ICONS_DIR   = __get_data_dir(__BASE_DIR, "icons")
__PIXMAPS_DIR = __get_data_dir(__BASE_DIR, "pixmaps")

__CONFIG_FILE = __proof_path_exists(join(xdg.BaseDirectory.xdg_config_home, "pdfchain.ini"))
