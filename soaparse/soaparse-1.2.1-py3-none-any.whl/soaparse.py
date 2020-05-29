#!/usr/bin/env python3

class SOArecord:
    """
    https://www.ripe.net/publications/docs/ripe-203
    Just object for storing all fields, and parsed email
    """
    def __init__(self, mname, rname, email_parsed_last, email_parsed_first, serial, refresh, retry, expire, minimum):
        self.mname = mname

        self.rname = rname

        self.email_parsed_last = email_parsed_last
        self.email_parsed_first = email_parsed_first

        self.serial = serial

        self.refresh = refresh
        self.retry = retry
        self.expire = expire
        self.minimum = minimum


def soa_parse(authority_data):
    """parse out data fields in SOA and best guess email address to object"""
    soa_data = authority_data.split(" ")

    try:
        mname = soa_data[0][:-1]

        rname = soa_data[1][:-1]

        email_parsed_last = replace_second_from_last(".", rname, "@")
        email_parsed_first = rname.replace(".", "@", 1)

        serial = soa_data[2]

        refresh = soa_data[3]
        retry = soa_data[4]
        expire = soa_data[5]
        minimum = soa_data[6]

        return SOArecord(mname, rname, email_parsed_last, email_parsed_first, serial, refresh, retry, expire, minimum)

    except IndexError as e:
        print("error parsing SOA data field:\n" + repr(e))
        return None


def replace_second_from_last(char, string, replacement):
    """replace second from last occurence of char in string"""
    parts = string.rsplit(char, maxsplit=2)
    part1 = parts[0]

    new_string = part1 + replacement + char.join(parts[1:])
    return new_string
