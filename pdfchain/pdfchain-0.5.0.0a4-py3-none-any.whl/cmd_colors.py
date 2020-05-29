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
@brief Terminal Color Commands.
@details
    This module contains constant strings with the escape sequences
    for various colors and styles in the terminal.

@see <https://en.wikipedia.org/wiki/ANSI_escape_code#3/4_bit>
'''

__ESC       = '\033'

RESET     = __ESC + '[0m'
#BOLD      = __ESC + '[1m'
#FAINT     = __ESC + '[2m'
#ITALIC    = __ESC + '[3m'
#UNDERLINE = __ESC + '[4m'

#FG_BLACK          = __ESC + '[30m'
#FG_RED            = __ESC + '[31m'
#FG_GREEN          = __ESC + '[32m'
#FG_YELLOW         = __ESC + '[33m'
#FG_BLUE           = __ESC + '[34m'
#FG_MAGENTA        = __ESC + '[35m'
#FG_CYAN           = __ESC + '[36m'
#FG_WHITE          = __ESC + '[37m'
#FG_BRIGHT_BLACK   = __ESC + '[90m'
FG_BRIGHT_RED     = __ESC + '[91m'
FG_BRIGHT_GREEN   = __ESC + '[92m'
FG_BRIGHT_YELLOW  = __ESC + '[93m'
FG_BRIGHT_BLUE    = __ESC + '[94m'
FG_BRIGHT_MAGENTA = __ESC + '[95m'
FG_BRIGHT_CYAN    = __ESC + '[96m'
#FG_BRIGHT_WHITE   = __ESC + '[97m'

#BG_BLACK          = __ESC + '[40m'
#BG_RED            = __ESC + '[41m'
#BG_GREEN          = __ESC + '[42m'
#BG_YELLOW         = __ESC + '[43m'
#BG_BLUE           = __ESC + '[44m'
#BG_MAGENTA        = __ESC + '[45m'
#BG_CYAN           = __ESC + '[46m'
#BG_WHITE          = __ESC + '[47m'
#BG_BRIGHT_BLACK   = __ESC + '[100m'
#BG_BRIGHT_RED     = __ESC + '[101m'
#BG_BRIGHT_GREEN   = __ESC + '[102m'
#BG_BRIGHT_YELLOW  = __ESC + '[103m'
#BG_BRIGHT_BLUE    = __ESC + '[104m'
#BG_BRIGHT_MAGENTA = __ESC + '[105m'
#BG_BRIGHT_CYAN    = __ESC + '[106m'
#BG_BRIGHT_WHITE   = __ESC + '[107m'

