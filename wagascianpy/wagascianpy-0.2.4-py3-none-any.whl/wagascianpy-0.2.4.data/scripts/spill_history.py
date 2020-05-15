#!python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import argparse
import textwrap

import wagascianpy.plotting.plotter
import wagascianpy.utils.utils


def spill_history(plotter):
    plotter.template_plotter()


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description=textwrap.dedent('''\
                                     Produce spill history plots. If the stop time or stop run is not provided
                                      the present time or the last run are assumed. If both time and run number
                                      are provided the run number is preferred.'''))

    PARSER.add_argument('-f', '--wagasci-runs-dir', metavar='<WAGASCI runs directory>', dest='wagasci_runs_dir',
                        type=str, nargs=1, required=True, help=textwrap.dedent('''\
                        Path to the directory containing all the WAGASCI decoded runs.
                        '''))

    PARSER.add_argument('-d', '--wagasci-database', metavar='<WAGASCI run database>', dest='wagasci_database',
                        type=str, nargs=1, required=True, help=textwrap.dedent('''\
                        Path to the WAGASCI run database file. This file is created by the 
                        Wagasci Database Viewer (wagascidb_viewer.py) program and is usually called wagascidb.db.
                        '''))

    PARSER.add_argument('-b', '--bsd-database', metavar='<BSD database>', dest='bsd_database',
                        type=str, nargs=1, required=True, help=textwrap.dedent('''\
                        Path to the BSD database file. This file is created by the Wagasci Database Viewer
                         (wagascidb_viewer.py) program and is usually called bsddb.db.
                        '''))

    PARSER.add_argument('-g', '--bsd-files-dir', metavar='<BSD files directory>', dest='bsd_files_dir',
                        type=str, nargs=1, required=True, help=textwrap.dedent('''\
                        Path to the directory containing all the BSD root files.
                        '''))

    PARSER.add_argument('-at', '--start-time', metavar='<start time>', dest='start_time', type=str,
                        nargs=1, help='Start date and time in the format "%Y/%m/%d %H:%M:%S"', default=None,
                        required=False)

    PARSER.add_argument('-ot', '--stop-time', metavar='<stop time>', dest='stop_time', type=str,
                        nargs=1, help='Stop date and time in the format "%Y/%m/%d %H:%M:%S"', default=None,
                        required=False)

    PARSER.add_argument('-ar', '--start-run', metavar='<start run>', dest='start_run', type=int,
                        nargs=1, help='start run number', default=None, required=False)

    PARSER.add_argument('-or', '--stop-run', metavar='<stop run>', dest='stop_run', type=int,
                        nargs=1, help='Stop run number', default=None, required=False)

    PARSER.add_argument('-t', '--t2krun', metavar='<T2K run>', dest='t2krun', type=int,
                        nargs=1, help='T2K run number (default is 10)', default=10, required=False)

    PARSER.add_argument('-dp', '--delivered-pot', dest='delivered_pot', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the POT delivered by the beam line in the selected interval of time (or runs)'''))

    PARSER.add_argument('-ap', '--accumulated-pot', dest='accumulated_pot', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the POT accumulated by the WAGASCI detectors in the selected interval of time (or 
                        runs)'''))

    PARSER.add_argument('-bs', '--bsd-spill', dest='bsd_spill', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the BSD spill number in the selected interval of time (or runs)'''))

    PARSER.add_argument('-ws', '--wagasci-spill', dest='wagasci_spill', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the WAGASCI spill number in the selected interval of time (or runs)'''))

    PARSER.add_argument('-wfs', '--wagasci-fixed-spill', dest='wagasci_fixed_spill', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the WAGASCI fixed spill number in the selected interval of time (or runs)'''))

    PARSER.add_argument('-all', '--all', dest='all', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot all available plots are produced for the selected interval of time (or runs)'''))

    ARGS = PARSER.parse_args()

    if isinstance(ARGS.wagasci_runs_dir, list):
        ARGS.wagasci_runs_dir = ARGS.wagasci_runs_dir[0]
    WAGASCI_RUNS_DIR = ARGS.wagasci_runs_dir

    if isinstance(ARGS.wagasci_database, list):
        ARGS.wagasci_database = ARGS.wagasci_database[0]
    WAGASCI_DATABASE = ARGS.wagasci_database

    if isinstance(ARGS.bsd_database, list):
        ARGS.bsd_database = ARGS.bsd_database[0]
    BSD_DATABASE = ARGS.bsd_database

    if isinstance(ARGS.bsd_files_dir, list):
        ARGS.bsd_files_dir = ARGS.bsd_files_dir[0]
    BSD_FILES_DIR = ARGS.bsd_files_dir

    if isinstance(ARGS.start_time, list):
        ARGS.start_time = ARGS.start_time[0]
    START_TIME = ARGS.start_time

    if isinstance(ARGS.stop_time, list):
        ARGS.stop_time = ARGS.stop_time[0]
    STOP_TIME = ARGS.stop_time

    if isinstance(ARGS.start_run, list):
        ARGS.start_run = ARGS.start_run[0]
    START_RUN = ARGS.start_run

    if isinstance(ARGS.stop_run, list):
        ARGS.stop_run = ARGS.stop_run[0]
    STOP_RUN = ARGS.stop_run

    if isinstance(ARGS.t2krun, list):
        ARGS.t2krun = ARGS.t2krun[0]
    T2KRUN = ARGS.t2krun

    START = START_RUN if START_RUN else START_TIME
    STOP = STOP_RUN if STOP_RUN else STOP_TIME

    DELIVERED_POT = ARGS.delivered_pot
    ACCUMULATED_POT = ARGS.accumulated_pot
    BSD_SPILL = ARGS.bsd_spill
    WAGASCI_SPILL = ARGS.wagasci_spill
    WAGASCI_FIXED_SPILL = ARGS.wagasci_fixed_spill
    ALL = ARGS.all

    print(ARGS)

    if DELIVERED_POT or ALL:
        spill_history(wagascianpy.plotting.plotter.BsdPotPlotter(
            output_path="/home/neo/Desktop/test_bsd_pot_history.png",
            bsd_database=BSD_DATABASE,
            bsd_repository=BSD_FILES_DIR,
            wagasci_database=WAGASCI_DATABASE,
            t2krun=T2KRUN,
            start=START,
            stop=STOP))

    if ACCUMULATED_POT or ALL:
        spill_history(wagascianpy.plotting.plotter.WagasciPotPlotter(
            output_path="/home/neo/Desktop/test_wagasci_pot_history.png",
            bsd_database=BSD_DATABASE,
            bsd_repository=BSD_FILES_DIR,
            wagasci_database=WAGASCI_DATABASE,
            wagasci_repository=WAGASCI_RUNS_DIR,
            t2krun=T2KRUN,
            start=START,
            stop=STOP))

    if BSD_SPILL or ALL:
        spill_history(wagascianpy.plotting.plotter.BsdSpillPlotter(
            output_path="/home/neo/Desktop/test_bsd_spill_history.png",
            bsd_database=BSD_DATABASE,
            bsd_repository=BSD_FILES_DIR,
            wagasci_database=WAGASCI_DATABASE,
            t2krun=T2KRUN,
            start=START,
            stop=STOP))

    if WAGASCI_SPILL or ALL:
        spill_history(wagascianpy.plotting.plotter.WagasciSpillPlotter(
            output_path="/home/neo/Desktop/test_wagasci_spill_history.png",
            bsd_database=BSD_DATABASE,
            bsd_repository=BSD_FILES_DIR,
            wagasci_database=WAGASCI_DATABASE,
            wagasci_repository=WAGASCI_RUNS_DIR,
            t2krun=T2KRUN,
            start=START,
            stop=STOP))

    if WAGASCI_FIXED_SPILL or ALL:
        spill_history(wagascianpy.plotting.plotter.WagasciFixedSpillPlotter(
            output_path="/home/neo/Desktop/test_wagasci_fixed_spill_history.png",
            bsd_database=BSD_DATABASE,
            bsd_repository=BSD_FILES_DIR,
            wagasci_database=WAGASCI_DATABASE,
            wagasci_repository=WAGASCI_RUNS_DIR,
            t2krun=T2KRUN,
            start=START,
            stop=STOP))
