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

"""
@brief The Preferences Module.
@details
    The application manages the various windows and dialogs.
    It contains the preferences and about dialog
    as well as multiple application window instances.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import configparser

import pdfchain.paths as paths
from pdfchain.cmd_pdftk import PDFtk as pdftk


class Preferences():
    """
    @brief Preferences Class.
    @details
        Loads, stores and saves the user preference values
        as well as running the preferences GUI dialog.
    """

    _PATH_PREF_FILE = paths.get_config_file()
    _PATH_PDFTK_DEFAULT_CMD = "/usr/bin/pdftk"

    # Gtk widgets
    _dialog = None
    _entry_path_pdftk = None

    # ConfigParser object
    _pref = None


    def __init__(self):
        """
        @brief Constructing a Preferences Object.
        @details
            Loads the UI file and builds the dialog widgets.
            Creates the configuration parser object, loads and exports the preferences.
        """
        builder = Gtk.Builder()
        builder.add_from_file(paths.get_ui_file("dialogs.ui"))
        self._entry_path_pdftk = builder.get_object("entry_path_pdftk")
        self._entry_path_pdftk.set_placeholder_text(self._PATH_PDFTK_DEFAULT_CMD)
        self._dialog = builder.get_object("dialog_preferences")

        if self._pref is None:
            self._pref = configparser.ConfigParser()
            self._load_file()
            self._export_values()


    def _save_file(self):
        """
        @brief Get preference values from dialog widgets and save preferences into file.
        @details
            Sets the values in the configuration parser object
            and saves the preferences file, using this object.
        """
        path_pdftk = self._entry_path_pdftk.get_text()
        self._pref['PATH'] = {
            'pdftk': path_pdftk
            }

        with open(self._PATH_PREF_FILE, 'w') as preffile:
            self._pref.write(preffile)


    def _load_file(self):
        """
        @brief Load preference values from file or set default values.
        @details
            If the preferences file was found, the configuration parser object
            reads the preferences file.
            If the preferences file was not found, default variables are set.
            The defined variables are set to the dialog widgets.
        """
        self._pref.read(self._PATH_PREF_FILE)
        path_pdftk = self._pref['PATH']['pdftk']
        if not path_pdftk:
            path_pdftk = self._PATH_PDFTK_DEFAULT_CMD
            self._pref['PATH'] = {
                'pdftk': path_pdftk
                }
        self._entry_path_pdftk.set_text(path_pdftk)


    def _export_values(self):
        """
        @brief Export the preferences variables to the corresponding modules.
        @details
            External module methods and functions are called to transfer
            preferences, stored in the configuration parser object.
        """
        path_pdftk = self._pref['PATH']['pdftk']
        pdftk.set_command(path_pdftk)


    def run_dialog(self, parent):
        """
        @brief Run the preferences dialog.
        @details
            This method calls the methods which are required
            to load, show, save and export the preference values.

        @param[in] parent The parent window or None
        """
        self._load_file()
        self._dialog.set_transient_for(parent)
        self._dialog.run()
        self._save_file()
        self._export_values()
        self._dialog.hide()


    # def get_path(self, str_command):
    #         return self._pref['PATH'][str_command]
