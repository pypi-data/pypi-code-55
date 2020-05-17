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

from . import core
from .__version__ import *
import click
import sys


@click.command()
@click.option('-b', '--begin', default=':SPOILERS BEGIN:',
              help='Tag for beginning of spoilers.')
@click.option('-e', '--end', default=':SPOILERS END:',
              help='Tag for ending of spoilers.')
@click.option('-f', '--file', type=click.Path(),
              help='Read from file PATH instead of STDIN.')
@click.option('-o', '--output', type=click.Path(),
              help='Write to file PATH instead of STDOUT. '
                   'Only usable in conjunction with the -f option.')
def main(begin, end, file, output):
    if file is not None:
        with open(file, 'r') as fin:
            if output is not None:
                with open(output, 'w') as fout:
                    core.despoilerize_file(
                        input_file=fin, output_file=fout,
                        begin=begin, end=end
                    )
            else:
                core.despoilerize_file(
                    input_file=fin, output_file=sys.stdout,
                    begin=begin, end=end
                )
    else:
        core.despoilerize_stdin(begin=begin, end=end)
    return 0


main.__doc__ = f"""
{__title__} version {__version__.string}.

{__description__}
See README for example usages.

{__url__}

By {__author__} <{__author_email__}>.
""".strip()

main.help = main.__doc__


main()
