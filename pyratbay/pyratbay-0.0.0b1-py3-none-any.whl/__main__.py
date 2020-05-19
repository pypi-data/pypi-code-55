#! /usr/bin/env python

# Copyright (c) 2016-2020 Patricio Cubillos.
# Pyrat Bay is open-source software under the GNU GPL-2.0 license (see LICENSE).

import argparse
import matplotlib
matplotlib.use('Agg')

import pyratbay as pb


def main():
    """
    Pyrat Bay: Python Radiative Transfer in a Bayesian framework
    """
    # Parse configuration file:
    parser = argparse.ArgumentParser(description=__doc__, add_help=True,
                  formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--version", action="version",
                       help="Show Pyrat Bay's version.",
                       version='Pyrat Bay version {:s}.'.format(pb.__version__))
    # Parse command-line args:
    args, unknown = parser.parse_known_args()


if __name__ == "__main__":
    matplotlib.pyplot.ioff()
    main()
