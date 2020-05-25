from __future__ import unicode_literals

import glob
import os
import shutil
import subprocess
import time
import codecs


def find_metadata_file():
    """Return path to the first found 'metadata.txt'

    Will look into current folder and one subdirectory deeper.
    """
    path = glob.glob('metadata.txt')
    path += glob.glob('*/metadata.txt')
    if len(path) == 1:
        if 'qgisMinimumVersion' in codecs.open(path[0], 'r', 'utf-8').read():
            return path[0]
    elif len(path) > 1:
        print("Multiple 'metadata.txt files have been found: %s" % path)
        print("Using the first found file: %s" % path[0])
        if 'qgisMinimumVersion' in codecs.open(path[0], 'r', 'utf-8').read():
            return path[0]


def create_zipfile(context):
    """This is the actual zest.releaser entry point

    Relevant items in the context dict:

    name
        Name of the project being released

    tagdir
        Directory where the tag checkout is placed (*if* a tag
        checkout has been made)

    version
        Version we're releasing

    workingdir
        Original working directory

    """
    metadata_file = find_metadata_file()
    if not metadata_file:
        return
    # Create a zipfile.
    subprocess.call(['make', 'zip'])
    for zipfile in glob.glob('*.zip'):
        first_part = zipfile.split('.')[0]
        new_name = "%s.%s.zip" % (first_part, context['version'])
        target = os.path.join(context['workingdir'], new_name)
        shutil.copy(zipfile, target)
        print("Copied %s to %s" % (zipfile, target))


def fix_version(context):
    """Fix the version in metadata.txt

    Relevant context dict item for both prerelease and postrelease:
    ``new_version``.

    """
    metadata_file = find_metadata_file()
    if not metadata_file:
        return
    lines = codecs.open(metadata_file, 'rU', 'utf-8').readlines()
    for index, line in enumerate(lines):
        if line.startswith('version'):
            new_line = 'version=%s\n' % context['new_version']
            lines[index] = new_line
    time.sleep(1)
    codecs.open(metadata_file, 'w', 'utf-8').writelines(lines)
