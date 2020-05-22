#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Application utilities

Created on   : 2019-12-11 ( Ergin Soysal )
Last modified: May 21, 2020, Thu 20:39:27 -0500
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import os.path

import json

import logging

LOG_FORMAT = '%(asctime)-15s %(levelname)-5s %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_SUFFIX = '%Y%m%d.log'


def _set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def write_json(obj, *name_parts, **kwargs):
    fname = os.path.join(*name_parts)
    with open(fname, 'w') as fp:
        json.dump(obj, fp, default=_set_default, **kwargs)


def read_json(*name_parts):
    fname = os.path.join(*name_parts)
    with open(fname) as fp:
        return json.load(fp)


def write(text, *name_parts):
    filename = os.path.join(*name_parts)
    with open(filename, 'w') as fp:
        fp.write(text)


def read(*name_parts):
    fname = os.path.join(*name_parts)
    with open(fname, 'r') as fp:
        return fp.read()


def _log(lvl, msg, *args, **kwargs):
    try:
        log.log(lvl, msg, *args, **kwargs)
    except:
        configure_default_logger()
        log.log(lvl, msg, *args, **kwargs)


def debug( msg, *args, **kwargs):
    _log(logging.DEBUG, msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    _log(logging.INFO, msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    _log(logging.WARNING, msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    _log(logging.ERROR, msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    _log(logging.CRITICAL, msg, *args, **kwargs)


def exception(msg, *args, exc_info=True, **kwargs):
    if 'log' not in globals():
        configure_default_logger()

    _log(logging.ERROR, msg, exc_info=exc_info, *args, **kwargs)


def configure_default_logger(level=LOG_LEVEL, format=LOG_FORMAT):
    global log

    logging.basicConfig(format=format, level=level)
    log = logging.getLogger()
    logging.debug("Configured logger at level %s to console", level)


def configure(args):
    config = _get_conf(args.cfgfile)
    _configure_log(config, args.log_section)

    log.info('Using configuration file: %s', args.cfgfile)
    log.debug(args)

    return config


def _configure_log_file(filename, formatter, level, suffix=LOG_SUFFIX):
    from logging.handlers import TimedRotatingFileHandler
    fh = TimedRotatingFileHandler(filename=filename, when='midnight', interval=1)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    fh.suffix = suffix

    return fh


def _configure_log_console(formatter, level):
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(level)

    return ch


def _configure_log(config, sec_name):
    global log

    if config and config.has_section(sec_name):
        log_conf = config[sec_name]
        appname = log_conf.get('name', None)
        level = log_conf.get('level', LOG_LEVEL)

        # format
        format = log_conf.get('format', LOG_FORMAT, raw=True)
        formatter = logging.Formatter(format)

        # the logger
        log = logging.getLogger(appname)
        log.setLevel(level)

        logfile = log_conf.get('filename', None)
        if logfile:
            suffix = log_conf.get('suffix', LOG_SUFFIX, raw=True)
            fh = _configure_log_file(logfile, formatter, level, suffix)
            log.addHandler(fh)
            log.info('Logging at level %s to file "%s"', level, logfile)

        ch_level = log_conf.get('con_level', None)
        if ch_level or not logfile:
            ch_level = ch_level or level
            ch = _configure_log_console(formatter, ch_level)
            log.addHandler(ch)

            log.info('Logging at level %s to console', ch_level)

        log.info('Log "%s" is configured using section "%s"', appname, sec_name)
    elif log is None:
        configure_default_logger()


def _get_conf(cfgfile):
    if os.path.exists(cfgfile):
        from configparser import ConfigParser, ExtendedInterpolation
        config = ConfigParser(os.environ, interpolation=ExtendedInterpolation())
        config.read(cfgfile)
        return config
    else:
        return None

