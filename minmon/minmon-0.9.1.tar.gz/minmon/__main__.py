#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
    minmon 0.9.1

MINimum MONitor - display on stdout: mem, swap, cpu, temp, disk i/o and net i/o

    1. date and time
    2. physical Memory % usage and Swap memory % usage
    3. Cpu % usage and cpu Temperature in °C 
    4. file system Read and Write rate in bytes/second
    5. network Download and Upload rate in bytes/second

Formats are:

    - 1: 'YYYY-mm-dd HH:MM:SS'
    - 2, 3: two 2-digit decimal numbers ('**' = 100) and a linear 0-100 graphic
    - 4, 5: two 5-digit human-readable numbers and a logarithmic 1-K-M-G-T graphic

As an example of 5-digit human-readable format, '10K50' means 11.50 * 1024 = 11776.

    - 'K' = 1024 ** 1 =             1,024
    - 'M' = 1024 ** 2 =         1,048,576
    - 'G' = 1024 ** 3 =     1,073,741,824
    - 'T' = 1024 ** 4 = 1,099,511,627,776

The program is minimalistic as it has a minimal memory (6 MB) and cpu footprint.

To stop the program press Ctrl-C.

Example:

    $ minmon -l log3.log # write on stdout and on ~/.minmon/log3.log
    YYYY-mm-dd HH:MM:SS M% S% 0 . . . .50 . . . 100 C% T° 0 . . . .50 . . . 100 R-B/s W-B/s 1 . . K . . M . . G . . T D-B/s U-B/s 1 . . K . . M . . G . . T
    2020-05-17 18:38:38 24  0 S────M────┼─────────┤  1 60 C─────────┼─T───────┤     0     0 X─────┼─────┼─────┼─────┤    52     0 U──D──┼─────┼─────┼─────┤
    2020-05-17 18:38:39 24  0 S . .M. . │ . . . . │  3 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:40 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │    52     0 U .D. │ . . │ . . │ . . │
    2020-05-17 18:38:41 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:42 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:43 24  0 S────M────┼─────────┤  4 58 ├C────────┼─T───────┤     0 10K50 R─────┼─W───┼─────┼─────┤     0     0 X─────┼─────┼─────┼─────┤
    2020-05-17 18:38:44 24  0 S . .M. . │ . . . . │  4 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:45 24  0 S . .M. . │ . . . . │  4 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:46 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │    52     0 U .D. │ . . │ . . │ . . │
    2020-05-17 18:38:47 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0 287K6 R . . │ . .W│ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:48 24  0 S────M────┼─────────┤  2 58 C─────────┼─T───────┤     0     0 X─────┼─────┼─────┼─────┤    52     0 U──D──┼─────┼─────┼─────┤
    2020-05-17 18:38:49 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:50 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    ^C
'''

from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from math import log
from os import makedirs
from os.path import expanduser, join as joinpath
from psutil import virtual_memory as mem, swap_memory as swap
from psutil import cpu_percent as cpu, sensors_temperatures as temp
from psutil import disk_io_counters as disk, net_io_counters as net
from sys import argv, exit
from time import localtime, sleep, time
from warnings import simplefilter

log1024 = log(1024.0)
head = ("YYYY-mm-dd HH:MM:SS M% S% 0 . . . .50 . . . 100 C% T° 0 . . . .50 . . . 100 "
    "R-B/s W-B/s 1 . . K . . M . . G . . T D-B/s U-B/s 1 . . K . . M . . G . . T")
path = expanduser("~/.minmon")

def now():
    'return current time in "YYYY-mm-dd HH:MM:SS" format'
    return '%04d-%02d-%02d %02d:%02d:%02d' % localtime()[:6]

def numlin(x):
    'display number for linear data'
    x = round(x)
    return ' 0' if x <= 0 else '**' if x >= 100 else '%2d' % x

def hislin(xx, cc, i):
    'display histogram for linear data'
    hh = list('├─────────┼─────────┤' if i % 5 == 2 else '│ . . . . │ . . . . │')
    for x, c in zip(xx, cc):
        j = max(0, min(20, round(0.2 * x)))
        hh[j] = 'X' if 'A' <= hh[j] <= 'Z' else c
    return ''.join(hh)
            
def numlog(x):
    'display number for logarithmic data'
    x = max(0, round(x))
    if x < 1024:
        return '%5d' % x
    for e, c in enumerate('KMGTPEZY'):
        if x < 1024 ** (e + 2):
            return (str(x / 1024 ** (e + 1)).replace('.', c) + '00000')[:5]
    return '*****'
    
def hislog(xx, cc, i):
    'display histogram for logarithmic data'
    hh = list('├─────┼─────┼─────┼─────┤' if i % 5 == 2 else '│ . . │ . . │ . . │ . . │')
    for x, c in zip(xx, cc):
        j = max(0, min(24, round(6.0 * log(max(1.0, x)) / log1024)))
        hh[j] = 'X' if 'A' <= hh[j] <= 'Z' else c
    return ''.join(hh)

def minmon_params(argv):
    "CLI arguments in argv -> dict of minmon() parameters"
    parser = Parser(prog="minmon", formatter_class=Formatter, description=__doc__)
    parser.add_argument("-V", "--version", action="version", version=__doc__.split("\n")[1].strip())
    parser.add_argument("-s","--sec", type=int, default=1, help="seconds between lines (integer >= 1, default: 1)")
    parser.add_argument("-l","--log", type=str, help=f"append lines into LOG logfile (default path: '~/.minmon')")
    class params: pass
    parser.parse_args(argv[1:], params)
    return {param: value for param, value in params.__dict__.items() if param[0] != "_"}

def minmon(sec=1, log=False):
    simplefilter('ignore')
    if sec < 1:
        exit(f"minmon: error: --sec is {sec} but can't be less than 1")
    print(head)
    makedirs(path, exist_ok=True)
    if log:
        if "/" not in log:
            log = joinpath(path, log)
        log_file = open(log, "a")
        print(head, file=log_file, flush=True)
    i, r0, w0, d0, u0, k0, k2 = 0, 0, 0, 0, 0, 0.0, sec
    while True:
        dk = k2 - k0
        k0 = time()
        i += 1
        s = swap().percent
        m = mem().percent
        c = cpu()
        t = max(x.current for xx in temp().values() for x in xx)
        r1 = disk().read_bytes;  r = max(0, r1 - r0) / dk; r0 = r1
        w1 = disk().write_bytes; w = max(0, w1 - w0) / dk; w0 = w1
        d1 = net().bytes_recv;   d = max(0, d1 - d0) / dk; d0 = d1
        u1 = net().bytes_sent;   u = max(0, u1 - u0) / dk; u0 = u1
        if i > 1:
            line = " ".join([now(),
                numlin(m), numlin(s), hislin([m, s], 'MS', i),
                numlin(c), numlin(t), hislin([c, t], 'CT', i),
                numlog(r), numlog(w), hislog([r, w], 'RW', i),
                numlog(d), numlog(u), hislog([d, u], 'DU', i)])
            print(line)
            if log:
                print(line, file=log_file, flush=True)
        k1 = time()
        sleep(sec - (k1 - k0))
        k2 = time()
            
def main():
    try:
        minmon(**minmon_params(argv))
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
