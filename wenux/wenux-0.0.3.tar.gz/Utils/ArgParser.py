import argparse
import os

class ArgParser(object):
    def __init__(self):
        pass

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="WAN Emulator for Linux")

        parser.add_argument(
            "-n", "--nic",
            choices=os.listdir("/sys/class/net"),
            metavar="interface",
            required=True,
            help="name of the network interface to be impaired"
        )

        direction = parser.add_mutually_exclusive_group(required=False)
        direction.add_argument(
            "--ingress",
            action="store_true",
            help="ingress interface impairment instead of egress"
        )
        direction.add_argument(
            "--bidirectional",
            action="store_true",
            help="bidirectional interface impairment (ingress+egress)"
        )

        parser.add_argument(
            "-i", "--include",
            action="append",
            default=["src=0/0", "src=::/0"],
            help="ip addresses and/or ports to be included in emulation "
                 " (example: --include src=ip,sport=portnum "
                 "--include dst=ip,dport=portnum)"
        )
        parser.add_argument(
            "-e", "--exclude",
            action="append",
            default=["dport=22", "sport=22"],
            help="ip addresses and/or ports to be excluded in emulation "
                 " (example: --exclude src=ip,sport=portnum "
                 "--exclude dst=ip,dport=portnum)"
        )

        parser.add_argument(
            "-d", "--debug",
            action="store_true",
            default=False,
            help="print out debug logging output"
        )

        subparsers = parser.add_subparsers(
            title="impairments",
            dest="subparser_name",
            description="list of available impairments",
            help="valid impairments"
        )

        netem_args = subparsers.add_parser("netem", help="manipulate netem attributes")

        netem_args.add_argument(
            "--loss_ratio",
            type=int,
            default=0,
            help="percentage of packets to be lost"
        )
        netem_args.add_argument(
            "--loss_corr",
            type=int,
            default=0,
            help="correlation factor for the random packet loss"
        )
        netem_args.add_argument(
            "--dupl_ratio",
            type=int,
            default=0,
            help="percentage of packets to be duplicated"
        )
        netem_args.add_argument(
            "--delay",
            type=int,
            default=0,
            help="overall delay for each packet in ms"
        )
        netem_args.add_argument(
            "--jitter",
            type=int,
            default=0,
            help="jitter in ms"
        )
        netem_args.add_argument(
            "--delay_jitter_corr",
            type=int,
            default=0,
            help="correlation factor for the random jitter"
        )
        netem_args.add_argument(
            "--reorder_ratio",
            type=int,
            default=0,
            help="percentage of packets to be reordered"
        )
        netem_args.add_argument(
            "--reorder_corr",
            type=int,
            default=0,
            help="correlation factor for the random reordering"
        )
        netem_args.add_argument(
            "--toggle",
            nargs="+",
            type=int,
            default=[1000000],
            help="toggles impairment on and off on specific intervals (example: "
                 "--toggle 10 3 5 2 will enable impairment for 10 s, turn it off "
                 "for 3 s, turn it on for 5 s, and turn it off for 2 s"
        )

        tbf_args = subparsers.add_parser("tbf", help="manipulate token bucket filter attributes")
        tbf_args.add_argument(
            "--limit",
            type=int,
            default=0,
            help="tbf limit in kb"
        )
        tbf_args.add_argument(
            "--burst",
            type=int,
            default=2000,
            help="amount of tokens in bucket available in bytes"
        )
        tbf_args.add_argument(
            "--latency",
            type=int,
            default=20,
            help="maximum time packets can stay queued before being dropped in ms"
        )
        tbf_args.add_argument(
            "--toggle",
            nargs="+",
            type=int,
            default=[1000000],
            help="toggles impairment on and off on specific intervals (example: "
                 "--toggle 10 3 5 2 will enable impairment for 10 s, turn it off "
                 "for 3 s, turn it on for 5 s, and turn it off for 2 s"
        )

        return parser.parse_args()