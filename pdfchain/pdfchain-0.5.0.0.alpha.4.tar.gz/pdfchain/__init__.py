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
PDF Chain is a graphical user interface for the PDF Toolkit (PDFtk).
The GUI supports all common features of the command line tool in a comfortable way.

PDF Chain generates a command for the PDF Toolkit from the GUI settings
and executes it on the system.
Therefore the PDF Toolkit must be already installed on the system.
"""

import datetime


__version__ = "0.5.0.0"
__author__ = "Martin Singer"
__author_email__ = "martin.singer@web.de"
__website_url__ = "pdfchain.sourceforge.net"
__license__ = "GPL v3+"
__copyright__ = u"Copyright \xa9 2009 - %d %s" % (datetime.date.today().year, __author__)


import gettext
import locale

import pdfchain.paths as paths


# def __init_translations():
#     """
#     @brief TODO
#     @details
#         TODO
#     """
#     print(__copyright__)
#
#     _GETTEXT_DOMAIN = "pdfchain"
#     _LOCALE_DIR = paths.get_locale_dir()
#
#     locale.setlocale(locale.LC_ALL, '')
#
#     for module in locale, gettext:
#         module.bindtextdomain(_GETTEXT_DOMAIN, _LOCALE_DIR)
#         module.textdomain(_GETTEXT_DOMAIN)
#
#
# __init_translations()
