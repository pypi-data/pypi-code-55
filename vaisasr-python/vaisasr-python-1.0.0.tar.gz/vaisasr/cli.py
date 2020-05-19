#!/usr/bin/env python3
"""Example usage of vaisasr by implementing a CLI."""

import argparse
import json
import logging
import ssl
import sys
from vaisasr import client
from vaisasr import __version__
import asyncio
import os
from pathlib import Path


def get_version():
    return __version__
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # path = Path(dir_path)
    # return open(os.path.join(path.parent, "VERSION")).read().strip()

LOGGER = logging.getLogger(__name__)


def get_log_level(verbosity):
    """
    Returns the appropriate log level given a verbosity level.

    Args:
        verbosity (int): Verbosity level.

    Returns:
        int: The logging level (e.g. logging.INFO).

    Raises:
        SystemExit: If the given verbosity level is invalid.
    """
    try:
        log_level = {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG}[verbosity]

        return log_level
    except KeyError as error:
        key = int(str(error))
        raise SystemExit(
            f"Only supports 2 log levels eg. -vv, you are asking for "
            f"-{'v' * key}"
        )


def main(args=None):
    if not args:
        args = vars(parse_args())
    logging.basicConfig(level=get_log_level(args["verbose"]))
    LOGGER.info("Args: %s", args)

    client.API_KEY = args["api_key"]
    if args["command"] == "transcribe":
        if args["bucket"] and args["key"]:
            audio = client.create_audio(os.path.basename(args["key"]), args["audio_source_id"], args["bucket"], args["key"])
        else:
            audio = client.upload_file(args["file"], audiosource_id=args["audio_source_id"])
        err, message = audio
        if err:
            raise Exception(message)
        audio = message
        output = asyncio.get_event_loop().run_until_complete(client.monitor_status(audio["id"]))
        result = client.get_plugin_result(audio['id'], args["plugin_code"])
        print(result)
    elif args["command"] == "list-source":
        for s in client.list_source():
            print(s["id"], s["name"])
    elif args["command"] == "list-api":
        for s in client.list_apis():
            print(s)
    elif args["command"] == "login":
        client.login(args["email"], args["password"])
    elif args["command"] == "version":
        print(get_version())
    elif args["command"] == "audio":
        result = client.get_plugin_result(args['audio_id'], args["plugin_code"])
        open(args["output"], "w").write(json.dumps(result))


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="CLI for VAIS Asr products.")
    parser.add_argument(
        "-v",
        dest="verbose",
        action="count",
        default=0,
        help=(
            "Set the log level for verbose logs. "
            "The number of flags indicate the level, eg. "
            "-v is INFO and -vv is DEBUG."
        ),
    )

    parser.add_argument(
        "--api-key",
        type=str,
        required=False,
        default="",
        help="API key",
    )

    subparsers = parser.add_subparsers(title='Commands', dest='command')

    version_subparser = subparsers.add_parser(
        "version",
        help="Get version code"
    )

    api_subparser = subparsers.add_parser(
        "list-api",
        help="List api keys"
    )

    transcribe_subparser = subparsers.add_parser(
        "transcribe",
        help="Transcribe one or more audio file(s)"
    )

    audio_subparser = subparsers.add_parser(
        "audio",
        help="Operators on a single audio"
    )

    source_subparser = subparsers.add_parser(
        "list-source",
        help="List all audio source"
    )

    login_subparser = subparsers.add_parser(
        "login",
        help="Login"
    )

    login_subparser.add_argument(
        "--email",
        required=True,
        help="Email"
            )

    login_subparser.add_argument(
        "--password",
        required=True,
        help="Password"
            )

    audio_subparser.add_argument(
        "--audio-id",
        default=False
            )

    audio_subparser.add_argument(
        "--plugin-code",
        type=str,
        default="all",
        help="Get data only for this plugin code",
    )

    audio_subparser.add_argument(
        "--output",
        type=str,
        help="Output file",
    )

    transcribe_subparser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help=(
            "Prints useful symbols to represent the messages on the wire. "
            "Symbols are printed to STDERR, use only when STDOUT is "
            "redirected to a file."
        ),
    )

    transcribe_subparser.add_argument(
        "--audio-source-id",
        type=str,
        required=False,
        default="",
        help="Audio source id",
    )

    transcribe_subparser.add_argument(
        "--output",
        type=str,
        default="",
        help="Write text result to file",
    )

    transcribe_subparser.add_argument(
        "--bucket",
        type=str,
        default="",
        help="Bucket",
    )

    transcribe_subparser.add_argument(
        "--key",
        type=str,
        default="",
        help="Key",
    )

    transcribe_subparser.add_argument(
        "--url",
        type=str,
        default="https://vaisapis.vais.vn/analytic",
        help="Server URL (e.g. https://vaisapis.vais.vn/analytic)",
    )

    transcribe_subparser.add_argument(
        "--file", metavar="FILEPATH", type=str,
        help="File to process"
    )

    transcribe_subparser.add_argument(
        "--plugin-code",
        type=str,
        default="all",
        help="Get data only for this plugin code",
    )

    return parser.parse_args(args=args)


if __name__ == '__main__':
    main()
