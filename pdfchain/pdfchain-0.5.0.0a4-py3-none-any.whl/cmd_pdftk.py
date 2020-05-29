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
@brief PDFtk Command Strings.
@details
    Contains the PDF Toolkit command and options as constant strings.
@todo
    Implement the constant PDFTK as getter function
    and get the value from the preferences

@see <https://www.pdflabs.com/docs/pdftk-man-page/>
@see <https://www.pdflabs.com/docs/pdftk-cli-examples/>
"""


class PDFtk():
    """
    """

    __PDFTK = "/usr/bin/pdftk"

    # @property
    # def PDFTK():
    #     return PDFtk.__PDFTK

    @staticmethod
    def set_command(path):
        """
        """
        PDFtk.__PDFTK = path


    @staticmethod
    def get_command():
        """
        """
        return PDFtk.__PDFTK


    # General
    # PDFTK                 = "pdftk"  # Do not use this! Use the command from the preferences!
    OUTPUT                = "output"
    PASSWORD_INPUT        = "input_pw"

    # Cat and Shuffle
    CAT                   = "cat"
    SHUFFLE               = "shuffle"

    ID_KEEP               = ""
    ID_NEW                = ""
    ID_FIRST              = "keep_first_id" # ID of first PDF
    ID_FINAL              = "keep_final_id" # ID of final PDF

    ROTATION_NORTH        = "north"         #   0 deg
    ROTATION_EAST         = "east"          #  90 deg
    ROTATION_SOUTH        = "south"         # 180 deg
    ROTATION_WEST         = "west"          # 270 deg

    PAGES_ALL             = ""
    PAGES_EVEN            = "even"
    PAGES_ODD             = "odd"

    # Burst
    BURST                 = "burst"
    TEMPLATE              = "%0"            # Complete suffix example: "%04d.pdf"
    EXTENSION             = ".pdf"
    COUNT_OCT             = "o"
    COUNT_DEC             = "d"
    COUNT_HEX             = "x"

    # Watermark / Stamp
    BACKGROUND            = "background"
    BACKGROUND_MULTI      = "multibackground"
    STAMP                 = "stamp"
    STAMP_MULTI           = "multistamp"

    # Attachment
    ATTACH_FILES          = "attach_files"
    TO_PAGE               = "to_page"

    # Permissions
    ALLOW                 = "allow"
    FEATURES_ALL          = "AllFeatures"

    PRINTING              = "Printing"
    DEGRADED_PRINTING     = "DegradedPrinting"
    MODIFY_CONTENTS       = "ModifyContents"
    ASSEMBLY              = "Assembly"
    COPY_CONTENTS         = "CopyContents"
    SCREEN_READERS        = "ScreenReaders"
    MODIFY_ANNOTATIONS    = "ModifyAnnotations"
    FILL_IN               = "FillIn"

    PASSWORD_OWNER        = "owner_pw"
    PASSWORD_USER         = "user_pw"

    #ENCRYPT_NONE          = ""
    ENCRYPT_40BIT         = "encrypt_40bit"
    ENCRYPT_128BIT        = "encrypt_128bit"

    # Tools
    UNPACK_FILES          = "unpack_files"
    COMPRESS              = "compress"
    UNCOMPRESS            = "uncompress"
    DUMP_DATA_ANNOTS      = "dump_data_annots"
    DUMP_DATA_FIELDS      = "dump_data_fields"
    DUMP_DATA_FIELDS_UTF8 = "dump_data_fields_utf8"
    DUMP_DATA             = "dump_data"
    DUMP_DATA_UTF8        = "dump_data_utf8"
    UPDATE_INFO           = "update_info"
    UPDATE_INFO_UTF8      = "update_info_utf8"
    GENERATE_FDF          = "generate_fdf"
    FILL_FORM             = "fill_form"
    FLATTEN               = "flatten"
    NEED_APPEARANCES      = "need_appearances"
    DROP_XFA              = "drop_xfa"
