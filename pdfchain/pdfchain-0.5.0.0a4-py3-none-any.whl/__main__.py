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

"""
 @brief The Main Module.
 @details
    This module is called when starting the application
    by calling the directory or the ZIP package name.
"""

import sys

import pdfchain.app as app


def main():
    """
    @brief Starting the Application
    """
    application = app.Application()
    application.run(sys.argv)


if __name__ == "__main__":
    main()
