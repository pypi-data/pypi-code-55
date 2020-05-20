#! /usr/bin/python

import os, sys
import csv
import argparse
import dicom_anonymiser.tools as anon
from pathlib import Path

from gooey import Gooey, GooeyParser


root = Path(os.path.abspath(__file__)).parent
tagpath = root / 'tags'
default_tagfile = tagpath / 'default_tags.csv'
default_tagfile_text = str(default_tagfile)

@Gooey(program_name='DICOM Anonymiser',
       required_cols=1,
       optional_cols=1,
       default_size=(610, 630))
def parse_args():
    # parser = argparse.ArgumentParser(description='Anonymise DICOM images')

    parser = GooeyParser(description='Anonymise DICOM images')

    parser.add_argument('source', type=str, metavar="Source",
                        widget="DirChooser",
                        help='location of dicom file or folder to anonymise')

    parser.add_argument('destination', type=str, metavar="Destination",
                        widget="DirChooser",
                        help='Destination folder to save anonymised images')

    parser.add_argument('-t', '--tagfile', default=default_tagfile_text, metavar="Tag file",
                        widget="FileChooser",
                        help='path to custom tags file')

    parser.add_argument('-i', '--intact', action="store_true", metavar="Intact",
                        help='Leave filenames unchanged')



    args = parser.parse_args()

    args.tagfile = Path(args.tagfile)
    args.source = Path(args.source)
    args.destination = Path(args.destination)

    if (args.source == args.destination) and (args.intact_filename):
        print('Source and destination are the same and filenames to be left intact. This will overwrite original files. Exiting.')
        sys.exit()
    return args


def tag_list(tagfile):
    data_elements = []
    with open(tagfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            data_elements.append(row)

    return anon.generate_tags(data_elements)


def file_rename(filename, keep_intact):
    if not keep_intact:
        return filename.replace('.dcm', '_anon.dcm', 1)
    else:
        return filename


def get_dest_filepath(src, src_root, dst_root):
    """
    This function will build the full abs path of the destination file
    :param src: The full abs path to the file to be anonymised
    :param src_root: The top level source directory
    :param dst_root: The top level destination directory
    :return: full destination file abs path
    """

    src_parts = list(src.parts)  # split the source into parts
    src_parts = src_parts[len(src_root.parts):]  # truncate the source root
    return Path(*list(dst_root.parts), *src_parts)  # add the destination root


def main():
    args = parse_args()
    my_tags = tag_list(args.tagfile)

    if args.source.is_dir():
        for root, dirs, files in os.walk(args.source):
            for file in files:
                source_filepath = Path(root) / file
                dest_filename = file_rename(file, args.intact)
                dest_filepath = get_dest_filepath(Path(root) / dest_filename, args.source, args.destination)
                anon.anonymise_file(source_filepath, dest_filepath, my_tags)
    else:
        file = file_rename(args.source.name, args.intact)
        dest_filepath = args.destination / file
        anon.anonymise_file(args.source, dest_filepath, my_tags)


if __name__ == '__main__':
    main()
