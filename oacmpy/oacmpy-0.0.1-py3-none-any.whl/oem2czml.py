# @author Joris OLYMPIO
#
import getopt
import glob
import os
import sys

from .ccsds import Oem
from .czml import OemToCzml, ScenarioCzml


def _ccsds2czml(oem_filename, output_filename, verbose, object_id=None):
    """ Write CZML file from OEM file """
    oem = []
    czml = []
    for file in glob.glob(oem_filename):
        if verbose:
            print("  File: ", file)

        filename, file_extension = os.path.splitext(file)
        fmt = file_extension.strip(".").upper()
        if fmt != "XML":
            fmt = "KVN"
        o = Oem.Oem(file, fmt)
        oem.append(o)
        czml.append(OemToCzml.OemAemToCzml(o))

    # take the random first satellite
    if not object_id:
        object_list = oem[0].get_satellite_list()
        object_id = list(object_list)[0]
    start = oem[0].get_start_time(object_id)
    end = oem[0].get_stop_time(object_id)
    if verbose:
        print(" Simulation time span: {} - {}".format(start, end))

    # Initialize a document
    scenario = ScenarioCzml.ScenarioCzml(start, end)
    for c in czml:
        scenario.add_content(c)
    scenario.create_document(output_filename)


def main(argv):
    help_str = "python -m ccsdz2czml <inputfile> -o <outputczmlfile>"

    try:
        opts, args = getopt.getopt(argv, "hvi:o:", ["oem=", "czml="])
    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)

    verbose = False
    inputfile = None
    outputfile = None
    for opt, arg in opts:
        if opt == "-h":
            print(help_str)
            sys.exit()
        if opt == "-v":
            verbose = True
        elif opt in ("-i", "--oem"):
            inputfile = arg
        elif opt in ("-o", "--czml"):
            outputfile = arg

    if not inputfile:
        print(help_str)
        sys.exit()

    if not outputfile:
        outputfile = inputfile[0] + ".czml"

    if verbose:
        print("Input File : {}".format(inputfile))
        print("Output File: " + outputfile)

    _ccsds2czml(inputfile, outputfile, verbose)


if __name__ == "__main__":
    main(sys.argv[1:])
