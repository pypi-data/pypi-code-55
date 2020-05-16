#!/usr/bin/python3
"""
    swapdf 0.9.2
    
SWAP PDF pages after scan of a two-sided sheet pack through a one-sided feeder.

Let's have a two-sided sheet pack we want scan through a one-sided feeder. Then:

    - we open the scan utility, namely simple-scan
    - we click the "All Pages From Feeder" option
    - we scan all odd pages
    - then we put again the pack upside down in the feeder
    - we scan all even pages
    - finally we save our pages in a file, say scanned.pdf

Now scanned.pdf contains odd pages in ascending order, followed by even pages in
descending order.

For instance, say our sheets are 4, so our pages are 8, and scanned.pdf contains
the pages:

    1 3 5 7 8 6 4 2
    
We issue at terminal:

    $ swapdf scanned.pdf mydoc.pdf
    'scanned.pdf' -> 8 pages -> 'mydoc.pdf'

Now mydoc.pdf contains the pages:

    1 2 3 4 5 6 7 8

in the right order.
"""

from os.path import isfile
from sys import argv, exit
from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from pdfrw import PdfReader, PdfWriter

def swapdf_params(argv):
    "CLI arguments in argv -> dict of swapdf() parameters"
    parser = Parser(prog="swapdf", formatter_class=Formatter, description=__doc__)
    parser.add_argument("-V", "--version", action="version", version=__doc__.split("\n")[1].strip())
    parser.add_argument("input_file", help="pages from scanner 1 3 5 ... 6 4 2")
    parser.add_argument("output_file", help="swapped pages 1 2 3 4 5 6 ...")
    class params: pass
    parser.parse_args(argv[1:], params)
    return {param: value for param, value in params.__dict__.items() if param[0] != "_"}

def swapdf(input_file, output_file):
    "SWAP PDF pages after scan of a two-sided sheet pack through a one-sided feeder"
    if not input_file.endswith(".pdf"):
        exit(f"swapdf: error: input file {input_file!r} has no '.pdf' extension")
    if not output_file.endswith(".pdf"):
        exit(f"swapdf: error: output file {output_file!r} has no '.pdf' extension")
    if not isfile(input_file):
        exit(f"swapdf: error: input file {input_file!r} not found")
    try:
        pages = PdfReader(input_file).pages
        assert pages
    except:
        exit(f"swapdf: error: input file {input_file!r} doesn't contain any pages")
    n = len(pages)
    if n % 2:
        exit(f"swapdf: error: pages in input file {input_file!r} must be even but they are {n}")
    writer = PdfWriter()
    for j in range(n // 2):
        writer.addpage(pages[j]) # odd page
        writer.addpage(pages[-j-1]) # even page
    try:
        writer.write(output_file)
    except:
        exit(f"swapdf: error writing output file {output_file!r}")
    print(f"{input_file!r} --> {n} pages --> {output_file!r}")

def main():
    try:
        swapdf(**swapdf_params(argv))
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
