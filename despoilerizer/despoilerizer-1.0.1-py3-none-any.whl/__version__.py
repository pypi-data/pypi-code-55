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


class Version:
    major = 1
    minor = 0
    patch = 1
    notes = ''
    string = '.'.join((str(major), str(minor), str(patch))) + notes

    @property
    def as_tuple(self):
        return (self.major, self.minor, self.patch, self.notes)

    @property
    def as_string(self):
        return '.'.join((str(self.major), str(self.minor), str(self.patch))) + \
               self.notes


__title__ = 'despoilerizer'
__description__ = 'Remove spoilers from files.'
__url__ = 'https://github.com/dpdani/despoilerizer'
__version__ = Version()
__author__ = 'Daniele Parmeggiani'
__author_email__ = 'git@danieleparmeggiani.me'
__license__ = 'GPLv3'
__copyright__ = 'Copyright (C) 2020 Daniele Parmeggiani'


__all__ = [
    '__title__',
    '__description__',
    '__url__',
    '__version__',
    '__author__',
    '__author_email__',
    '__license__',
    '__copyright__',
]
