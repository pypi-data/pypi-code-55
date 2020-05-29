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
 @brief   File Chooser Dialog File Filter
 @details
    The file filters do not work very well in Glade UI definitions.
    So I implemented them in code.

 @note Inadequacies with the file filters using the UI definitions
     - Multiple file filters are not possible
     - File filter can not be named
     - File filter can not be shared
       (have to be extra defined file filter for every single dialog)
'''

import os # for `os.path.splitext()`
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# File Filter
class FileFilter_All(Gtk.FileFilter):
    """
    @brief File Filter: All files
    """

    def __init__(self):
        super().__init__()
        self.set_name("All Files")
        self.add_pattern("*")


class FileFilter_PDF(Gtk.FileFilter):
    """
    @brief File Filter: Portable Document Format file
    """

    def __init__(self):
        super().__init__()
        self.set_name("PDF Files")
        self.add_mime_type("application/pdf")
        self.add_pattern("*.pdf")


class FileFilter_Text(Gtk.FileFilter):
    """
    @brief File Filter: Text files
    """

    def __init__(self):
        super().__init__()
        self.set_name("Text Files")
        self.add_mime_type("text/plain")
        self.add_pattern("*.txt")


class FileFilter_FDF(Gtk.FileFilter):
    """
    @brief File Filter: Forms Data Format files
    @details
        - Pattern `*.fdf`:  Forms Data Format file
        - Pattern `*.xfdf`: XML Forms Data Format file
    @note
        PDFtk can create form data exclusively in FDF format.
    """

    def __init__(self):
        super().__init__()
        self.set_name("FDF Files")
        self.add_pattern("*.fdf")
        self.add_pattern("*.xfdf")


class FileFilter_Dump(Gtk.FileFilter):
    """
    @brief File Filter: Metadata Dump files
    """

    def __init__(self):
        super().__init__()
        self.set_name("Metadata Dump Files")
        self.add_pattern("*.dump")


# FileChooserDialogs
class FCDialog_SaveDoc(Gtk.FileChooserDialog):
    """
    @brief File Chooser Dialog: Save PDF Files
    """

    def __init__(self, transient):
        super().__init__("Save Document", transient, Gtk.FileChooserAction.SAVE,
                ("_Save", Gtk.ResponseType.OK, "_Cancel", Gtk.ResponseType.CANCEL))
        self.set_create_folders(True)
        self.set_current_name("Untitled.pdf")
        self.set_do_overwrite_confirmation(True)
        self.add_filter(FileFilter_PDF())
        self.add_filter(FileFilter_All())


class FCDialog_OpenDoc(Gtk.FileChooserDialog):
    """
    @brief File Chooser Dialog: Open PDF Files
    """

    def __init__(self, transient):
        super().__init__("Open Document", transient, Gtk.FileChooserAction.OPEN,
                ("_Open", Gtk.ResponseType.OK, "_Cancel", Gtk.ResponseType.CANCEL))
        self.add_filter(FileFilter_PDF())
        self.add_filter(FileFilter_All())


class FCDialog_OpenDocMulti(Gtk.FileChooserDialog):
    """
    @brief File Chooser Dialog: Open multiple PDF Files
    """

    def __init__(self, transient):
        super().__init__("Open Documents", transient, Gtk.FileChooserAction.OPEN,
                ("_Open", Gtk.ResponseType.OK, "_Cancel", Gtk.ResponseType.CANCEL))
        self.set_select_multiple(True)
        self.add_filter(FileFilter_PDF())
        self.add_filter(FileFilter_All())


class FCDialog_SaveFDF(Gtk.FileChooserDialog):
    """
    @brief File Chooser Dialog: Save Forms Data Format files
    @note
        PDFtk can create form data exclusively in FDF format.
        Therefore no file filter for the XFDF format is added
        to the save FDF file dialog.
    """

    def __init__(self, transient):
        super().__init__("Save FDF file", transient, Gtk.FileChooserAction.SAVE,
                ("_Save", Gtk.ResponseType.OK, "_Cancel", Gtk.ResponseType.CANCEL))
        self.set_create_folders(True)
        self.set_current_name("Untitled.fdf")
        self.set_do_overwrite_confirmation(True)
        self.add_filter(FileFilter_FDF())
        self.add_filter(FileFilter_Text())
        self.add_filter(FileFilter_All())


#class FCDialog_OpenFDF(Gtk.FileChooserDialog):
#    """
#    @brief File Chooser Dialog: Open FDF
#    """
#
#    def __init__(self, transient):
#        super().__init__("Open FDF file", transient, Gtk.FileChooserAction.OPEN,
#                ("_Open", Gtk.ResponseType.OK, "_Cancel", Gtk.ResponseType.CANCEL))
#        self.add_filter(FileFilter_FDF())
#        self.add_filter(FileFilter_XFDF())
#        self.add_filter(FileFilter_Text())
#        self.add_filter(FileFilter_All())


class FCDialog_SaveDump(Gtk.FileChooserDialog):
    """
    @brief File Chooser Dialog: Save Metadata files
    """

    def __init__(self, transient):
        super().__init__("Save Metadata Dump File", transient, Gtk.FileChooserAction.SAVE,
                ("_Save", Gtk.ResponseType.OK, "_Cancel", Gtk.ResponseType.CANCEL))
        self.set_create_folders(True)
        self.set_current_name("Untitled.dump")
        self.set_do_overwrite_confirmation(True)
        self.add_filter(FileFilter_Dump())
        self.add_filter(FileFilter_Text())
        self.add_filter(FileFilter_All())


#class FCDialog_OpenDump(Gtk.FileChooserDialog):
#    """
#    @brief File Chooser Dialog: Open Metadata files
#    """
#
#    def __init__(self, transient):
#        super().__init__("Open Metadata Dump File", transient, Gtk.FileChooserAction.OPEN,
#                ("_Open", Gtk.ResponseType.OK, "_Cancel", Gtk.ResponseType.CANCEL))
#        self.add_filter(FileFilter_Dump())
#        self.add_filter(FileFilter_Text())
#        self.add_filter(FileFilter_All())


class FCDialog_OpenAllMulti(Gtk.FileChooserDialog):
    """
    @brief File Chooser Dialog: Open multiple (various) files
    """

    def __init__(self, transient):
        super().__init__("Open Various Files", transient, Gtk.FileChooserAction.OPEN,
                ("_Open", Gtk.ResponseType.OK, "_Cancel", Gtk.ResponseType.CANCEL))
        self.set_select_multiple(True)
        self.add_filter(FileFilter_All())
        self.add_filter(FileFilter_PDF())
        self.add_filter(FileFilter_Text())


class FCDialog_SelectFolder(Gtk.FileChooserDialog):
    """
    @brief File Chooser Dialog: Select Folder
    """

    def __init__(self, transient):
        super().__init__("Select Folder", transient, Gtk.FileChooserAction.SELECT_FOLDER,
                ("_Select", Gtk.ResponseType.OK, "_Cancel", Gtk.ResponseType.CANCEL))
        self.set_do_overwrite_confirmation(True)
        self.set_create_folders(True)


# Functions
def fchooser_run(fcdialog):
    """
    @brief Helper function to run file choosers.
    @details
        This function has the standard procedure to run a file choosers.
        Works for file chooser dialogs and buttons.

    @param[in] fcdialog     The FileChooserDialog object to run()
    @return    str_filename String of chosen filename path
    @retval    ""           Empty string when "Cancel" was clicked
    """
    str_filename = ""
    response = fcdialog.run()
    fcdialog.hide()
    if response == Gtk.ResponseType.OK:
        str_filename = fcdialog.get_filename()
        if str_filename == None:
            cli.debug_message("WARNING: str_filename is None")
            str_filename = ""
    return str_filename
