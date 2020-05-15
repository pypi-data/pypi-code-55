####################################################################################################
#
# Pyterate - Sphinx add-ons to create API documentation for Python projects
# Copyright (C) 2017 Fabrice Salvaire
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
#
####################################################################################################

####################################################################################################

import os
import re

####################################################################################################

init_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Pyterate', '__init__.py')
with open(init_path) as fh:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$", fh.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

####################################################################################################

def merge_include(src_lines, doc_path, included_rst_files=None):
    if included_rst_files is None:
        included_rst_files = {}
    text = ''
    for line in src_lines:
        if line.startswith('.. include::'):
            include_file_name = line.split('::')[-1].strip()
            if include_file_name not in included_rst_files:
                # print "include", include_file_name
                with open(os.path.join(doc_path, include_file_name)) as f:
                    included_rst_files[include_file_name] = True
                    text += merge_include(f.readlines(), doc_path, included_rst_files)
        else:
            text += line
    return text

####################################################################################################

# Utility function to read the README file.
# Used for the long_description.
def read_readme(file_name):

    source_path = os.path.dirname(os.path.realpath(__file__))
    if os.path.basename(source_path) == 'tools':
        source_path = os.path.dirname(source_path)
    elif 'build/bdist' in source_path:
        source_path = source_path[:source_path.find('build/bdist')]
    absolut_file_name = os.path.join(source_path, file_name)
    doc_path = os.path.join(source_path, 'doc', 'sphinx', 'source')

    # Read and merge includes
    with open(absolut_file_name) as f:
        lines = f.readlines()
    text = merge_include(lines, doc_path)

    return text

####################################################################################################

if not __file__.endswith('conf.py'):
    long_description = read_readme('README.txt')
else:
    long_description = ''

####################################################################################################

setup_dict = dict(
    name='Pyterate',
    version=version,
    author='Fabrice Salvaire',
    author_email='fabrice.salvaire@orange.fr',
    description='Pyterate is a Sphinx add-ons to generate API documentation using autogen and litterate programming documentation for Python projects.',
    license='GPLv3',
    keywords='sphinx autogen documentation generator builder literate programming',
    url='https://github.com/FabriceSalvaire/Pyterate',
    long_description=long_description,
)
