####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2019 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

__all__ = ['AstmSeam']

####################################################################################################

class AstmSeamClass:

    ##############################################

    def __init__(self, name):

        self._name = str(name)

    ##############################################

    @property
    def name(self):
        return self._name

####################################################################################################

class AstmSeam:

    ##############################################

    def __init__(self, seam_class, seam_type, number_of_rows):

        self._class = seam_class
        self._type = seam_type
        self._number_of_rows = number_of_rows

    ##############################################

    @property
    def name(self):
        return '{self._class}{self._type}-{self._number_of_rows}'.format(self)
