#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
import hashlib
import json
from datetime import datetime, timedelta
import requests
from xml.etree import cElementTree as ElementTree
from typing import NewType, Optional, Tuple, Iterable, List
import click

from bbbmon.xmldict import XmlListConfig, XmlDictConfig
from bbbmon.configuration import Config, Endpoint, SERVER_PROPERTIES_FILE, Url, Secret, get_user_config_path, init_config, new_config
import bbbmon.printing as printing






def generate_checksum(call_name: str, query_string: str, secret: Secret) -> str:
    """
    Generate Checksum for the request header (passed as value for `?checksum=`)
    """
    m = hashlib.sha1()
    m.update(call_name.encode('utf-8'))
    m.update(query_string.encode('utf-8'))
    m.update(secret.encode('utf-8'))
    return m.hexdigest()


def request_meetings(secret: Secret, bbb_url: Url, user_config_path: str) -> XmlDictConfig:
    """
    Make a getMeetings-API Call to the bbb instance and return a XmlDictConfig
    with the servers response
    """
    call_name = "getMeetings"
    checksum = generate_checksum(call_name, "", secret)
    url = "{}/api/{}?checksum={}".format(bbb_url, call_name, checksum)

    try:
        r = requests.get(url, timeout=3)
    except requests.exceptions.Timeout as e:
        # Offline Server!
        return XmlDictConfig({"meetings":None})
    except:
        # Offline Server!
        return XmlDictConfig({"meetings":None})

    try:
        root = ElementTree.XML(r.text)
    except ElementTree.ParseError as e:
        click.echo("{} The XML returned from {} couldn't be properly parsed. The response text from the Server was:\n{}".format(click.style('Error:', fg='red', bold=True), url, r.text))
        print("Exiting...")
        exit()

    xmldict = XmlDictConfig(root)
    if "returncode" in xmldict.keys():
        if xmldict['returncode'] == "FAILED":
            print(xmldict)
            exit()
    else:
        print(r.text)
        exit()
    return xmldict



def get_meetings(secret: Secret, bbb_url: Url, user_config_path: str) -> Iterable[XmlDictConfig]:
    """
    Request meetings and return a list of them. Sorted by biggest first
    """
    meetings = []
    try:
        d = request_meetings(secret, bbb_url, user_config_path)
    except:
        return ["unreachable"]

    if d["meetings"] is None:
        return []

    if type(d["meetings"]["meeting"]) is XmlListConfig:
        meetings = sorted([m for m in d["meetings"]["meeting"] if m["running"] == "true"], key=lambda x:int(x['participantCount']), reverse=True)
    elif type(d["meetings"]["meeting"]) is XmlDictConfig:
        meetings = [d["meetings"]["meeting"]]
    return meetings


def get_presenter(meeting: XmlDictConfig) -> Optional[XmlDictConfig]:
    """
    Get the presenter of a meeting (return None if there is none)
    """
    presenters = []
    if type(meeting["attendees"]) is str:
        presenters = [meeting["attendees"]]
    elif type(meeting["attendees"]["attendee"]) is XmlListConfig:
        presenters = [a for a in meeting["attendees"]["attendee"] if a["isPresenter"] == "true"]
    elif type(meeting["attendees"]["attendee"]) is XmlDictConfig:
        presenters = [meeting["attendees"]["attendee"]]
    
    if len(presenters) > 0:
        return presenters[0]
    else:
        return None


def get_duration(meeting: XmlDictConfig) -> timedelta:
    """
    Return the duration of a meeting
    """
    timestamp = int(meeting["startTime"][:-3])
    start_time = datetime.fromtimestamp(timestamp)
    duration = datetime.now() - start_time
    return duration


def list_meetings(config: Config, leaderboards: bool, n: int, participants: bool, presenter: bool, presenter_id: bool, show_meetings: bool, watch: int, fancy: bool, compact: bool):
    """
    For each endpoint in the configuration get the active meetings and print 
    out an overview of the current bbb-usage
    """

    # Request Meetings from API
    meetings = [get_meetings(e.secret, e.url, config.path) for e in config.endpoints]

    # Clear screen after request is done, and before printing new data to keep
    # blinking to a minimum
    if watch is not None:
        click.clear()


    for i, endpoint in enumerate(config.endpoints):
        meeting = meetings[i]

        # Print divider if there is more than one endpoint
        if i > 0:
            print()
            print("="*click.get_terminal_size()[0])
            print()

        if meeting[0] == "unreachable":
            printing.print_header(endpoint.name, "No connection..", fancy)
            continue

        # If there are no meetings, skip to next endpoint
        if len(meeting) == 0:
            if show_meetings:
                printing.print_header(endpoint.name, "MEETINGS", fancy)
                print("   └─── Currently no active meetings.")
            continue

        n_running = len(meeting)
        n_recording = len([m for m in meeting if m["recording"] == "true"])
        n_participants = sum([int(m["participantCount"]) for m in meeting])
        n_listeners = sum([int(m["listenerCount"]) for m in meeting])
        n_voice = sum([int(m["voiceParticipantCount"]) for m in meeting])
        n_video = sum([int(m["videoCount"]) for m in meeting])
        n_moderator = sum([int(m["moderatorCount"]) for m in meeting])

        if show_meetings and not compact:
            printing.print_header(endpoint.name, "MEETINGS", fancy)
            print("   ├─── {:>4} running".format(n_running))
            print("   └─── {:>4} recording".format(n_recording))
            print()

        if participants and not compact:
            printing.print_header(endpoint.name, "PARTICIPANTS across all {} rooms".format(n_running), fancy)
            print("   └─┬─ {:>4} total".format(n_participants))
            print("     ├─ {:>4} listening only".format(n_listeners))
            print("     ├─ {:>4} mic on".format(n_voice))
            print("     ├─ {:>4} video on".format(n_video))
            print("     └─ {:>4} moderators".format(n_moderator))

        if compact: 
            h1 = printing.format_header(endpoint.name, "MEETINGS", fancy) 
            h2 = printing.format_header("", "PARTICIPANTS across all {} rooms".format(n_running), fancy)
            s1 ="   ├─── {:>4} running  ".format(n_running)
            s2 ="   └─── {:>4} recording".format(n_recording)
            p1 ="   └─┬─ {:>4} total".format(n_participants)
            p2 ="     ├─ {:>4} listening only".format(n_listeners)
            p3 ="     ├─ {:>4} mic on".format(n_voice)
            p4 ="     ├─ {:>4} video on".format(n_video)
            p5 ="     └─ {:>4} moderators".format(n_moderator)
            print("{:<20}  {}".format(h1.rstrip(), h2))
            print("{:<22} {}".format(s1, p1))
            print("{:<22} {}".format(s2, p2))
            print("{:<22} {}".format("", p3))
            print("{:<22} {}".format("", p4))
            print("{:<22} {}".format("", p5))

        if leaderboards:
            print()
            printing.print_leaderboard(meeting, n, "participantCount", endpoint.name, presenter, presenter_id, fancy)
            printing.print_leaderboard(meeting, n, "videoCount", endpoint.name, presenter, presenter_id, fancy)
            printing.print_leaderboard(meeting, n, "voiceParticipantCount", endpoint.name, presenter, presenter_id, fancy)
            printing.print_duration_leaderboard(meeting, n, endpoint.name, presenter, presenter_id, fancy)



def meetings_twolines(config: Config, watch: int, fancy: bool):
    """
    For each endpoint in the configuration get the active meetings and print 
    out an overview of the current bbb-usage. This is guaranteed to fit within
    60 characters and two lines
    """

    # Request Meetings from API
    meetings = [get_meetings(e.secret, e.url, config.path) for e in config.endpoints]

    # Clear screen after request is done, and before printing new data to keep
    # blinking to a minimum
    if watch is not None:
        click.clear()

    for i, endpoint in enumerate(config.endpoints):
        meeting = meetings[i]

        # Print divider if there is more than one endpoint
        if i > 0:
            print("="*click.get_terminal_size()[0])

        # If there are no meetings, skip to next endpoint
        if len(meeting) == 0:
            lines = [
                "{:^60}".format("{}   there   are   currently  no   sessions.").format(endpoint.name[:3]),
                ""
            ]
            # Cut above 60 characters fill empty
            lines = ["{:<60}".format(l[:61]) for l in lines]
            lines = "\n".join(lines)
            print(lines)
            continue

        if meeting[0] == "unreachable":
            printing.print_header(endpoint.name, "No connection..", fancy)
            continue

        n_running = len(meeting)
        n_recording = len([m for m in meeting if m["recording"] == "true"])
        n_participants = sum([int(m["participantCount"]) for m in meeting])
        n_listeners = sum([int(m["listenerCount"]) for m in meeting])
        n_voice = sum([int(m["voiceParticipantCount"]) for m in meeting])
        n_video = sum([int(m["videoCount"]) for m in meeting])
        n_moderator = sum([int(m["moderatorCount"]) for m in meeting])
        avg_s = sum([int(get_duration(m).total_seconds()) for m in meeting])/float(n_running)
        avg_s = avg_s/60./60.

        if not fancy:
            if config.on_server:
                # If on server get load
                w = subprocess.run(["w | head -1"], shell=True, stdout=subprocess.PIPE)
                w = w.stdout.decode('utf-8').strip().split("load average:")
                if len(w) != 2:
                    w = 999.0
                else:
                    w = w[1].strip().split(" ")[0].rstrip(",")
                    try:
                        w = float(w.replace(",", "."))
                    except:
                        w =  666.0
                lines = [
                    "{}    rec / ses    ppl    mod   vid   mic  ear  lod".format(endpoint.name[:3]),
                    "stats   {:>2} /  {:<2}    {:>3}    {:>3}   {:>3}   {:>3}  {:>3}  {:.1f}"\
                    .format(n_recording, n_running, n_participants, n_moderator, n_video, n_voice, n_listeners, w)
                ]
            else:
                lines = [
                    "{}    rec / ses    ppl    mod   vid   mic  ear".format(endpoint.name[:3]),
                    "stats   {:>2} /  {:<2}    {:>3}    {:>3}   {:>3}   {:>3}  {:>3}"\
                    .format(n_recording, n_running, n_participants, n_moderator, n_video, n_voice, n_listeners)
                ]
        else:
            lines = [
                "{}: There are {} people in {} meetings for {:.1f}h on average"\
                .format(endpoint.name, n_participants, n_running, avg_s),
                "{} webcams and {} microphones are on. {} just listen. {} mods"\
                .format(n_video, n_voice, n_listeners, n_moderator)
            ]

        # Cut above 60 characters fill empty
        lines = ["{:^60}".format(l[:61]) for l in lines]
        lines = "\n".join(lines)
        print(lines)


def format_json(config: Config, watch: bool, compact: bool) -> str:
    meetings = [get_meetings(e.secret, e.url, config.path) for e in config.endpoints]

    # Clear screen after request is done, and before printing new data to keep
    # blinking to a minimum
    if watch is not None:
        click.clear()


    if compact:
        return str(json.dumps(meetings))
    else:
        return str(json.dumps(meetings, indent=4))
