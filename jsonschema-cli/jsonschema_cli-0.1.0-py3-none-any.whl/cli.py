#!/usr/bin/env python3
from jsonschema_cli.main import main, create_parser
import jsonschema


def run():
    parser = create_parser()
    args = parser.parse_args()

    try:
        main(args)
    except jsonschema.ValidationError as e:
        print(e)
