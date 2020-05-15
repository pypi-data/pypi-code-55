#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

""" Virtual database record class """

import abc
from datetime import datetime
import pytz

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


_DEFAULT_TIMEZONE = "Asia/Tokyo"


###########################################################################
#                                DBRecord                                 #
###########################################################################

class DBRecord(ABC):
    """Generic database record record"""

    timezone = _DEFAULT_TIMEZONE

    def __init__(self, record=None):

        if record is not None:
            for init_member, init_value in record.items():
                if init_member in self.list_fields():
                    setattr(self, init_member, init_value)

    def is_ready(self):
        """Return True if the make_record method is ready to be called on the object"""
        for member in dir(self):
            value = getattr(self, member)
            if not member.startswith('_') and not callable(value):
                if value is None:
                    print(member)
                    return False
        return True

    def set_timezone(self, timezone):
        """ Change the timezone (default timezone is Asia/Tokyo)"""
        self.timezone = timezone

    def make_record(self):
        """Return a dictionary containing the full record"""
        record = {}
        for member in dir(self):
            value = getattr(self, member)
            if not member.startswith('_') and not callable(value):
                if value is None:
                    raise ValueError("Field %s is not set" % member)
                else:
                    record[member] = getattr(self, member)
        return record

    def list_fields(self):
        """List all the field names of the record"""
        return list(
            filter(lambda member: not member.startswith('__') and not callable(getattr(self, member)), dir(self)))

    @classmethod
    def datetime2timestamp(cls, datetime_arg):
        """Convert from datetime string to timestamp
        """
        if isinstance(datetime_arg, datetime):
            try:
                timestamp = int(pytz.timezone(DBRecord.timezone).localize(datetime_arg).timestamp())
            except ValueError:
                timestamp = datetime_arg.timestamp()
            return timestamp
        elif isinstance(datetime_arg, str):
            try:
                time = pytz.timezone(DBRecord.timezone).localize(datetime.strptime(datetime_arg, "%Y/%m/%d %H:%M:%S"))
                return int(time.timestamp())
            except ValueError:
                time = datetime.strptime(datetime_arg, "%Y/%m/%d %H:%M:%S %Z")
            return int(time.timestamp())
        elif isinstance(datetime_arg, int):
            return datetime_arg
        else:
            raise ValueError("Datetime argument not recognized %s" % datetime_arg)

    @classmethod
    def timestamp2datetime(cls, posix_timestamp):
        """Convert from timestamp to datetime
        """
        utc_dt = datetime.utcfromtimestamp(posix_timestamp).replace(tzinfo=pytz.utc)
        return utc_dt.astimezone(pytz.timezone(DBRecord.timezone))

    @classmethod
    def timestamp2str(cls, posix_timestamp):
        """Convert from timestamp to human readable date string
        """
        utc_dt = datetime.utcfromtimestamp(posix_timestamp).replace(tzinfo=pytz.utc)
        return utc_dt.astimezone(pytz.timezone(DBRecord.timezone)).strftime('%Y/%m/%d %H:%M:%S %Z')

    @classmethod
    def str2datetime(cls, string):
        try:
            time = pytz.timezone(DBRecord.timezone).localize(datetime.strptime(string, "%Y/%m/%d %H:%M:%S"))
            return int(time.timestamp())
        except ValueError:
            time = datetime.strptime(string, "%Y/%m/%d %H:%M:%S %Z")
        return time

    def pretty_print(self):
        """Print the run record to standard output"""
        for member in dir(self):
            value = getattr(self, member)
            if not member.startswith('__') and not callable(value):
                print("%s : %s" % (member, str(value)))
