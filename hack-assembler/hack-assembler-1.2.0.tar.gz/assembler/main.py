import logging
from assembler.arguments import args_parser
from assembler.parser import parse
from assembler.code import assemble

_log = logging.getLogger(name=__name__)


def main():
    args = args_parser()

    if args.debug:
        level = getattr(logging, 'DEBUG', None)
    else:
        level = getattr(logging, 'INFO', None)

    logging.basicConfig(level=level)

    parsed_code = parse(args.file)
    _log.debug(f"parsed code: {parsed_code}")

    assembled_code = assemble(parsed_code, args.file, args.dry_run)
    _log.debug(f"assembled code: {assembled_code}")


if __name__ == '__main__':
    main()
