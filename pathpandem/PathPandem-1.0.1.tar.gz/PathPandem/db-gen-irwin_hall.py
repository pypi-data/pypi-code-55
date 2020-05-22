#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# This file is part of PathPandem.
#
# PathPandem is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PathPandem is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PathPandem.  If not, see <https://www.gnu.org/licenses/>.
'''Calculate Irwin Hall CDF for Various Thresholds and sums'''

from multiprocessing import Pool, cpu_count
from numpy.random import random_sample as nprandom
from datetime import datetime
from pickle import dump, load
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def anti_irwin_hall(sums: int=0, upbound: int=1, sampling=1000000)-> float:
    '''Calculate probability that 'sums' uniform variables
    bounded by 'upbound' sum up to *MORE* than 1
    '''
    return ((nprandom((sampling, sums))
                       * upbound).sum(axis=1) > 1).mean()


def worker(args)-> None:
    '''Parallel Worker'''
    dpi = args[0]
    cfr = args[1]
    return cfr, anti_irwin_hall(dpi, cfr)


def update_aih(indict, key1, key2, value)-> None:
    '''updates dict if key exists, else, appends to list'''
    if key1 in indict:
        if key2 in indict[key1]:
            return
        indict[key1][key2] = value
    else:
        indict[key1] = {key2: value}

def cli()-> tuple:
    '''Command line Interface'''
    parser = ArgumentParser(description="PreCaluclate IrwinHall Probabilities",
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-l", "--lower", type=int, default=1,
                        help="Lower Bound Infection Days (DPI) to start with")
    parser.add_argument("-u", "--upper", type=int, default=10,
                        help="Upper bound DPI to start with")
    parser.add_argument("-f", "--fname", default="reverse_cfr_database.pkl",
                        type=str, help="FileName of database")
    parser.add_argument("-p", "--parallel", default=0, type=int,
                        help="Number of parallel threads to use, all used if 0")
    args = parser.parse_args()
    return args.lower, args.upper, args.fname, args.parallel

if __name__ == "__main__":
    lower, upper, db_f_name, cpu = cli()
    aih_db = dict()
    if lower > upper:
        upper, lower = lower, upper
    if (not cpu) or cpu > cpu_count():
        cpu = cpu_count()
    pool = Pool(cpu)
    sampling = 1000000
    precision = 10/sampling
    try:
        db_file_h = open(db_f_name, "rb")
        aih_db = load(db_file_h)
        print("appending to pre_existing database")
        db_file_h.close()
        del db_file_h
    except:
        pass
    for dpi in range(lower,upper):
        if dpi in aih_db:
            print("%d-day results read from file" %dpi)
            continue
        print("Calculation for %d-day infection started at" %dpi,
                datetime.now())
        pool_h = pool.map_async(worker, [(dpi, cfr/1000)
                                         for cfr in range(0,1000)])
        res = pool_h.get()
        for args in res:
            cfr, cumul_fatality = args
            if precision < cumul_fatality % 1 < (1 - precision) :
                update_aih(aih_db, dpi, cumul_fatality, cfr)
    db_file_h = open(db_f_name, "wb")
    dump(aih_db, db_file_h)
    db_file_h.close()
    del pool
    exit()
