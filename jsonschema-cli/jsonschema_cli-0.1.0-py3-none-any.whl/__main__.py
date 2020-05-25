#!/usr/bin/env python3
from jsonschema_cli.main import main, create_parser, JsonschemaException
import jsonschema

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    try:
        main(args)
    except (jsonschema.ValidationError, JsonschemaException) as e:
        print(e)
