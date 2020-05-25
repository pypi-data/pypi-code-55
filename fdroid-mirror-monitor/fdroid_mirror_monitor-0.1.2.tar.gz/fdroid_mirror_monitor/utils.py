#!/usr/bin/env python3

# stdlibs:
from queue import Queue
import logging
import requests
import threading
# external:
import coloredlogs
import GeoIP


def parallelize(list_of_stuff, function_that_does_stuff, num_worker_threads=1):
    '''
    Parallelize a loop that iterates over a list and calls a function.

    :param list_of_stuff: (list of) parameter for the function call
    :param function_that_does_stuff: function that gets called with the corresponding parameter
    :param num_worker_threads: number of maximal threads in parallel
    :return: unsorted dict of parameter values with corresponding return value
    '''
    return_values = []
    parameter_values = []

    def worker(q):
        while not q.empty():
            stuff = q.get()
            threading.currentThread().name = stuff
            return_value = function_that_does_stuff(stuff)
            return_values.append(return_value)
            parameter_values.append(stuff)
            q.task_done()

    jobs = Queue()
    for stuff in list_of_stuff:
        jobs.put(stuff)

    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(jobs,))
        t.start()
    jobs.join()
    return dict(zip(parameter_values, return_values))


log_level = None


def get_logger(name=__name__, verbosity=None):
    '''
    Colored logging

    :param name: logger name (use __name__ variable)
    :param verbosity:
    :return: Logger
    '''
    global log_level
    if verbosity is not None:
        if log_level is None:
            log_level = verbosity
        else:
            raise RuntimeError('Verbosity has already been set.')

    shortname = name.replace('fdroid_mirror_monitor.', '')
    logger = logging.getLogger(shortname)

    # no logging of libs (and fix double logs because of fdroidserver)
    logger.propagate = False

    fmt = '%(asctime)s %(threadName)-48s %(name)-7s %(levelname)-8s %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S%z'

    fs = {'asctime':     {'color': 'green'},
          'hostname':    {'color': 'magenta'},
          'levelname':   {'color': 'red', 'bold': True},
          'name':        {'color': 'magenta'},
          'programname': {'color': 'cyan'},
          'username':    {'color': 'yellow'}}

    ls = {'critical':    {'color': 'red', 'bold': True},
          'debug':       {'color': 'green'},
          'error':       {'color': 'red'},
          'info':        {},
          'notice':      {'color': 'magenta'},
          'spam':        {'color': 'green', 'faint': True},
          'success':     {'color': 'green', 'bold': True},
          'verbose':     {'color': 'blue'},
          'warning':     {'color': 'yellow'}}

    coloredlogs.install(level=log_level, logger=logger, fmt=fmt,
                        datefmt=datefmt, level_styles=ls, field_styles=fs)

    return logger


def geoip(ip):
    '''
    :param ip: IPv4 or IPv4 address
    :return: touple of country_name and country_code
    '''
    if ':' in ip:
        # IPv6
        gi6 = GeoIP.open("/usr/share/GeoIP/GeoIPv6.dat", GeoIP.GEOIP_STANDARD)

        return gi6.country_name_by_addr_v6(ip), gi6.country_code_by_addr_v6(ip)

    else:
        # IPv4
        gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)

        return gi.country_name_by_addr(ip), gi.country_code_by_addr(ip)


def own_ip(timeout=60):
    r = requests.get('https://ident.me')

    try:
        r.raise_for_status()
    except Exception as e:
        log = get_logger(__name__)
        log.warning(str(e))
        log.error('Failed to get own ip from ident.me')

    return r.text
