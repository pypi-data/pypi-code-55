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


import os
import re # RegEx parser

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#import pdfchain.strings as strings
import pdfchain.cmd_colors as color


'''
 @brief   Command Line Interface
 @details
    This module contains functions for outputs on the Command Line Interface (CLI).
'''


STR_NAME = "pdfchain"


def init(str_name):
    '''
    @brief Initializes this module.
    @details
        - sets the global program name variable, used for the CLI messages

    @param[in] str_name The program name string
    '''
    global STR_NAME
    STR_NAME = str_name


def debug_message(str_message):
    '''
    @brief Prints debug messages to the command line.
    @details
        Only calls the `cli.message` function with the `Gtk.MessageType.OTHER`,
        which will be interpreted and printed as "DEBUG" message.

    @param[in] str_message The message string
    '''
    message(Gtk.MessageType.OTHER, str_message)


def message(message_type, str_message):
    '''
    @brief Prints colored user messages to the command line.
    @details
        This function is called when a Gtk.InfoBar message appears.
        It prints the message with the leading program name
        and a colored message type indicator to the command line.

    @par Message Types
        - `Gtk.MessageType.INFO`     --> "INFO"
        - `Gtk.MessageType.WARNING`  --> "WARNING"
        - `Gtk.MessageType.QUESTION` --> "QUESTION"
        - `Gtk.MessageType.ERROR`    --> "ERROR"
        - `Gtk.MessageType.OTHER`    --> "DEBUG"

    @see window.AppWindowHandler._infobar_message()

    @param[in] message_type The `Gtk.MessageType`
    @param[in] str_message  The message string
    '''
    if message_type is Gtk.MessageType.INFO:
        str_type = color.FG_BRIGHT_BLUE + r"INFO" + color.RESET
    elif message_type is Gtk.MessageType.WARNING:
        str_type = color.FG_BRIGHT_YELLOW + r"WARNING" + color.RESET
    elif message_type is Gtk.MessageType.QUESTION:
        str_type = color.FG_BRIGHT_GREEN + r"QUESTION" + color.RESET
    elif message_type is Gtk.MessageType.ERROR:
        str_type = color.FG_BRIGHT_RED + r"ERROR" + color.RESET
    elif message_type is Gtk.MessageType.OTHER:
        str_type = color.FG_BRIGHT_MAGENTA + r"DEBUG" + color.RESET
    else:
        pass # write unknown messages without type indicator to the command line

    if str_type:
        str_type += ": "

    str_output = STR_NAME + ": " + str_type + str_message
    print(str_output)


def help():
    '''
    @brief Print program usage informations.
    @details
        Print informations about the program options to standard output.

    @TODO Command line options are not implemented yet!
    @TODO Get some strings from the UI (app name, ...) and build system (version, ...)
    '''
    print("""\
        NAME
            pdfchain - a graphical user interface for the PDF Toolkit

        SYNOPSIS
            pdfchain [OPTION]... [FILE]...

        DESCRIPTION
            Manages PDF documents easy for processing with the `pdftk` command line program.

            Mandatory arguments to long options are mandatory for short options too.

            -p --path=PATH    Path to document file or directory
    """)


def execute(str_command):
    '''
    @brief Execute the PDFtk command.
    @details
        Execute the command with `os.system()` function.

    @TODO Run the command execution in a separate Vte.Terminal() widget thread

    @return     The PDFtk error code
    @retval   0 Everything worked fine
    @retval 256 sh: pdftk: command not found
    @retval 768 pdftk: input PDF is not an acroform, so its fields were not filled
    '''
    print("{}".format(str_command))
    exit_code = os.system(str_command)
    return exit_code
