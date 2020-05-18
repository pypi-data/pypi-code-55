#!/usr/bin/env python3
import os
from argparse import ArgumentParser

from termcolor import cprint

from pywiface import MonitorInterface, WirelessInterface

ENABLE = ('start', 'on', 'yes')
DISABLE = ('stop', 'off', 'no')
CHANNELS_2_4GHZ = list(range(11))
CHANNELS_5GHZ = [*range(32, 64, 2), 68, 96, *range(100, 128, 2), *range(132, 144, 2), *range(149, 161, 2), 165]


def handle_mon(args):
    if args.state in ENABLE:
        interface = MonitorInterface(name=args.interface)
        cprint("Enabled monitor mode on {}".format(interface.name), 'green')
    elif args.state in DISABLE:
        interface = WirelessInterface(name=args.interface)
        interface.set_managed_mode()
        cprint("Disabled monitor mode on {}".format(interface.name), 'green')


def handle_chan(args):
    interface = WirelessInterface(name=args.interface)
    interface.channel == args.channel
    cprint("Channel set to {} on {}".format(args.channel, interface.name), 'green')


def main():
    if os.getuid() != 0:
        cprint('Error: Must be run as root!', 'red')
        raise SystemExit

    parser = ArgumentParser(description="Manage wireless interfaces")
    subparsers = parser.add_subparsers(title="Commands")
    mon_parser = subparsers.add_parser('mon', help="Set/unset the interface's monitor mode.")
    mon_parser.add_argument('state', choices=ENABLE + DISABLE,
                            help="Whether to enable/disable monitor mode. Multiple synonyms supported.")
    mon_parser.set_defaults(func=handle_mon)
    chan_parser = subparsers.add_parser('chan', help="Manipulate the interface's channel.")
    chan_parser.add_argument('channel', choices=CHANNELS_2_4GHZ + CHANNELS_5GHZ,
                             type=int, help="Channel to set the interface to.")
    chan_parser.set_defaults(func=handle_chan)
    parser.add_argument('interface', help='The interface to operate on')

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
