#!/usr/bin/env python3
import sys

import jsonschema

from jsonschema_cli.args import create_parser
from jsonschema_cli.exceptions import JsonschemaCliException


def run():
    parser = create_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except (jsonschema.ValidationError, JsonschemaCliException) as e:
        print(e)
        sys.exit(1)
