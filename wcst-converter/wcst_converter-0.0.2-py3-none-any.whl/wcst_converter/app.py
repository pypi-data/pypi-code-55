import argparse
import sys
import os
import pandas as pd
import numpy as np
import re
import logging
import time
import collections


def find_input_files(input_dir):
    file_paths = []
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            file_paths.append(os.path.join(input_dir, file))
    return file_paths


def generate_column_map(contents):
    '''
    Find columns matching the format "{quantity} - {name}" and add or update column
    {name} with {quantity}.
    '''
    col_map = collections.OrderedDict()
    p = re.compile('^(\d) ?-? (.*)')
    for h in contents.head():
        match = p.match(h)
        if match is not None:
            logging.info('Found column to collapse: {}'.format(h))
            new_col = match.group(2)
            quantity = match.group(1)
            logging.info('Column: {}; Quantity: {}'.format(new_col, quantity))
            if col_map.get(h, None) is not None:
                raise AssertionError('Duplicate header found! {}'.format(h))

            col_map[h] = {
                'name': new_col,
                'quantity': int(quantity)
            }
    return col_map

def convert(file_path, output_path, delete_old_cols):
    print('Converting file {}'.format(file_path))
    filename = os.path.basename(file_path)
    with open(file_path) as f:
        contents = pd.read_csv(f)

    col_map = generate_column_map(contents)

    # For each column to collapse, add the new column if needed and increment quantity
    for c, map in col_map.items():
        logging.info('Collapsing column {}...'.format(c))
        col = contents[c]
        inc = col.notnull().astype(int) * map['quantity']

        # Determine if column already exists or if it needs to be added
        header = contents.head()
        if map['name'] not in header:
            logging.info('Mapped column doesn\'t exist, adding...')
            contents[map['name']] = inc
        else:
            logging.info('Mapped column already exists, adding new values...')
            contents[map['name']] += inc

    if delete_old_cols is True:
        # Remove outdated columns
        contents = contents.drop(columns=list(col_map.keys()))

    # Save the output CSV
    output_file_path = os.path.join(output_path, filename)
    contents.to_csv(output_file_path)
    print('Converted file saved as {}'.format(output_file_path))


def main():
    parser = argparse.ArgumentParser(
            description='Convert WCST reports to desired format')
    parser.add_argument(
            '-i', '--input',
            help='Path to the input directory containing CSV reports')
    #parser.add_argument(
    #        '-o', '--output',
    #        help='Path to the output directory where converted CSV files will be saved')
    parser.add_argument(
            '-d', '--delete-old-cols', action='store_true',
            help='Delete old columns')
    parser.add_argument(
            '-v', '--verbose', action='store_true',
            help='Print verbose logs')
    parser.add_argument(
            '-V', '--version', action='store_true',
            help='Print application version and exit')
    args = parser.parse_args()

    if args.version is True:
        print('wcst-converter: {}'.format('0.0.2'))
        exit(0)

    if args.input is None:
        raise ValueError('Input directory not provided!')

    if args.verbose is True:
        logging.basicConfig(level=logging.INFO)

    output_dir_name = 'converted-{}-({})'.format(time.strftime('%Y-%m-%d'), time.strftime('%H-%M-%S'))
    output_path = os.path.join(args.input, output_dir_name)
    os.mkdir(output_path)

    file_list = find_input_files(args.input)

    if not file_list:
        raise RuntimeError('No CSV files found in input directory')

    for f in file_list:
        convert(f, output_path, args.delete_old_cols)

    #except Exception as e:
    #    print('Encountered Error: ' + str(e))
    #    sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()