#!/usr/bin/python3

# Copyright (C) 2020  Daniele Parmeggiani
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys


DEFAULT_BEGIN = ':SPOILERS BEGIN:'
DEFAULT_END = ':SPOILERS END:'


class DespoilerizerException(Exception):
    pass


class BeginTagInsideSpoilerBlock(DespoilerizerException):
    def __init__(self, line_no):
        self.line_no = line_no
        self.string = f'Found beginning of spoilers tag on line #{line_no} ' \
                      f'while already in a spoiler block.'
        super().__init__(self.string)


class EndTagOutsideSpoilerBlock(DespoilerizerException):
    def __init__(self, line_no):
        self.line_no = line_no
        self.string = f'Found ending of spoilers tag on line #{line_no} ' \
                      f'while outside of a spoiler block.'
        super().__init__(self.string)


def despoilerize(string, begin=DEFAULT_BEGIN, end=DEFAULT_END):
    result = []
    in_spoiler = False
    for i, line in enumerate(string.split('\n')):
        if line.find(begin) > -1:
            if in_spoiler:
                raise BeginTagInsideSpoilerBlock(i)
            else:
                in_spoiler = True
        elif line.find(end) > -1:
            if not in_spoiler:
                raise EndTagOutsideSpoilerBlock(i)
            else:
                in_spoiler = False
        else:
            if not in_spoiler:
                result.append(line)
            else:
                pass
    return '\n'.join(result)


def despoilerize_file(input_file, output_file, begin=DEFAULT_BEGIN, end=DEFAULT_END):
    despoilerized = despoilerize(input_file.read(), begin, end)
    output_file.write(despoilerized)


def despoilerize_stdin(begin=DEFAULT_BEGIN, end=DEFAULT_END):
    """
    Runs the `despoilerizer` function with `sys.stdin` as input and `sys.stdout`
    as output.
    """
    sys.stdout.write(
        despoilerize(sys.stdin.read(), begin=begin, end=end)
    )
