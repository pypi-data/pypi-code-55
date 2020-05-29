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
@brief The Application Window
@details
    This module contains classes handling the application window.

@see ./__init__.py
@see ./window.ui
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

#gi.require_version('Handy', '1')
#from gi.repository import Handy

# Local Libs
from pdfchain import paths as paths
from pdfchain import cli as cli
from pdfchain import filechooser as filechooser
from pdfchain import strings as strings
from pdfchain.cmd_pdftk import PDFtk as pdftk


class AppWindowHandler:
    '''
    @brief The Application Window Handler.
    @details
        This class contains signal handlers and dependent helper methods.
        The window GUI and its signals, is defined in an external XML file.
        This file is loaded and interpreted by a builder,
        and the signals defined in it are linked to the signal handlers
        of this class.
    '''

    # Constant column and row numbers
    _COLUMN_ID          = 0  # ComboBox ListStore column
    _COLUMN_TEXT        = 1
    _ROW_FILTER_ALL     = 0  # ComboBox ListStore entry
    _ROW_ROTATION_NORTH = 0

    _COLUMN_ACTIVE        = 0  # TreeView ListStore column (cat documents)
    _COLUMN_PATH          = 1
    #_COLUMN_filename      = 2  # not required
    #_COLUMN_tooltip       = 3  # not required
    _COLUMN_SELECTION     = 4
    _COLUMN_FILTER_TEXT   = 5
    _COLUMN_ROTATION_TEXT = 6
    _COLUMN_PASSWORD      = 7
    _COLUMN_PAGES         = 8
    _COLUMN_INDEX         = 9
    _COLUMN_FILTER_ID     = 10
    _COLUMN_ROTATION_ID   = 11

    _COLUMN_ADD = 0           # TreeView ListStore column (attach files)

    # Constant strings
    _STR_PATH = "Path"  # Used for the tool tip strings

    # Variables
    _source_document_pages = 0  # FIXME: pages are not counted, when document was selected!
    #_layer_document_pages = 0  # TODO: implement this variable!
                                #       Only if document has more than one page,
                                #       multiple background / stamp is able

    # Declaration of the title and sub title strings
    # (the strings will be copied from the UI file)
    _str_title_main   = ""
    _str_title_cat    = ""
    _str_title_burst  = ""
    _str_title_layer  = ""
    _str_title_attach = ""
    _str_title_tools  = ""

    _str_subtitle_main   = ""
    _str_subtitle_cat    = ""
    _str_subtitle_burst  = ""
    _str_subtitle_layer  = ""
    _str_subtitle_attach = ""
    _str_subtitle_tools  = ""


    def __init__(self, app):
        '''
        @brief The Initialization Method of the Application Window Class.
        @details
            This method creates a local builder object, used to load the UI file
            with the application window and connects the defined signals
            with the signal handlers defined in this class.
            It also connects the application window to the application object,
            which manages application window instances.
            Using the builder object also required widgets and list store objects
            are imported from the UI file.

        @param[in] app Reference to the application object
        '''
        # Create the Builder object, load the UI file and connect the SignalHandler
        builder = Gtk.Builder()
        builder.add_from_file(paths.get_ui_file("window.ui"))
        builder.connect_signals(self)

        # Add the ApplicationWindow to the Application
        app_window = builder.get_object("applicationwindow")
        app.add_window(app_window)
        #cli.debug_message("TEST: type: {} ".format(type(app_window))) #TEST: show the object type
        #cli.debug_message("TEST: app_window: {}".formtat(app_window)) #TEST: show the memory address of the object instances

        # Import required ListStores
        self._lstore_cat_document_id = builder.get_object("lstore_cat_document_id")
        self._lstore_cat_documents = builder.get_object("lstore_cat_documents")
        self._lstore_cat_filter = builder.get_object("lstore_cat_filter")
        self._lstore_cat_rotation = builder.get_object("lstore_cat_rotation")
        #self._lstore_burst_counter_base = builder.get_object("lstore_burst_counter_base") # not required
        self._lstore_attach_files = builder.get_object("lstore_attach_files")

        # Import required widgets of the Header Bar
        self._headerbar            = builder.get_object("headerbar")
        self._revealer_button_menu = builder.get_object("revealer_button_menu")
        self._revealer_button_help = builder.get_object("revealer_button_help")
        self._stack_hbar_right     = builder.get_object("stack_hbar_right")
        self._page_appmenu         = builder.get_object("page_appmenu")
        self._page_exec            = builder.get_object("page_exec")
        self._mbutton_rest         = builder.get_object("mbutton_rest")

        # Import required widgets of the InfoBar
        self._infobar = builder.get_object("infobar")
        self._label_infobar = builder.get_object("label_infobar")

        # Import required widgets of page Main
        self._stack_main       = builder.get_object("stack_main")
        self._page_main_menu   = builder.get_object("page_main_menu")
        self._page_main_cat    = builder.get_object("page_main_cat")
        self._page_main_srcdoc = builder.get_object("page_main_srcdoc")

        self._label_main_title_cat    = builder.get_object("label_main_title_cat")
        self._label_main_title_burst  = builder.get_object("label_main_title_burst")
        self._label_main_title_layer  = builder.get_object("label_main_title_layer")
        self._label_main_title_attach = builder.get_object("label_main_title_attach")
        self._label_main_title_tools  = builder.get_object("label_main_title_tools")
        self._label_main_subtitle_cat    = builder.get_object("label_main_subtitle_cat")
        self._label_main_subtitle_burst  = builder.get_object("label_main_subtitle_burst")
        self._label_main_subtitle_layer  = builder.get_object("label_main_subtitle_layer")
        self._label_main_subtitle_attach = builder.get_object("label_main_subtitle_attach")
        self._label_main_subtitle_tools  = builder.get_object("label_main_subtitle_tools")

        # Import required widgets of page Main - Menu
        #self._listbox_main_menu = builder.get_object("listbox_main_menu") # not required
        self._lbrow_main_cat    = builder.get_object("lbrow_main_cat")
        self._lbrow_main_burst  = builder.get_object("lbrow_main_burst")
        self._lbrow_main_layer  = builder.get_object("lbrow_main_layer")
        self._lbrow_main_attach = builder.get_object("lbrow_main_attach")
        self._lbrow_main_tools  = builder.get_object("lbrow_main_tools")

        #TEST
        #self._lbrow_main_burst.set_header(Gtk.HSeparator()) # FIXME: works only in Gtk.ListBoxUpdateHeaderFunc()

        # Import required widgets of page Main - Source File
        self._fcbutton_srcdoc       = builder.get_object("fcbutton_srcdoc")
        self._stack_srcdoc          = builder.get_object("stack_srcdoc")
        self._subpage_srcdoc_attach = builder.get_object("subpage_srcdoc_attach")
        self._subpage_srcdoc_layer  = builder.get_object("subpage_srcdoc_layer")
        self._subpage_srcdoc_burst  = builder.get_object("subpage_srcdoc_burst")
        self._subpage_srcdoc_tools  = builder.get_object("subpage_srcdoc_tools")

        # Import required widgets of page Concatenate
        self._ttbutton_cat_shuffle  = builder.get_object("ttbutton_cat_shuffle")
        self._cbox_cat_document_id  = builder.get_object("cbox_cat_document_id")
        self._entry_cat_document_id = builder.get_object("entry_cat_document_id")
        self._tview_cat_documents   = builder.get_object("tview_cat_documents")

        # Import required widgets of sub page Attachments
        #self._rtbutton_attach_to_doc = builder.get_object("rtbutton_attach_to_document") # not required
        self._rtbutton_attach_page   = builder.get_object("rtbutton_attach_to_page")
        self._toolitem_attach_page   = builder.get_object("toolitem_attach_page")
        self._sbutton_attach_page    = builder.get_object("sbutton_attach_page")
        self._tview_attach_files     = builder.get_object("tview_attach_files")

        # Import required widgets of sub page Layer (Watermark / Stamp)
        self._fcbutton_layer_document = builder.get_object("fcbutton_layer_document")
        self._rbutton_layer_watermark = builder.get_object("rbutton_layer_watermark")
        #self._rbutton_layer_stamp     = builder.get_object("rbutton_layer_stamp") # not required
        self._switch_layer_multiple   = builder.get_object("switch_layer_multiple")

        # Import required widgets of sub page Burst
        self._entry_burst_prefix   = builder.get_object("entry_burst_prefix")
        self._cbox_burst_base      = builder.get_object("cbox_burst_base")
        #self._entry_burst_base     = builder.get_object("entry_burst_base")
        self._rbutton_burst_auto   = builder.get_object("rbutton_burst_auto")
        self._rbutton_burst_manual = builder.get_object("rbutton_burst_manual")
        self._sbutton_burst_manual = builder.get_object("sbutton_burst_manual")
        self._entry_burst_suffix   = builder.get_object("entry_burst_suffix")
        self._switch_burst_ext     = builder.get_object("switch_burst_extension")
        self._label_burst_template = builder.get_object("label_burst_template_preview")

        # Import required widgets of sub page Tools
        self._rbutton_tools_unpack            = builder.get_object("rbutton_tools_unpack")

        self._rbutton_tools_dump_annots       = builder.get_object("rbutton_tools_dump_annots")
        self._rbutton_tools_ddata             = builder.get_object("rbutton_tools_ddata")
        self._cbutton_tools_ddata_utf8        = builder.get_object("cbutton_tools_ddata_utf8")
        self._rbutton_tools_ddfields          = builder.get_object("rbutton_tools_ddfields")
        self._cbutton_tools_ddfields_utf8     = builder.get_object("cbutton_tools_ddfields_utf8")
        self._box_tools_update_info           = builder.get_object("box_tools_update_info")
        self._rbutton_tools_update_info       = builder.get_object("rbutton_tools_update_info")
        self._cbutton_tools_update_info_utf8  = builder.get_object("cbutton_tools_update_info_utf8")
        self._fcbutton_tools_dump_file        = builder.get_object("fcbutton_tools_dump_file")

        self._rbutton_tools_generate_fdf      = builder.get_object("rbutton_tools_generate_fdf")
        self._box_tools_fform_file            = builder.get_object("box_tools_fform_file")
        self._rbutton_tools_fform             = builder.get_object("rbutton_tools_fform")
        self._box_tools_fform_options         = builder.get_object("box_tools_fform_options")
        self._cbutton_tools_fform_flatten     = builder.get_object("cbutton_tools_fform_flatten")
        self._cbutton_tools_fform_appearances = builder.get_object("cbutton_tools_fform_need_appearances")
        self._cbutton_tools_fform_drop_xfa    = builder.get_object("cbutton_tools_fform_drop_xfa")
        self._fcbutton_tools_fdf_file         = builder.get_object("fcbutton_tools_fdf_file")
        self._rbutton_tools_flatten           = builder.get_object("rbutton_tools_flatten")
        self._rbutton_tools_drop_xfa          = builder.get_object("rbutton_tools_drop_xfa")

        self._rbutton_tools_uncompress        = builder.get_object("rbutton_tools_uncompress")
        self._rbutton_tools_compress          = builder.get_object("rbutton_tools_compress")

        self._rbutton_tools_repair            = builder.get_object("rbutton_tools_repair")

        # Import required widgets of Restrictions popover menu
        self._entry_rest_passwd_user               = builder.get_object("entry_rest_passwd_user")
        self._entry_rest_passwd_owner              = builder.get_object("entry_rest_passwd_owner")
        self._rbutton_rest_enc_none                = builder.get_object("rbutton_rest_enc_none")
        self._rbutton_rest_enc_rc4_40bit           = builder.get_object("rbutton_rest_enc_rc4_40bit")
        self._rbutton_rest_enc_rc4_128bit          = builder.get_object("rbutton_rest_enc_rc4_128bit")
        self._frame_rest_perm                      = builder.get_object("frame_rest_perm")
        self._cbutton_rest_perm_printing           = builder.get_object("cbutton_rest_perm_printing")
        self._cbutton_rest_perm_degraded_printing  = builder.get_object("cbutton_rest_perm_degraded_printing")
        self._cbutton_rest_perm_copy_contents      = builder.get_object("cbutton_rest_perm_copy_contents")
        self._cbutton_rest_perm_screen_readers     = builder.get_object("cbutton_rest_perm_screenreaders")
        self._cbutton_rest_perm_modify_contents    = builder.get_object("cbutton_rest_perm_modify_contents")
        self._cbutton_rest_perm_assembly_contents  = builder.get_object("cbutton_rest_perm_assembly_contents")
        self._cbutton_rest_perm_modify_annotations = builder.get_object("cbutton_rest_perm_modify_annotations")
        self._cbutton_rest_perm_fill_in_annots     = builder.get_object("cbutton_rest_perm_fill_annotations")

        # Add File Filter to the File Chooser Dialogs
        # FIXME: set them transient/modal (but I don't know how)
        # Maybe I should create them here, using `Gtk.FileChooserButton.new_with_dialog()`
        self._fcbutton_srcdoc.add_filter(filechooser.FileFilter_PDF())
        self._fcbutton_srcdoc.add_filter(filechooser.FileFilter_All())

        self._fcbutton_layer_document.add_filter(filechooser.FileFilter_PDF())
        self._fcbutton_layer_document.add_filter(filechooser.FileFilter_All())

        self._fcbutton_tools_dump_file.add_filter(filechooser.FileFilter_Dump())
        self._fcbutton_tools_dump_file.add_filter(filechooser.FileFilter_Text())
        self._fcbutton_tools_dump_file.add_filter(filechooser.FileFilter_All())

        self._fcbutton_tools_fdf_file.add_filter(filechooser.FileFilter_FDF())
        self._fcbutton_tools_fdf_file.add_filter(filechooser.FileFilter_Text())
        self._fcbutton_tools_fdf_file.add_filter(filechooser.FileFilter_All())

        # Instance file chooser dialogs
        self._fcdialog_open_doc_multi = filechooser.FCDialog_OpenDocMulti(app_window)
        self._fcdialog_open_all_multi = filechooser.FCDialog_OpenAllMulti(app_window)
        self._fcdialog_select_folder  = filechooser.FCDialog_SelectFolder(app_window)
        self._fcdialog_save_doc       = filechooser.FCDialog_SaveDoc(app_window)
        self._fcdialog_save_dump_file = filechooser.FCDialog_SaveDump(app_window)
        self._fcdialog_save_fdf_file  = filechooser.FCDialog_SaveFDF(app_window)

        # Read the title and subtitle strings from the widgets
        self._str_title_main   = self._headerbar.get_title()
        self._str_title_cat    = self._label_main_title_cat.get_text()
        self._str_title_burst  = self._label_main_title_burst.get_text()
        self._str_title_layer  = self._label_main_title_layer.get_text()
        self._str_title_attach = self._label_main_title_attach.get_text()
        self._str_title_tools  = self._label_main_title_tools.get_text()

        self._str_subtitle_main   = self._headerbar.get_subtitle()
        self._str_subtitle_cat    = self._label_main_subtitle_cat.get_text()
        self._str_subtitle_burst  = self._label_main_subtitle_burst.get_text()
        self._str_subtitle_layer  = self._label_main_subtitle_layer.get_text()
        self._str_subtitle_attach = self._label_main_subtitle_attach.get_text()
        self._str_subtitle_tools  = self._label_main_subtitle_tools.get_text()

        # Create the Application Menu
        mbutton_appmenu = builder.get_object("mbutton_appmenu")

        builder_appmenu = Gtk.Builder()
        builder_appmenu.add_from_file(paths.get_ui_file("menus.ui"))
        appmenu = builder_appmenu.get_object("app-menu")
        popover_appmenu = Gtk.Popover.new_from_model(mbutton_appmenu, appmenu)
        mbutton_appmenu.set_popover(popover_appmenu)

        # Show the application window and all widgets
        app_window.present()


    # Handler for Window Signals
    def on_app_window_delete_event(self, *args):
        '''Signal handler to quit the application window.'''
        Gtk.main_quit(*args)


    # Handler for the InfoBar action widgets
    def on_infobar_response(self, infobar, response_id):
        '''
        @brief Handler for the InfoBar response signal
        @details
            Hides the InfoBar when the response ID is Gtk.ResponseType.CLOSE

        @param[in] infobar     The object which received the signal
        @param[in] response_id The response ID
        '''
        if response_id == Gtk.ResponseType.CLOSE:
            self._infobar.set_revealed(False)


    def _infobar_message(self, message_type, str_message):
        '''
        @brief Method to show user messages in the infobar.
        @details
            First, this method calls a function to print the message
            on the command line.  Then it sets the message type
            and the message text of the InfoBar and then displays it.

        @see cli.message()

        @param[in] message_type The `Gtk.MessageType`
        @param[in] str_message  The message string
        '''
        cli.message(message_type, str_message)
        self._infobar.set_message_type(message_type)
        self._label_infobar.set_text(str_message)
        self._infobar.set_revealed(True)


    # Handler for the HeaderBar action widgets
    def on_button_help_clicked(self, *args):
        '''
        @brief Handler for the Help button clicked signal
        @details
            Shows the help system for the shown section.

        @TODO: not implemented yet
        '''
        self._infobar_message(Gtk.MessageType.INFO, "The help system is not implemented yet!")


    def on_button_menu_clicked(self, *args):
        '''
        @brief Signal Handler for Button Menu clicked (back button)
        @details
            Sets the window widgets for the main menu.
        @see on_listbox_main_menu_row_activated()
        '''
        self._infobar.set_revealed(False)
        self._headerbar.set_title(self._str_title_main)
        self._headerbar.set_subtitle(self._str_subtitle_main)
        self._stack_main.set_visible_child(self._page_main_menu)
        self._revealer_button_menu.set_reveal_child(False)
        self._revealer_button_help.set_reveal_child(False)
        self._stack_hbar_right.set_visible_child(self._page_appmenu)


    # Handler for all pages (execute)
    def on_button_execute_clicked(self, button):
        """
        @brief Signal Handler for the execute button ("Save Document As").
        @details
            Starts the creation and execution of the command.

        @param[in] button The object which received the signal _(not used)_
        """
        str_section_command = self._create_pdftk_cmd()
        if str_section_command:
            str_command = " ".join([pdftk.get_command(), str_section_command])
            exit_code = cli.execute(str_command)
            self._evaluate_pdftk_exit_codes(exit_code)


    def _evaluate_pdftk_exit_codes(self, exit_code):
        '''
        @brief Evaluation of the PDFtk exit codes.
        @details
            If the exit code is not 0, a message with the PDFtk exit code appears.
        @par
            The PDFtk exit codes are not unique,
            rather they should be understood in the context of the selected options
            and also the error messages output.
            This makes it very difficult and difficult to deduce error causes
            from them correctly without parsing the error messages
            - which would also be very difficult.
            For this reason, the exit codes are not evaluated.
        @todo
            A terminal display of the output messages is planned for a later version.

        @see <https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/pdftk-2.02-src.zip>

        @param[in] exit_code The PDFtk exit code
        '''
        if exit_code == 0:
            #self._infobar.set_revealed(False)
            pass
        elif exit_code == 32512:
            self._infobar_message(Gtk.MessageType.ERROR,
                    "PDF Toolkit command '{}' not found!".format(pdftk.get_command()))
        else:
            self._infobar_message(Gtk.MessageType.ERROR,
                    "PDFtk exited with error code '{}'!".format(str(exit_code)))


    def _verify_rest_passwd_enc_is_correct(self):
        '''
        @brief Verify that both restriction passwords are correctly encoded.
        @details
            Only Characters of the character set Latin-1 are allowed.
            If a illegal character was detected, a warning message is displayed.
        @see self.on_button_execute_clicked()
        @see self._create_pdftk_cmd_cat_paths()

        @retval False One of the two passwords contains illegal characters
        @retval True  Both passwords contain no illegal characters
        '''
        str_passwd = self._entry_rest_passwd_user.get_text()
        #self._entry_rest_passwd_user.get_style_context().add_class("error") #TEST
        if self._str_is_latin1_encoded(str_passwd) == False:
            self._infobar_message(Gtk.MessageType.WARNING,
                    "User password contains illegal characters!"
                    " Only Latin-1 encoding is allowed.")
            return False
        str_passwd = self._entry_rest_passwd_owner.get_text()
        if self._str_is_latin1_encoded(str_passwd) == False:
            self._infobar_message(Gtk.MessageType.WARNING,
                    "Owner password contains illegal characters!"
                    " Only Latin-1 encoding is allowed.")
            return False
        return True


    def _str_is_latin1_encoded(self, string):
        '''
        @brief Check if string is Latin-1 encoded.
        @see self._verify_rest_passwd_enc_is_correct()

        @param[in] string The string to check
        @retval False String contains illegal characters
        @retval True  String contains no illegal characters
        '''
        try:
            string.encode(encoding="latin-1", errors="strict")
        except UnicodeError:
            return False
        return True


    def _create_pdftk_cmd(self):
        '''
        @brief Creation of the PDFtk command.
        @details
            This method initiates the building of the PDFtk command.
            When it was able to create a valid command,
            the method also initiates the execution of the command.
            The creation of the command depends on the shown stack children,
            which create their command part and return it back.
            Depending on the selected stack child,
            is checked that the user and owner passwords
            do not contain illegal characters before the command is created.

        @par Stack Children
            - `_page_main_cat`
            - `_page_main_srcdoc`
              - `_subpage_srcdoc_burst`
              - `_subpage_srcdoc_layer`
              - `_subpage_srcdoc_attach`
              - `_subpage_srcdoc_tools`

        @see on_button_execute_clicked()
        @see self._create_pdftk_cmd_cat()
        @see self._create_pdftk_cmd_burst()
        @see self._create_pdftk_cmd_layer()
        @see self._create_pdftk_cmd_attach()
        @see self._create_pdftk_cmd_tools()
        @see self._create_pdftk_cmd_rest()
        '''
        str_section_command = ""

        if self._stack_main.get_visible_child() is self._page_main_cat:
            if self._verify_rest_passwd_enc_is_correct() == True:
                str_section_command = self._create_pdftk_cmd_cat()
                if str_section_command:
                    str_section_command += self._create_pdftk_cmd_rest()
        elif self._stack_main.get_visible_child() is self._page_main_srcdoc:
            source_document = self._fcbutton_srcdoc.get_filename()
            if source_document:
                str_section_options = ""
                if self._stack_srcdoc.get_visible_child() is self._subpage_srcdoc_burst:
                    if self._verify_rest_passwd_enc_is_correct() == True:
                        str_section_options = self._create_pdftk_cmd_burst()
                        if str_section_options:
                            str_section_options += self._create_pdftk_cmd_rest()
                elif self._stack_srcdoc.get_visible_child() is self._subpage_srcdoc_layer:
                    if self._verify_rest_passwd_enc_is_correct() == True:
                        str_section_options = self._create_pdftk_cmd_layer()
                        if str_section_options:
                            str_section_options += self._create_pdftk_cmd_rest()
                elif self._stack_srcdoc.get_visible_child() is self._subpage_srcdoc_attach:
                    if self._verify_rest_passwd_enc_is_correct() == True:
                        str_section_options = self._create_pdftk_cmd_attach()
                        if str_section_options:
                            str_section_options += self._create_pdftk_cmd_rest()
                elif self._stack_srcdoc.get_visible_child() is self._subpage_srcdoc_tools:
                    str_section_options = self._create_pdftk_cmd_tools()
                else:
                    cli.debug_message("WARNING: Unknown sub page!")
                    #TODO: maybe rise exception

                if str_section_options:
                    str_section_command = strings.quote_and_escape_string(source_document)
                    str_section_command += ' ' + str_section_options
            else:
                self._infobar_message(Gtk.MessageType.INFO,
                        "No source document was chosen!")
        else:
            cli.debug_message("WARNING: Unknown main page!")
            #TODO: maybe rise exception

        return str_section_command


    def _create_pdftk_cmd_cat(self):
        '''
        @brief Creation of the PDFtk concatenate command.
        @details
            This is the first part of the concatenate command creation.
            It runs the output file chooser dialog
            and evaluates the static widgets of the concatenate page.
            It also calls a method to get the concatenate path command.

        @see self.on_button_execute_clicked()
        @see self._create_pdftk_cmd_cat_paths()

        @return str_command String with the concatenate part of the PDFtk command
        '''
        str_command = ""

        str_cat_paths = self._create_pdftk_cmd_cat_paths()
        if str_cat_paths: #TODO: check here, if iter_first is not None, and read paths when output doc is selected
            str_target = filechooser.fchooser_run(self._fcdialog_save_doc)
            if str_target:
                str_document_id = ""
                treeiter_cbox_doc_id = self._cbox_cat_document_id.get_active_iter()
                if treeiter_cbox_doc_id is None:
                    str_document_id = pdftk.ID_KEEP
                else:
                    str_active_id = self._lstore_cat_document_id.get_value(
                            treeiter_cbox_doc_id, self._COLUMN_ID)
                    if str_active_id == "new":
                        str_document_id = pdftk.ID_NEW
                    elif str_active_id == "first":
                        str_document_id = pdftk.ID_FIRST
                    elif str_active_id == "final":
                        str_document_id = pdftk.ID_FINAL
                    else:
                        cli.debug_message("WARNING: Unknown document ID")

                str_command += str_cat_paths
                str_command += ' ' + pdftk.OUTPUT
                str_command += ' ' + strings.quote_and_escape_string(str_target)
                if str_document_id:
                    str_command += ' ' + str_document_id
#        else:
#            self._infobar_message(Gtk.MessageType.INFO, "No active document for concatenation was found in the list!")

        return str_command


    def _create_pdftk_cmd_cat_paths(self):
        '''
        @brief Creation of the PDFtk concatenate path command.
        @details
            This is the second part of the creation of the concatenate command.
            It evaluates the concatenate list store.

        @see self._create_pdftk_cmd_cat()

        @return str_command String with the second part of the concatenate command
        '''
        str_command = ""
        self._index_cat_docs() #TODO: Check later, if this call is required here anymore

        # Append handles for every individual document stored in an active entry
        num_index = 0
        treeiter_entry = self._lstore_cat_documents.get_iter_first()
        while treeiter_entry is not None:
            if self._lstore_cat_documents.get_value(treeiter_entry, self._COLUMN_INDEX) == num_index:
                str_path = self._lstore_cat_documents.get_value(treeiter_entry, self._COLUMN_PATH)
                str_command += ' ' + strings.create_handle_from_number(num_index)
                str_command += '=' + strings.quote_and_escape_string(str_path)
                num_index += 1
            treeiter_entry = self._lstore_cat_documents.iter_next(treeiter_entry)

        if not str_command:
            self._infobar_message(Gtk.MessageType.INFO,
                    "No active document for concatenation was found in the list!")
            return "" # return empty command string

        # Append input password command, if at least one entry with a password was found
        treeiter_entry = self._lstore_cat_documents.get_iter_first()
        while treeiter_entry is not None:
            if self._lstore_cat_documents.get_value(treeiter_entry, self._COLUMN_PASSWORD):
                str_command += ' ' + pdftk.PASSWORD_INPUT
                break
            treeiter_entry = self._lstore_cat_documents.iter_next(treeiter_entry)

        # Assign input passwords to their corresponding handle
        num_index = 0
        treeiter_entry = self._lstore_cat_documents.get_iter_first()
        while treeiter_entry is not None:
            if self._lstore_cat_documents.get_value(treeiter_entry, self._COLUMN_INDEX) == num_index:
                str_password = self._lstore_cat_documents.get_value(treeiter_entry, self._COLUMN_PASSWORD)
                if str_password:
                    if self._str_is_latin1_encoded(str_password) == False:
                        self._infobar_message(Gtk.MessageType.INFO,
                                "Input password contains illegal characters!"
                                " Only Latin-1 encoding is allowed.")
                        return "" # return empty command string
                    str_command += ' ' + strings.create_handle_from_number(num_index)
                    str_command += '=' + strings.quote_and_escape_string(str_password)
            num_index += 1
            treeiter_entry = self._lstore_cat_documents.iter_next(treeiter_entry)

        # Insert the command "cat" or "shuffle"
        if self._ttbutton_cat_shuffle.get_active() == True:
            str_command += ' ' + pdftk.SHUFFLE
        else:
            str_command += ' ' + pdftk.CAT

        # Parsing the page selection string, selection filter and rotation
        # and appending the created command
        treeiter_entry = self._lstore_cat_documents.get_iter_first()
        while treeiter_entry is not None:
            num_index = self._lstore_cat_documents.get_value(treeiter_entry, self._COLUMN_INDEX)
            if num_index < GLib.MAXUINT:
                str_selection = self._lstore_cat_documents.get_value(treeiter_entry, self._COLUMN_SELECTION)
                valid, str_selection = strings.validate_page_selection_string(str_selection)
                if valid == True:

                    str_filter_id = self._lstore_cat_documents.get_value(treeiter_entry, self._COLUMN_FILTER_ID)
                    if str_filter_id == 'even':
                        str_filter = pdftk.PAGES_EVEN
                    elif str_filter_id == 'odd':
                        str_filter = pdftk.PAGES_ODD
                    else:
                        str_filter = pdftk.PAGES_ALL

                    str_rotation_id = self._lstore_cat_documents.get_value(treeiter_entry, self._COLUMN_ROTATION_ID)
                    if str_rotation_id == 'east':
                        str_rotation = pdftk.ROTATION_EAST
                    elif str_rotation_id == 'south':
                        str_rotation = pdftk.ROTATION_SOUTH
                    elif str_rotation_id == 'west':
                        str_rotation = pdftk.ROTATION_WEST
                    else:
                        str_rotation = pdftk.ROTATION_NORTH

                    arr_selection_parts = str_selection.split(None) # consecutive whitespace are regarded as a single separator
                    for str_selection_part in arr_selection_parts:
                        str_command += ' ' + strings.create_handle_from_number(num_index)
                        str_command += str_selection_part
                        str_command += str_filter
                        str_command += str_rotation
                else:
                    self._infobar_message(Gtk.MessageType.INFO, "Invalid page selection: '{}'".format(str_selection))
                    return "" # return empty command string

            treeiter_entry = self._lstore_cat_documents.iter_next(treeiter_entry)

        return str_command


    def _create_pdftk_cmd_burst(self):
        '''
        @brief Method to create the PDFtk command for sub page Burst.
        @details
            This method creates the PDFtk command
            by evaluating the widgets of the Burst sub page.

        @see self.on_button_execute_clicked()

        @return str_command String with the burst command
        '''
        str_command = ""
        str_target = filechooser.fchooser_run(self._fcdialog_select_folder)

        if str_target:
            str_template = self._label_burst_template.get_text()
            str_pattern = str_target + GLib.DIR_SEPARATOR_S + str_template

            str_command  =       pdftk.BURST
            str_command += ' ' + pdftk.OUTPUT
            str_command += ' ' + strings.quote_and_escape_string(str_pattern)

        return str_command


    def _create_pdftk_cmd_layer(self):
        '''
        @brief Method to create the PDFtk command for sub page Background / Stamp.
        @details
            This method creates the PDFtk command
            by evaluating the widgets of the Background / Stamp sub page.

        @see self.on_button_execute_clicked()

        @return str_command String with the background or stamp command
        '''
        str_command = ""
        str_layer_doc = self._fcbutton_layer_document.get_filename()
        if not str_layer_doc:
            self._infobar_message(Gtk.MessageType.INFO, "No layer document was chosen!")
        else:
            str_target = filechooser.fchooser_run(self._fcdialog_save_doc)
            if str_target:
                if self._rbutton_layer_watermark.get_active() == True:
                    if self._switch_layer_multiple.get_active() == True:
                        str_command = pdftk.BACKGROUND_MULTI
                    else:
                        str_command = pdftk.BACKGROUND
                else:
                    if self._switch_layer_multiple.get_active() == True:
                        str_command = pdftk.STAMP_MULTI
                    else:
                        str_command = pdftk.STAMP

                str_command += ' ' + strings.quote_and_escape_string(str_layer_doc)
                str_command += ' ' + pdftk.OUTPUT
                str_command += ' ' + strings.quote_and_escape_string(str_target)

        return str_command


    def _create_pdftk_cmd_attach(self):
        '''
        @brief Method to create the PDFtk command for sub page Attachments.
        @details
            This method creates the PDFtk command
            by evaluating the widgets of the Attachments sub page.
            It calls a method to get the part of the command
            with the paths from the attachment list store.

        @see self.on_button_execute_clicked()
        @see self._create_pdftk_cmd_attach_paths()

        @return str_command String with the attachment command
        '''
        str_command = ""
        str_command_options = ""
        str_attach_paths = self._create_pdftk_cmd_attach_paths()
        if str_attach_paths:
            str_target = filechooser.fchooser_run(self._fcdialog_save_doc)
            if str_target:
                str_command = pdftk.ATTACH_FILES
                str_command += str_attach_paths

                if self._rtbutton_attach_page.get_active() == True:
                    str_command_options += ' ' + pdftk.TO_PAGE
                    str_command_options += ' ' + str(int(self._sbutton_attach_page.get_value()))

                str_command += str_command_options
                str_command += ' ' + pdftk.OUTPUT
                str_command += ' ' + strings.quote_and_escape_string(str_target)
        else:
            self._infobar_message(Gtk.MessageType.INFO, "No file to attach was found in the list!")

        return str_command


    def _create_pdftk_cmd_attach_paths(self):
        '''
        @brief Method to create the PDFtk command for sub page Attachments.
        @details
            This method creates the part
            with the paths from the attachment list store
            of the Attachment sub page for the PDFtk command.
            The created command part is just a list with the files to attach.

        @see self._create_pdftk_cmd_attach()

        @return str_command String with the path part of the attachment command
        '''
        str_command = ""

        treeiter_files = self._lstore_attach_files.get_iter_first()
        while treeiter_files is not None:
            path = self._lstore_attach_files.get_value(treeiter_files, self._COLUMN_PATH)
            str_command += ' ' + strings.quote_and_escape_string(path)
            treeiter_files = self._lstore_attach_files.iter_next(treeiter_files)

        return str_command


    def _create_pdftk_cmd_tools(self):
        '''
        @brief Method to create the PDFtk command for sub page Tools.
        @details
            This method creates the PDFtk command
            by evaluating the widgets of the Tools sub page.
        @note
            If the target string is empty,
            no command string is created and also remains empty.
        @see self.on_button_execute_clicked()
        @return str_command String with the selected tool command
        '''
        # Get the target string (document, file or directory path)
        str_dump_file = self._fcbutton_tools_dump_file.get_filename()
        str_fdf_file = self._fcbutton_tools_fdf_file.get_filename()
        str_target = ""

        if self._rbutton_tools_unpack.get_active() == True:
            response = self._fcdialog_select_folder.run()
            self._fcdialog_select_folder.hide()
            if response == Gtk.ResponseType.OK:
                str_target = self._fcdialog_select_folder.get_current_folder()
        elif self._rbutton_tools_dump_annots.get_active() == True \
                or self._rbutton_tools_ddfields.get_active() == True \
                or self._rbutton_tools_ddata.get_active() == True:
            str_target = filechooser.fchooser_run(self._fcdialog_save_dump_file)
        elif self._rbutton_tools_generate_fdf.get_active() == True:
            str_target = filechooser.fchooser_run(self._fcdialog_save_fdf_file)
        else:
            if self._rbutton_tools_update_info.get_active() == True:
                if str_dump_file:
                    str_target = filechooser.fchooser_run(self._fcdialog_save_doc)
                else:
                    self._infobar_message(Gtk.MessageType.INFO,
                            "No metadata dump file was chosen! (*.dump)")
                    return ""
            elif self._rbutton_tools_fform.get_active() == True:
                if str_fdf_file:
                    str_target = filechooser.fchooser_run(self._fcdialog_save_doc)
                else:
                    self._infobar_message(Gtk.MessageType.INFO,
                            "No fill form file was chosen! (*.fdf, *.xfdf)")
                    return ""
            else:
                str_target = filechooser.fchooser_run(self._fcdialog_save_doc)
        #cli.debug_message("TEST: str_target: '{}'".format(str_target)) #TEST

        # Build the command string
        str_command = ""
        if str_target:
            str_target = strings.quote_and_escape_string(str_target)

            if self._rbutton_tools_repair.get_active() == True:
                str_command += " " + pdftk.OUTPUT
                str_command += " " + str_target
            elif self._rbutton_tools_unpack.get_active() == True:
                str_command += " " + pdftk.UNPACK_FILES
                str_command += " " + pdftk.OUTPUT
                str_command += " " + str_target
            elif self._rbutton_tools_uncompress.get_active() == True:
                str_command += " " + pdftk.OUTPUT
                str_command += " " + str_target
                str_command += " " + pdftk.UNCOMPRESS
            elif self._rbutton_tools_compress.get_active() == True:
                str_command += " " + pdftk.OUTPUT
                str_command += " " + str_target
                str_command += " " + pdftk.COMPRESS
            elif self._rbutton_tools_dump_annots.get_active() == True:
                str_command += " " + pdftk.DUMP_DATA_ANNOTS
                str_command += " " + pdftk.OUTPUT
                str_command += " " + str_target
            elif self._rbutton_tools_ddfields.get_active() == True:
                if self._cbutton_tools_ddfields_utf8.get_active() == True:
                    str_command += " " + pdftk.DUMP_DATA_FIELDS_UTF8
                else:
                    str_command += " " + pdftk.DUMP_DATA_FIELDS
                str_command += " " + pdftk.OUTPUT
                str_command += " " + str_target
            elif self._rbutton_tools_ddata.get_active() == True:
                if self._cbutton_tools_ddata_utf8.get_active() == True:
                    str_command += " " + pdftk.DUMP_DATA_UTF8
                else:
                    str_command += " " + pdftk.DUMP_DATA
                str_command += " " + pdftk.OUTPUT
                str_command += " " + str_target
            elif self._rbutton_tools_update_info.get_active() == True:
                if str_dump_file:
                    if self._cbutton_tools_update_info_utf8.get_active() == True:
                        str_command += " " + pdftk.UPDATE_INFO_UTF8
                    else:
                        str_command += " " + pdftk.UPDATE_INFO
                    str_command += " " + strings.quote_and_escape_string(str_dump_file)
                    str_command += " " + pdftk.OUTPUT
                    str_command += " " + str_target
                else:  # Has already been checked and should never be the case here
                    self._infobar_message(Gtk.MessageType.INFO,
                            "No metadata dump file was chosen! (*.dump)")
                    return ""
            elif self._rbutton_tools_generate_fdf.get_active() == True:
                str_command += " " + pdftk.GENERATE_FDF
                str_command += " " + pdftk.OUTPUT
                str_command += " " + str_target
            elif self._rbutton_tools_fform.get_active() == True:
                if str_fdf_file:
                    str_command += " " + pdftk.FILL_FORM
                    str_command += " " + strings.quote_and_escape_string(str_fdf_file)
                    str_command += " " + pdftk.OUTPUT
                    str_command += " " + str_target
                    if self._cbutton_tools_fform_drop_xfa.get_active() == True:
                        str_command += " " + pdftk.DROP_XFA
                    if self._cbutton_tools_fform_appearances.get_active() == True:
                        str_command += " " + pdftk.NEED_APPEARANCES
                    if self._cbutton_tools_fform_flatten.get_active() == True:
                        str_command += " " + pdftk.FLATTEN
                else:  # Has already been checked and should never be the case here
                    self._infobar_message(Gtk.MessageType.INFO,
                            "No fill form file was chosen! (*.fdf, *.xfdf)")
                    return ""
            elif self._rbutton_tools_flatten.get_active() == True:
                str_command += " " + pdftk.OUTPUT
                str_command += " " + str_target
                str_command += " " + pdftk.FLATTEN
            elif self._rbutton_tools_drop_xfa.get_active() == True:
                str_command += " " + pdftk.OUTPUT
                str_command += " " + str_target
                str_command += " " + pdftk.DROP_XFA

        #cli.debug_message("TEST: str_command: '{}'".format(str_command)) #TEST
        return str_command


    def _create_pdftk_cmd_rest(self):
        '''
        @brief   Method: Create the restriction options for the PDFtk command.
        @details
            This method creates a PDFtk command part
            by evaluating the widgets of the Permissions menu.

        @see self.on_button_execute_clicked()

        @return String with the restriction options for the PDFtk command

        @par When checking if one or more options are active _(OR)_
            - when 'Screen readers'      is not active, also 'Copy Contents'      is not active
            - when 'Assembly Contents'   is not active, also 'Modify Contents'    is not active
            - when 'Fill In Annotations' is not active, also 'Modify Annotations' is not active

        @par When checking if all options are active _(AND)_
            - when 'Copy Contents'      is active, also 'Screen readers'      is active
            - when 'Modify Contents'    is active, also 'Assembly Contents'   is active
            - when 'Modify Annotations' is active, also 'Fill In Annotations' is active
        '''
        str_cmd_password = ""
        str_cmd_restrictions = ""
        str_cmd_encryption = ""

        # Read Passwords
        str_passwd_user = self._entry_rest_passwd_user.get_text()
        str_passwd_owner = self._entry_rest_passwd_owner.get_text()

        if str_passwd_user or str_passwd_owner:
            if str_passwd_user == str_passwd_owner:
                # User and owner password are identical!
                # In this case the document can only be protected with the user password.
                self._infobar_message(Gtk.MessageType.WARNING,
                        "User and owner password are identical!")
                str_cmd_password += " " + pdftk.PASSWORD_USER
                str_cmd_password += " " + strings.quote_and_escape_string(str_passwd_user)
            else:
                if str_passwd_user:
                    str_cmd_password += " " + pdftk.PASSWORD_USER
                    str_cmd_password += " " + strings.quote_and_escape_string(str_passwd_user)

                if str_passwd_owner:
                    str_cmd_password += " " + pdftk.PASSWORD_OWNER
                    str_cmd_password += " " + strings.quote_and_escape_string(str_passwd_owner)

        # Read Restrictions
        if self._rbutton_rest_enc_none.get_active() == False:
            if self._cbutton_rest_perm_printing.get_active() == True \
                    or self._cbutton_rest_perm_degraded_printing.get_active() == True \
                    or self._cbutton_rest_perm_screen_readers.get_active() == True \
                    or self._cbutton_rest_perm_assembly_contents.get_active() == True \
                    or self._cbutton_rest_perm_fill_in_annots.get_active() == True:

                str_cmd_restrictions += " " + pdftk.ALLOW

                if self._cbutton_rest_perm_printing.get_active() == True \
                        and self._cbutton_rest_perm_degraded_printing.get_active() == True \
                        and self._cbutton_rest_perm_copy_contents.get_active() == True \
                        and self._cbutton_rest_perm_modify_contents.get_active() == True \
                        and self._cbutton_rest_perm_modify_annotations.get_active() == True:

                    str_cmd_restrictions += " " + pdftk.FEATURES_ALL
                else:
                    if self._cbutton_rest_perm_printing.get_active() == True:
                        str_cmd_restrictions += " " + pdftk.PRINTING

                    if self._cbutton_rest_perm_degraded_printing.get_active() == True:
                        str_cmd_restrictions += " " + pdftk.DEGRADED_PRINTING

                    if self._cbutton_rest_perm_copy_contents.get_active() == True:
                        str_cmd_restrictions += " " + pdftk.COPY_CONTENTS
                    elif self._cbutton_rest_perm_screen_readers.get_active() == True:
                        str_cmd_restrictions += " " + pdftk.SCREEN_READERS

                    if self._cbutton_rest_perm_modify_contents.get_active() == True:
                        str_cmd_restrictions += " " + pdftk.MODIFY_CONTENTS
                    elif self._cbutton_rest_perm_assembly_contents.get_active() == True:
                        str_cmd_restrictions += " " + pdftk.ASSEMBLY

                    if self._cbutton_rest_perm_modify_annotations.get_active() == True:
                        str_cmd_restrictions += " " + pdftk.MODIFY_ANNOTATIONS
                    elif self._cbutton_rest_perm_fill_in_annots.get_active() == True:
                        str_cmd_restrictions += " " + pdftk.FILL_IN

        # Read Encryption
        if self._rbutton_rest_enc_rc4_40bit.get_active() == True:
            str_cmd_encryption = " " + pdftk.ENCRYPT_40BIT
        elif self._rbutton_rest_enc_rc4_128bit.get_active() == True:
            str_cmd_encryption = " " + pdftk.ENCRYPT_128BIT
        else:
            if str_passwd_user or str_passwd_user:
                self._infobar_message(Gtk.MessageType.WARNING, "A password without an encryption has no effect!")

            if str_cmd_restrictions:
                self._infobar_message(Gtk.MessageType.WARNING, "Restrictions without an encryption have no effect!")

        # Create Permissions command
        str_command = str_cmd_password + str_cmd_restrictions + str_cmd_encryption
        return str_command


    # Handler for main page Menu
    def on_lbox_main_menu_row_activated(self, list_box, row):
        '''
        @brief Signal Handler when a ListBox row of the Main Menu was activated.
        @details
            This signal hander switches the stack pages according to the selected row.
            It also sets related widgets visible.

        @TODO Rework this method!

        @param[in] list_box The object which received the signal _(not used)_
        @param[in] row      The activated row
        '''
        if row is self._lbrow_main_cat:
            self._headerbar.set_title(self._str_title_cat)
            self._headerbar.set_subtitle(self._str_subtitle_cat)
            self._stack_main.set_visible_child(self._page_main_cat)
            self._revealer_button_menu.set_reveal_child(True)
            self._revealer_button_help.set_reveal_child(True)
            self._mbutton_rest.set_visible(True)
            self._stack_hbar_right.set_visible_child(self._page_exec)
        elif row is self._lbrow_main_burst:
            self._headerbar.set_title(self._str_title_burst)
            self._headerbar.set_subtitle(self._str_subtitle_burst)
            self._stack_srcdoc.set_visible_child(self._subpage_srcdoc_burst)
            self._stack_main.set_visible_child(self._page_main_srcdoc)
            self._revealer_button_menu.set_reveal_child(True)
            self._revealer_button_help.set_reveal_child(True)
            self._mbutton_rest.set_visible(True)
            self._stack_hbar_right.set_visible_child(self._page_exec)
            self.on_section_burst_changed()
        elif row is self._lbrow_main_layer:
            self._headerbar.set_title(self._str_title_layer)
            self._headerbar.set_subtitle(self._str_subtitle_layer)
            self._stack_srcdoc.set_visible_child(self._subpage_srcdoc_layer)
            self._stack_main.set_visible_child(self._page_main_srcdoc)
            self._revealer_button_menu.set_reveal_child(True)
            self._revealer_button_help.set_reveal_child(True)
            self._mbutton_rest.set_visible(True)
            self._stack_hbar_right.set_visible_child(self._page_exec)
        elif row is self._lbrow_main_attach:
            self._headerbar.set_title(self._str_title_attach)
            self._headerbar.set_subtitle(self._str_subtitle_attach)
            self._stack_srcdoc.set_visible_child(self._subpage_srcdoc_attach)
            self._stack_main.set_visible_child(self._page_main_srcdoc)
            self._revealer_button_menu.set_reveal_child(True)
            self._revealer_button_help.set_reveal_child(True)
            self._mbutton_rest.set_visible(True)
            self._stack_hbar_right.set_visible_child(self._page_exec)
        elif row is self._lbrow_main_tools:
            self._headerbar.set_title(self._str_title_tools)
            self._headerbar.set_subtitle(self._str_subtitle_tools)
            self._stack_srcdoc.set_visible_child(self._subpage_srcdoc_tools)
            self._stack_main.set_visible_child(self._page_main_srcdoc)
            self._revealer_button_menu.set_reveal_child(True)
            self._revealer_button_help.set_reveal_child(True)
            self._mbutton_rest.set_visible(False)
            self._stack_hbar_right.set_visible_child(self._page_exec)
        else:
            cli.debug_message("WARNING: unknown list box row: '{}'".format(row))


    # Handler for main page Concatenate
    def on_toolbutton_cat_add_doc_clicked(self, tbutton):
        '''
        @brief Signal Handler for the ToolButton Concatenate click event.
        @details
            This signal handler runs a FileChooserDialog with multiple selection
            to add new documents to the Concatenate ListStore.
            If a file name that already exists in the list is added,
            file-specific values are taken over for the new entry.
            After adding the documents,
            a method is called which re-indexes all list entries.

        @see self._get_data_from_cat_list()
        @see self._update_cat_combobox_document_id()

        @param[in] tbutton The object which received the signal _(not used)_
        '''
        response = self._fcdialog_open_doc_multi.run()
        self._fcdialog_open_doc_multi.hide()

        if response == Gtk.ResponseType.OK:
            str_filenames = self._fcdialog_open_doc_multi.get_filenames()

            treeselection = self._tview_cat_documents.get_selection()
            treemodel, treepaths = treeselection.get_selected_rows()

            if treepaths == []:
                treeiter_selected = None
            else:
                treeiter_selected = treemodel.get_iter(treepaths[0]) # get the first iterator

            for str_filename in str_filenames:
                str_doc_basename = GLib.path_get_basename(str_filename)
                str_tooltip = self._STR_PATH + ": '" + str_filename + "'"
                str_page_selection = ""
                str_page_filter = self._lstore_cat_filter[self._ROW_FILTER_ALL][self._COLUMN_TEXT]
                str_page_rotation = self._lstore_cat_rotation[self._ROW_ROTATION_NORTH][self._COLUMN_TEXT]
                str_doc_passwd = self._get_data_from_cat_list(str_filename, self._COLUMN_PASSWORD)
                str_doc_pages = self._get_data_from_cat_list(str_filename, self._COLUMN_PAGES)
                num_doc_index = GLib.MAXUINT
                str_page_filter_id = self._lstore_cat_filter[self._ROW_FILTER_ALL][self._COLUMN_ID]
                str_page_rotation_id = self._lstore_cat_rotation[self._ROW_ROTATION_NORTH][self._COLUMN_ID]

                if not str_doc_pages:
                    str_doc_pages = str(strings.count_pages_of_document(str_filename))

                if treeiter_selected == None:
                    treeiter_new = self._lstore_cat_documents.append(None)
                else:
                    treeiter_new = self._lstore_cat_documents.insert_before(
                            treeiter_selected)

                self._lstore_cat_documents[treeiter_new] = [
                        True,
                        str_filename,
                        str_doc_basename,
                        str_tooltip,
                        str_page_selection,
                        str_page_filter,
                        str_page_rotation,
                        str_doc_passwd,
                        str_doc_pages,
                        num_doc_index,
                        str_page_filter_id,
                        str_page_rotation_id]

                self._update_cat_combobox_document_id()


    def on_toolbutton_cat_remove_doc_clicked(self, tbutton):
        '''
        @brief Handler for the ToolButton Concatenate remove document clicked signal.
        @details
            This signal handler method removes selected entries
            from the Concatenate ListStore.

        @param[in] tbutton The object which received the signal _(not used)_
        '''
        treeselection = self._tview_cat_documents.get_selection()
        tree_model_selected, tree_paths_selected = treeselection.get_selected_rows()
        treeiters_selected = []
        for tree_path_selected in tree_paths_selected:
            treeiters_selected.append(tree_model_selected.get_iter(tree_path_selected))
        for treeeiter_entries_selected in treeiters_selected:
            self._lstore_cat_documents.remove(treeeiter_entries_selected)
        self._update_cat_combobox_document_id()


    def on_toolbutton_cat_duplicate_doc_clicked(self, tbutton):
        '''
        @brief Handler for the ToolButton Concatenate duplicate document clicked signal.
        @details
            This signal handler method duplicates selected entries
            in the Concatenate ListStore.

        @param[in] tbutton The object which received the signal _(not used)_
        '''
        treeselection = self._tview_cat_documents.get_selection()
        tree_model_selected, tree_paths_selected = treeselection.get_selected_rows()

        tree_iters_selected = []
        for tree_path_selected in tree_paths_selected:
            tree_iters_selected.append(tree_model_selected.get_iter(tree_path_selected))
        for treeiter_selected in tree_iters_selected:
            treeiter_new = self._lstore_cat_documents.append(None)
            self._lstore_cat_documents[treeiter_new][:] = \
                    self._lstore_cat_documents[treeiter_selected][:]


    def on_crenderer_cat_active_toggled(self, crtoggle, str_tview_path):
        '''
        @brief Signal Handler for a CellRenderer Toggle in section Cat: The Active button was toggled.
        @details
            Toggles the boolean value in the concatenate list store.

        @param[in] crtoggle       The object which received the signal _(not used)_
        @param[in] str_tview_path String representation of Gtk.TreePath describing the event location
        '''
        treeiter = self._lstore_cat_documents.get_iter(str_tview_path)
        value    = self._lstore_cat_documents.get_value(treeiter, self._COLUMN_ACTIVE)
        self._lstore_cat_documents.set_value(treeiter, self._COLUMN_ACTIVE, not value)
        self._update_cat_combobox_document_id()


    def on_crenderer_cat_selection_edited(
            self, crtext, str_tview_path, str_new_text):
        '''
        @brief Signal Handler for a CellRenderer Text in section Cat: The Page Selection was changed.
        @details
            Copy the new selection string for this entry
            into the selection string cell of the concatenate list store.

        @param[in] crtext         The object which received the signal _(not used)_
        @param[in] str_tview_path String representation of Gtk.TreePath describing the event location
        @param[in] str_new_text   The new text
        '''
        treeiter_entry = self._lstore_cat_documents.get_iter(str_tview_path)
        self._lstore_cat_documents.set_value(treeiter_entry, self._COLUMN_SELECTION, str_new_text)


    def on_crenderer_cat_filter_changed(
            self, crcombo, str_tview_path, treeiter_combo):
        '''
        @brief Signal Handler for a CellRenderer Combo in section Cat: The Page Filter was changed.
        @details
            Copies the selected text from the list store of the cell renderer combo
            into the corresponding cell of the concatenate list store.

        @param[in] crcombo        The object which received the signal _(not used)_
        @param[in] str_tview_path String representation of Gtk.TreePath describing the event location
        @param[in] treeiter_combo The new iter selected in the combo box (combo box model)
        '''
        str_text = self._lstore_cat_filter.get_value(treeiter_combo, self._COLUMN_TEXT)
        str_id = self._lstore_cat_filter.get_value(treeiter_combo, self._COLUMN_ID)
        treeiter_entry = self._lstore_cat_documents.get_iter(str_tview_path)
        self._lstore_cat_documents.set_value(treeiter_entry, self._COLUMN_FILTER_TEXT, str_text)
        self._lstore_cat_documents.set_value(treeiter_entry, self._COLUMN_FILTER_ID, str_id)


    def on_crenderer_cat_rotation_changed(
            self, crcombo, str_tview_path, treeiter_combo):
        '''
        @brief Signal Handler for a CellRenderer Combo in section Cat: The Rotation was changed.
        @details
            Copies the selected text from the list store of the cell renderer combo
            into the corresponding cell of the concatenate list store.

        @param[in] crcombo        The object which received the signal _(not used)_
        @param[in] str_tview_path String representation of Gtk.TreePath describing the event location
        @param[in] treeiter_combo The new iter selected in the combo box (combo box model)
        '''
        str_text = self._lstore_cat_rotation.get_value(treeiter_combo, self._COLUMN_TEXT)
        str_id = self._lstore_cat_rotation.get_value(treeiter_combo, self._COLUMN_ID)
        treeiter_entry = self._lstore_cat_documents.get_iter(str_tview_path)
        self._lstore_cat_documents.set_value(treeiter_entry, self._COLUMN_ROTATION_TEXT, str_text)
        self._lstore_cat_documents.set_value(treeiter_entry, self._COLUMN_ROTATION_ID, str_id)


    def on_crenderer_cat_password_edited(
            self, cellrenderer_text, str_tview_path, str_new_text):
        '''
        @brief Signal Handler for a CellRenderer Text in section Cat: The Password was edited.
        @details
            Copy the new password string for this entry
            into the password string cell of the concatenate list store.
            Then call a method to clone the password string of this entry
            into the password string cell of every entry with the same filename.

        @param[in] cellrenderer_text The object which received the signal _(not used)_
        @param[in] str_tview_path    String representation of `Gtk.TreePath describing the event location
        @param[in] str_new_text      The new text
        '''
        treeiter_entry = self._lstore_cat_documents.get_iter(str_tview_path)
        self._lstore_cat_documents.set_value(treeiter_entry,
                self._COLUMN_PASSWORD, str_new_text)
        self._sync_cat_passwords(treeiter_entry)


    def _index_cat_docs(self):
        '''
        @brief Index concatenate documents.
        @details
            This method indexes all active entries of the Concatenate list store
            with a unique ID number.
            Individual documents are identified by their path.
            Entries with the same path are assigned the same ID number.
            A index number with Glib.MAXUINT marks an inactive entry.
        '''
        # Set the index values of all entries to an "invalid" number (GLib.MAXUINT),
        # which indicates later, that this entry has no "valid" index yet.
        treeiter_A = self._lstore_cat_documents.get_iter_first()
        while treeiter_A is not None:
            self._lstore_cat_documents.set_value(treeiter_A, self._COLUMN_INDEX, GLib.MAXUINT)
            treeiter_A = self._lstore_cat_documents.iter_next(treeiter_A)

        # Search for the first unindexed entry and assign a new ID number.
        # Then continue searching for unindexed entries with the same path
        # and assign them the same ID number.
        #  - treeiter_A: compares index entries
        #  - treeiter_B: compares path  entries
        index_number = 0
        treeiter_A = treeiter_B = self._lstore_cat_documents.get_iter_first()
        while treeiter_A is not None:
            if self._lstore_cat_documents.get_value(treeiter_A, self._COLUMN_ACTIVE) == True:
                if self._lstore_cat_documents.get_value(treeiter_A, self._COLUMN_INDEX) == GLib.MAXUINT:
                    path_A = self._lstore_cat_documents.get_value(treeiter_A, self._COLUMN_PATH)
                    treeiter_B = treeiter_A
                    while treeiter_B is not None:
                        if self._lstore_cat_documents.get_value(treeiter_B, self._COLUMN_ACTIVE) == True:
                            path_B = self._lstore_cat_documents.get_value(treeiter_B, self._COLUMN_PATH)
                            if path_A == path_B:
                                self._lstore_cat_documents.set_value(treeiter_B, self._COLUMN_INDEX, index_number)
                        treeiter_B = self._lstore_cat_documents.iter_next(treeiter_B)
                    index_number += 1
            treeiter_A = self._lstore_cat_documents.iter_next(treeiter_A)

        # TEST
        #treeiter = self._lstore_cat_documents.get_iter_first()
        #while treeiter is not None:
        #    cli.debug_message("TEST: index: {}, path: '{}'".format(
        #        self._lstore_cat_documents.get_value(treeiter, self._COLUMN_INDEX),
        #        self._lstore_cat_documents.get_value(treeiter, self._COLUMN_PATH)))
        #    treeiter = self._lstore_cat_documents.iter_next(treeiter)


    def _sync_cat_passwords(self, treeiter_source):
        '''
        @brief Method: Synchronize Concatenate Passwords.
        @details
            Find row entries with the same filename like the source row (iter)
            in the concatenate list store
            and copy the password from the source row to the found rows.

        @TODO maybe using _index_cat_docs()

        param[in] treeiter_source Tree iterator pointing to the source entry
        '''
        path     = self._lstore_cat_documents.get_value(treeiter_source, self._COLUMN_PATH)
        password = self._lstore_cat_documents.get_value(treeiter_source, self._COLUMN_PASSWORD)

        treeiter_target = self._lstore_cat_documents.get_iter_first()
        while treeiter_target is not None:
            if self._lstore_cat_documents.get_value(treeiter_target, 1) == path:
                 self._lstore_cat_documents.set_value(
                         treeiter_target, self._COLUMN_PASSWORD, password)
            treeiter_target = self._lstore_cat_documents.iter_next(treeiter_target)


    def _get_data_from_cat_list(self, str_path, num_column):
        '''
        @brief   Get stored data of a document from concatenate list store.
        @details
            This method finds the first entry with the same path string
            as the one passed in the parameters and returns its column data.
            If no data has been assigned to an entry found so far,
            an empty string is returned.
            If there is no entry with the searched path string,
            an empty string will also be returned.

            This method is called when another document is added to the list.
            If the path to the new document already exists in the list,
            then the same data should be noted for this new entry.

        @param[in] str_path   String with the filename
        @param[in] num_column Column number, containing the data
        @return               Data string
        '''
        str_data = ""
        treeiter = self._lstore_cat_documents.get_iter_first()
        while treeiter is not None:
            if self._lstore_cat_documents.get_value(treeiter, self._COLUMN_PATH) == str_path:
                str_data = self._lstore_cat_documents.get_value(treeiter, num_column)
                break
            treeiter = self._lstore_cat_documents.iter_next(treeiter)
        return str_data


    def _scan_cat_list_for_diff_active_entries(self):
        '''
        @brief Scan the concatenate list store for active entries with different filenames.
        @details
            This information is required to update the Document ID combo box.

        @see _update_cat_combobox_document_id()

        @retval 0 No active entry was found or list is empty
        @retval 1 Active entries with one or the same document path was found
        @retval 2 Active entries with two (or more) various document path was found
        '''
        treeiter_A = self._lstore_cat_documents.get_iter_first()
        while treeiter_A is not None:
            if self._lstore_cat_documents.get_value(treeiter_A, self._COLUMN_ACTIVE) == True:
                str_path_A = self._lstore_cat_documents.get_value(treeiter_A, self._COLUMN_PATH)
                treeiter_B = treeiter_A
                while treeiter_B is not None:
                    if self._lstore_cat_documents.get_value(treeiter_B, self._COLUMN_ACTIVE) == True:
                        str_path_B = self._lstore_cat_documents.get_value(treeiter_B, self._COLUMN_PATH)
                        if str_path_A != str_path_B:
                            return 2  # a second active document path was found
                    treeiter_B = self._lstore_cat_documents.iter_next(treeiter_B)
                return 1              # no second active document path was found, but a first was
            treeiter_A = self._lstore_cat_documents.iter_next(treeiter_A)
        return 0                      # no active document was found


    def _update_cat_combobox_document_id(self):
        '''
        @brief Update the Concatenate document ID combo box.
        @details
            This method is always called when something in the list has changed.

        @see _scan_cat_list_for_diff_active_entries()
        '''
        active_documents = self._scan_cat_list_for_diff_active_entries()
        if active_documents == 0:
            self._cbox_cat_document_id.set_active_id(None)
            self._cbox_cat_document_id.set_sensitive(False)
            self._entry_cat_document_id.set_text("")
            self._entry_cat_document_id.set_placeholder_text("")
        elif active_documents == 1:
            self._cbox_cat_document_id.set_active_id('new')
            self._cbox_cat_document_id.set_sensitive(False)
            self._entry_cat_document_id.set_text("")
            self._entry_cat_document_id.set_placeholder_text("Keep document ID")
        else:
            self._cbox_cat_document_id.set_active_id('first') # TODO: restore old ID
            self._cbox_cat_document_id.set_sensitive(True)


    # Handler for all source document pages
    def on_fcbutton_file_set(self, fcbutton):
        '''
        @brief Signal Handler: On FileChooserButton File set
        @details
            Sets the tool tip to the actual selected path.

        @param[in] fcbutton The object which received the signal
        '''
        fcbutton.set_tooltip_markup(self._STR_PATH + ": '" + fcbutton.get_filename() + "'" )


    # Handler for sub page Burst
    def on_section_burst_changed(self, *args):
        '''
        @brief   Signal Handler: On section Burst has any widget changed.
        @details
            This signal handler is called from any (useful) editable widget
            of the Burst section when it has changed its state
            and when section Burst gets visible.
            The handler calls a function to get the PDFtk burst template string,
            assembled from the states of the widgets in section Burst
            and makes this string visible.

        @see self._refresh_burst_template()
        '''
        num_pages = self._source_document_pages

        if num_pages == 0:
            self._rbutton_burst_manual.set_active(True)
        #else:
        #    self._rbutton_burst_auto.set_active(True)

        self._refresh_burst_template(num_pages)


    def on_rbutton_burst_manual_toggled(self, button):
        '''
        '''
        if button.get_active() == True:
            self._sbutton_burst_manual.set_sensitive(True)
        else:
            self._sbutton_burst_manual.set_sensitive(False)


    def on_entry_burst_prefix_icon_pressed(self, entry, icon_pos, event):
        '''
        '''
        if icon_pos == Gtk.EntryIconPosition.SECONDARY:
            entry.set_text("")


    def on_entry_burst_suffix_icon_pressed(self, entry, icon_pos, event):
        '''
        '''
        if icon_pos == Gtk.EntryIconPosition.SECONDARY:
            entry.set_text("")


    def _refresh_burst_template(self, num_pages):
        '''
        Creates the burst pattern for the PDFtk command.
        '''
        str_prefix    = self._entry_burst_prefix.get_text()
        str_suffix    = self._entry_burst_suffix.get_text()
        str_digits    = "3" # set three digits a fall back
        cmd_base      = "d" # set decimal as fall back base
        num_base      = 10  # set decimal as fall back base
        str_extension = ""

        if not str_prefix:
            str_prefix = self._entry_burst_prefix.get_placeholder_text()

        #TODO: Gtk.ComboBox.use get_active_id()
        treeiter = self._cbox_burst_base.get_active_iter()
        if treeiter is not None:
            treemodel = self._cbox_burst_base.get_model()
            str_id = treemodel[treeiter][self._COLUMN_ID]
            if str_id == 'oct':
                num_base = 8
                cmd_base = pdftk.COUNT_OCT
            elif str_id == 'hex':
                num_base = 16
                cmd_base = pdftk.COUNT_HEX
            else:
                num_base = 10
                cmd_base = pdftk.COUNT_DEC

        if self._rbutton_burst_auto.get_active() == True:
            if num_pages > 0:
                str_digits = str(strings.calculate_digits_of_number_for_base(num_base, num_pages))
            else:
                str_digits = "3" # fallback value
        else:
            str_digits = str(int(self._sbutton_burst_manual.get_value()))

        if self._switch_burst_ext.get_active() == True:
            str_extension = '.pdf'

        str_template = str_prefix + pdftk.TEMPLATE + str_digits + cmd_base \
                + str_suffix + str_extension

        self._label_burst_template.set_label(str_template)


    # Signal Handler: Sub Page Attachment
    def on_toolbutton_attach_add_file_clicked(self, tool_button):
        '''
        Gtk.TreeModel() is the base class of Gtk.ListStore()

        # first get selection of the tree view
        treeselection = self._tview_attach_files.get_selection()

        # then get selected rows of the list store
        treemodel, treepaths = treeselection.get_selected_rows()
        '''
        response = self._fcdialog_open_all_multi.run()
        self._fcdialog_open_all_multi.hide()

        if response == Gtk.ResponseType.OK:
            str_filenames = self._fcdialog_open_all_multi.get_filenames()

            treeselection = self._tview_attach_files.get_selection()
            treemodel, treepaths = treeselection.get_selected_rows()

            if treepaths == []:
                treeiter_selected = None
            else:
                treeiter_selected = treemodel.get_iter(treepaths[0]) # get the first iterator

            for str_filename in str_filenames:
                str_file_basename = GLib.path_get_basename(str_filename)
                str_tooltip = self._STR_PATH + ": '" + str_filename + "'"

                if treeiter_selected == None:
                    treeiter_new = self._lstore_attach_files.append(None)
                else:
                    treeiter_new = self._lstore_attach_files.insert_before(
                            treeiter_selected)

                self._lstore_attach_files[treeiter_new] = [
                        True,
                        str_filename,
                        str_file_basename,
                        str_tooltip]


    def on_toolbutton_attach_remove_file_clicked(self, tool_button):
        '''
        Generate a list of iterators form the tree paths first.
        Delete then the list store entries by using this iterator list.
        '''
        treeselection = self._tview_attach_files.get_selection()
        tree_model_selected, tree_paths_selected = treeselection.get_selected_rows()

        treeiters_selected = []
        for tree_path_selected in tree_paths_selected:
            treeiters_selected.append(tree_model_selected.get_iter(tree_path_selected))
        for treeiter_selected in treeiters_selected:
            self._lstore_attach_files.remove(treeiter_selected)


    def on_rtoolbutton_attach_page_toggled(self, button):
        '''
        '''
        if button.get_active() == True:
            self._toolitem_attach_page.set_sensitive(True)
        else:
            self._toolitem_attach_page.set_sensitive(False)


    def on_crenderer_attach_add_toggled(self, cell_renderer_toggle, str_tview_path):
        '''
        @brief Signal Handler for a CellRenderer Toggle in section Attach: The Active button was toggled.
        @details
            Toggles the boolean value in the concatenate list store.

        @param[in] crtoggle       The object which received the signal _(not used)_
        @param[in] str_tview_path String representation of Gtk.TreePath describing the event location
        '''
        treeiter = self._lstore_attach_files.get_iter(str_tview_path)
        value = self._lstore_attach_files.get_value(treeiter, self._COLUMN_ADD)
        self._lstore_attach_files.set_value(treeiter, self._COLUMN_ADD, not value)


    # Handler for sub page Tools
    def on_rbutton_tools_ddata_toggled(self, button):
        '''
        @brief   Tools; Signal Handler: on RadioButton "Dump Data" toggled
        @details
            Makes associated widgets sensitive.
        '''
        if button.get_active() == True:
            self._cbutton_tools_ddata_utf8.set_sensitive(True)
        else:
            self._cbutton_tools_ddata_utf8.set_sensitive(False)


    def on_rbutton_tools_ddfields_toggled(self, button):
        '''
        @brief   Tools; Signal Handler: on RadioButton "Dump Data Fields" toggled
        @details
            Makes associated widgets sensitive.
        '''
        if button.get_active() == True:
            self._cbutton_tools_ddfields_utf8.set_sensitive(True)
        else:
            self._cbutton_tools_ddfields_utf8.set_sensitive(False)


    def on_rbutton_tools_update_info_toggled(self, button):
        '''
        @brief   Tools; Signal Handler: on RadioButton "Update Info" toggled
        @details
            Makes associated widgets sensitive.
        '''
        if button.get_active() == True:
            self._cbutton_tools_update_info_utf8.set_sensitive(True)
            self._box_tools_update_info.set_sensitive(True)
        else:
            self._cbutton_tools_update_info_utf8.set_sensitive(False)
            self._box_tools_update_info.set_sensitive(False)


    def on_rbutton_tools_fform_toggled(self, rbutton):
        '''
        @brief   Tools; Signal Handler: on RadioButton "FillForm" toggled
        @details
            Makes associated widgets sensitive.
        '''
        if rbutton.get_active() == True:
            self._box_tools_fform_file.set_sensitive(True)
            self._box_tools_fform_options.set_sensitive(True)
        else:
            self._box_tools_fform_file.set_sensitive(False)
            self._box_tools_fform_options.set_sensitive(False)


    # Signal Handler for popover menu Restrictions
    def on_entry_rest_passwd_icon_pressed(self, entry, icon_pos, event):
        '''
        @brief Signal Handler for icon press events of restriction Password entries.
        @details
            A press on the primary entry icon, toggles the visibility of the text.
            One mode shows the password stared, the other in readable text.
            A press on the secondary entry icon, resets (deletes) the password.
        @par
            This signal hander is called by:
            - `entry_rest_passwd_user`
            - `entry_rest_passwd_owner`

        @param[in] entry    The object which received the signal
        @param[in] icon_pos The position of the clicked icon
        @param[in] event    The button press event _(not used)_
        '''
        if icon_pos == Gtk.EntryIconPosition.PRIMARY:
            visibility = entry.get_visibility()
            entry.set_visibility(not visibility)
            if entry.get_visibility() == True:
                entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "view-reveal-symbolic")
            else:
                entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "view-conceal-symbolic")
        elif icon_pos == Gtk.EntryIconPosition.SECONDARY:
            entry.set_text("")


    def on_rbutton_rest_enc_toggled(self, rbutton):
        '''
        @brief Signal Handler for toggle events of the encryption radio buttons.
        @details
            As soon as one of the two encryption algorithms is selected,
            the frame Permissions is made available (sensitive).
        @par
            This signal handler is called by:
            - `rbutton_rest_enc_none`
            - `rbutton_rest_enc_rc4_40bit`
            - `rbutton_rest_enc_rc4_128bit`

        @param[in] rbutton The object which received the signal _(not used)_
        '''
        if self._rbutton_rest_enc_none.get_active() == True:
            self._frame_rest_perm.set_sensitive(False)
        else:
            self._frame_rest_perm.set_sensitive(True)


    def on_cbutton_rest_perm_copy_contents_toggled(self, cbutton):
        '''
        @brief Signal Handler for toggle event of check button Copy Content.
        @details
            If Copy Content is allowed, Screen readers are also allowed.
            It is not possible to deselect screen readers
            if copying of content is allowed.
            Therefore, the Screen reader check box is also active
            as soon as Copy Content becomes active.
            It is then not possible to deactivate screen readers.
            Only if Copy Content is deactivated
            is it possible to deactivate screen readers.

        @see on_cbutton_rest_perm_modify_contents_toggled()
        @see on_cbutton_rest_perm_modify_annots_toggled()

        @param[in] cbutton The object which received the signal
        '''
        if cbutton.get_active() == True:
            self._cbutton_rest_perm_screen_readers.set_sensitive(False)
            self._cbutton_rest_perm_screen_readers.set_active(True)
        else:
            self._cbutton_rest_perm_screen_readers.set_sensitive(True)


    def on_cbutton_rest_perm_modify_contents_toggled(self, cbutton):
        '''
        @brief Signal Handler for toggle event of check button Modify Contents.
        @details
            If Modify Contents is allowed, Assembly Contents is also allowed.
            It is not possible to deny Assembly, when Modify Content is allowed.

        @see on_cbutton_rest_perm_copy_contents_toggled()
        @see on_cbutton_rest_perm_modify_annots_toggled()

        @param[in] cbutton The object which received the signal
        '''
        if cbutton.get_active() == True:
            self._cbutton_rest_perm_assembly_contents.set_sensitive(False)
            self._cbutton_rest_perm_assembly_contents.set_active(True)
        else:
            self._cbutton_rest_perm_assembly_contents.set_sensitive(True)


    def on_cbutton_rest_perm_modify_annots_toggled(self, cbutton):
        '''
        @brief Signal Handler for toggle event of check button Modify Annotations.
        @details
            If Modify Annotations is allowed, Fill In Annotations is also allowed.
            It is not possible to deny Fill In, when Modify Annotations is allowed.

        @see on_cbutton_rest_perm_copy_contents_toggled()
        @see on_cbutton_rest_perm_modify_contents_toggled()

        @param[in] cbutton The object which received the signal
        '''
        if cbutton.get_active() == True:
            self._cbutton_rest_perm_fill_in_annots.set_sensitive(False)
            self._cbutton_rest_perm_fill_in_annots.set_active(True)
        else:
            self._cbutton_rest_perm_fill_in_annots.set_sensitive(True)


    # Handler used by widgets from various sections
    def on_entry_rest_passwd_changed(self, editable):
        '''
        @brief Signal Handler: On entry Restrictions Password changed
        @details
            This handler is called for every single character
            entered in one the restriction password entries.
            It checks if the entered password does not contain any characters
            that do not correspond to the Latin-1 encoding.
            If it does, the entry is colored red (style class: "error").

        @param[in] editable The object which received the signal
        '''
        str_passwd = editable.get_text()
        if self._str_is_latin1_encoded(str_passwd) == True:
            editable.get_style_context().remove_class("error")
        else:
            editable.get_style_context().add_class("error")
            cli.debug_message("WARNING: illegal character in restriction password")
