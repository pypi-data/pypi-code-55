import sys
import os
import re

import numpy as np


def extract_binary_matrices(filename):
    """Extract binary matrices (extent and intent) of output filename"""
    filename = os.path.abspath(filename)
    output_filename_extent = filename + '.binary_extent'
    output_filename_intent = filename + '.binary_intent'
    intent_str_to_int = {}
    intent_int_to_str = {}
    extents = []
    intents = []
    number_lines = 0
    number_columns = 0
    print('Reading:', filename)
    with open(filename, 'r') as f:
        for line in f.read().splitlines():
            regex_number_columns = re.match(r'# Number columns: (\d+)', line)
            if regex_number_columns:
                number_columns = int(regex_number_columns.group(1))

            regex_number_lines = re.match(r'# Number lines: (\d+)', line)
            if regex_number_lines:
                number_lines = int(regex_number_lines.group(1))

            line = re.sub('\s*#.*$', '', line)
            if not line:
                continue
            if 'Mandatory:' in line:
                continue
            if 'Non-mandatory:' in line:
                continue
            if 'Total:' in line:
                continue
            line = line.replace(' Mandatory', '')
            extent, intent = line.split(';')
            extent = extent.strip()
            intent = intent.strip()
            extents.append([int(val.strip()) for val in extent.split(',')])
            intents.append([int(val.strip()) for val in intent.split(',')])

    # Check if "# Number lines:" and "# Number columns:" are in output file
    if (number_lines == 0):
        print('No line "#Number lines: <nb lines>" found, try recalculating your concepts with a newer version',
              file=sys.stderr)
        sys.exit(1)

    if (number_columns == 0):
        print('No line "#Number columns: <nb lines>" found, try recalculating your concepts with a newer version',
              file=sys.stderr)
        sys.exit(1)

    # intent
    new_intents = []

    for intent in intents:
        print(intent)
        new_intent = []
        for i in range(1, number_columns + 1):
            if i in intent:
                new_intent.append('1')
            else:
                new_intent.append('0')

        new_intents.append(new_intent)

    np_intents = np.array(new_intents)

    with open(output_filename_intent, 'w') as f:
        for np_intent in np_intents:
            print(' '.join(np_intent))
            f.write(' '.join(np_intent) + '\n')

    print('Wrote intent binary matrice:', output_filename_intent)

    # extent
    new_extents = []

    for extent in extents:
        new_extent = []
        for i in range(1, number_lines + 1):
            if i in extent:
                new_extent.append('1')
            else:
                new_extent.append('0')

        new_extents.append(new_extent)

    np_extents = np.array(new_extents)
    np_extents = np_extents.transpose()

    with open(output_filename_extent, 'w') as f:
        for np_extent in np_extents:
            f.write(' '.join(np_extent) + '\n')

    print('Wrote extent binary matrice:', output_filename_extent)


if __name__ == '__main__':
    extract_binary_matrices('/home/toad/projects/quality_cover/backend/quality_covers_py_app/contexte.out')
