#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from datetime import datetime, timedelta
from typing import NewType, Optional, Tuple, Iterable, List

from bbbmon.xmldict import XmlListConfig, XmlDictConfig
import bbbmon.meetings
from bbbmon.configuration import Config



# This is used as Leaderboard names
FRIENDLY_KEYNAMES = {
    "participantCount"      : "Participants",
    "listenerCount"         : "only listening",
    "voiceParticipantCount" : "Mics on",
    "videoCount"            : "Webcams on",
    "moderatorCount"        : "Number of Moderators"
}



def strfdelta(duration: timedelta) -> str:
    """
    Helper function for datetime.timedelta formatting, use like this:
    strfdelta(delta_obj, "{days} days {hours}:{minutes}:{seconds}")
    """
    s = int(duration.total_seconds())

    return '{:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60)


def format_duration(meeting: XmlDictConfig) -> str:
    """
    Helper functions for duration
    """
    duration = bbbmon.meetings.get_duration(meeting)
    return strfdelta(duration)



def get_formated_presenter_name_id(meeting: XmlDictConfig) -> str:
    """
    Get the formated name of the presenter for a given meeting (with id)
    """
    presenter = bbbmon.meetings.get_presenter(meeting)
    if presenter is not None:
        return "{:<30} ({})".format(presenter["fullName"], presenter["userID"])
    else:
        return "no Presenter"

def get_formated_presenter_name(meeting: XmlDictConfig) -> str:
    """
    Get the formated name of the presenter for a given meeting
    """
    presenter = bbbmon.meetings.get_presenter(meeting)
    if presenter is not None:
        return "{:<30}".format(presenter["fullName"])
    else:
        return "no Presenter"


def print_leaderboard(meetings: Iterable[XmlDictConfig], n: int, key: str, endpoint_name: str, presenter: bool, presenter_id: bool, fancy: bool):
    """
    Print a leaderboard of all meetings sorted by a given key (e.g. 
    participantCount)
    """
    if n==1:
        prefix = "Most"
    else:
        prefix = "By"
    # Stay on same line if n == 1
    print_header(endpoint_name, "{} {}".format(prefix, FRIENDLY_KEYNAMES[key]), fancy, n != 1)
    sorted_by = sorted([m for m in meetings], key=lambda x:int(x[key]), reverse=True)
    more = len(sorted_by[:n]) != len(sorted_by)
    if n != 1:
        for m in sorted_by[:n]:
            if presenter:
                if presenter_id:
                    print("{:>5} {:<45} {}".format(m[key], m["meetingName"], get_formated_presenter_name_id(m))) 
                else:
                    print("{:>5} {:<45} {}".format(m[key], m["meetingName"], get_formated_presenter_name(m))) 
            else:
                print("{:>5} {}".format(m[key], m["meetingName"]))
        if more:
            print("    {}".format("."*(len(sorted_by)-len(sorted_by[:n]))))
        print()
    else:
        m = sorted_by[0]
        if presenter:
            if presenter_id:
                print("{:>8} {:<45} {}".format(m[key], m["meetingName"], get_formated_presenter_name_id(m))) 
            else:
                print("{:>8} {:<45} {}".format(m[key], m["meetingName"], get_formated_presenter_name(m))) 
        else:
            print("{:>8} {}".format(m[key], m["meetingName"]))


def print_duration_leaderboard(meetings: Iterable[XmlDictConfig], n: int, endpoint_name: str, presenter: bool, presenter_id: bool, fancy: bool):
    """
    Print a leaderboard of all meetings sorted by a given key (e.g. 
    participantCount)
    """
    if n==1:
        prefix = "Most"
    else:
        prefix = "By"
    # Stay on same line if n == 1
    print_header(endpoint_name, "{} Duration".format(prefix, ), fancy, n != 1)
    by_duration = sorted([m for m in meetings], key=lambda x:int(bbbmon.meetings.get_duration(x).total_seconds()), reverse=True)
    more = len(by_duration[:n]) != len(by_duration)
    if n != 1:
        for m in by_duration[:n]:
            if presenter:
                if presenter_id:
                    print("{:>12} {:<38} {}".format(format_duration(m), m["meetingName"], get_formated_presenter_name_id(m))) 
                else:
                    print("{:>12} {:<38} {}".format(format_duration(m), m["meetingName"], get_formated_presenter_name(m))) 
            else:
                print("{:>12} {}".format(format_duration(m), m["meetingName"]))
        if more:
            print("    {}".format("."*(len(by_duration)-len(by_duration[:n]))))
        print()
    else:
        m = by_duration[0]
        if presenter:
            if presenter_id:
                print("{:>4} {:<45} {}".format(format_duration(m), m["meetingName"], get_formated_presenter_name_id(m))) 
            else:
                print("{:>4} {:<45} {}".format(format_duration(m), m["meetingName"], get_formated_presenter_name(m))) 
        else:
            print("{:>4} {}".format(format_duration(m), m["meetingName"]))


def print_header(endpoint_name: str, text: str, fancy=True, newline=True):
    """
    Print a section header
    """
    click.echo(format_header(endpoint_name, text, fancy), nl=newline)


def format_header(endpoint_name: str, text: str, fancy=True) -> str:
    """
    Format a header and return a string
    """
    if fancy:
        if len(endpoint_name) > 0:
            block = click.style("  [{}] {}  ".format(endpoint_name, text), fg='black', bg='white', bold=True)
        else:
            block = click.style("  {} {}  ".format(endpoint_name, text), fg='black', bg='white', bold=True)
    else:
        if len(endpoint_name) > 0:
            block = "[{}] {}".format(endpoint_name, text)
        else:
            block = "{} {}".format(endpoint_name, text)
    return "{}{}".format(block, " "*(20-len(endpoint_name+text)))