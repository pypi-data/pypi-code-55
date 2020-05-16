#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

""" mdtoc: Generates a table of contents for a markdown document in markdown.  """

# Include the argparse module to parse command line arguments and sys to get access to stdio.
import argparse
import sys
# Also include the needed library file.
import libmdtoc

__author__ = "Michael Connor Buchan"
__copyright__ = "Copyright (C) 2019-2020" + __author__
__credits__ = __author__
__license__ = "GPL-3.0-OR-LATER"
__version__ = "1.4.1"
__maintainer__ = __author__
__email__ = "mikeybuchan@hotmail.co.uk"
__status__ = "Production"

def main() -> int:
    # Create an ArgumentParser object to parse the command line arguments.
    arg_parser = argparse.ArgumentParser("MD TOC",
                                         description="""Generate a table of
                                         contents for a markdown document""",
                                         epilog="""Submit any bugs to
                                         https://github.com/mcb2003/md-toc-creator/issues/new"""
                                         )
    # This argument defines what file (default stdin) to read  the TOC from.
    arg_parser.add_argument("input",
                            help="The markdown file to read.",
                            type=argparse.FileType('r'),
                            default=sys.stdin,
                            nargs="?"
                            )
    # This argument defines the minimum heading level for which the indentation will be 0.
    # Headings at or below this level will not be indented.
    arg_parser.add_argument("-m", "--min-indent",
                            help="""Specify the minimum level of heading for
                            which the list items will be indented. Headings at or
                            below this level will not be indented and the rest
                            of the heading levels will be adjusted accordingly.
                            The default is 1.""",
                            type=int,
                            choices=range(1, 7),
                            default=1
                            )
    # This argument specifies the maximum level of heading for which the list
    # items will be indented.
    # Headings above this level will not be indented any further; Thus,
    # specifying 0 flattens the list.
    arg_parser.add_argument("-M", "--max-indent",
                            help="""Specify the maximum level of heading for
                            which the list items will be indented. Headings
                            above this level will not be indented any further;
                            Thus, specifying 0 flattens the list.
                            The default is 6.""",
                            type=int,
                            choices=range(0, 7),
                            default=6
                            )
    # This argument specifies whether to output the TOC items as links to their
    # sections or as simple plane text.
    arg_parser.add_argument("-n", "--no-links",
                            help="""Do not link the sections of the document to
                            their list items in the table of contents.""",
                            action="store_true"
                            )
    # This argument defines what file (default stdout) to write   the TOC to.
    arg_parser.add_argument("-o", "--output",
                            help="""The markdown file to write the table of
                            contents to. The default is standard output.""",
                            type=argparse.FileType('w'),
                            default=sys.stdout
                            )
    # This argument allows a different separator string to be defined.
    arg_parser.add_argument("-s", "--separator",
                            help="""Specifies a string to be used as the
                            separator between the '*' character and the
                            succeeding list item (default: ' ').""",
                            type=str,
                            default=" "
                            )
    # This argument allows a different whitespace string to be defined.
    arg_parser.add_argument("-w", "--whitespace",
                            help="""Specify the characters used as whitespace
                            before each item. This is repeated or omitted
                            depending on the indentation level of each item.
                            (default: '\t')""",
                            type=str,
                            default="\t"
                            )
    # This argument allows the exclusion of specific heading levels from the TOC.
    # It can be repeated to exclude multiple levels.
    arg_parser.add_argument("-x", "--exclude",
                            help="""Specify specific levels of heading to
                            exclude from the table of contents. This option can
                            be repeated to exclude multiple levels.""",
                            metavar="LEVEL",
                            type=int,
                            action="append",
                            default=[]
                            )

    # Parse the arguments passed to the script.
    args = arg_parser.parse_args()

    # Create an MDTOC object with the parsed options.
    tocobj: libmdtoc.MDTOC = libmdtoc.MDTOC(
        args.input, not args.no_links, args.min_indent, args.max_indent,
        args.exclude, args.whitespace, args.separator)
    # Get the text representing the contents and print it to the standard output
    # or the specified file.
    text: str = tocobj.get_toc()
    print(text, file=args.output)
    return 0

if __name__ == "__main__":
    main()
