import argparse


def args_parser():
    parser = argparse.ArgumentParser(description='Generates hack machine binary code from symbolic form.')
    parser.add_argument('file', type=str, action='store',
                        help='File path with assembly code')

    parser.add_argument('--debug', default=False, action='store_true',
                        help='debug process of assembler')

    parser.add_argument('--dry-run', default=False, action='store_true',
                        help='Dry run assemble process. Useful with --debug')

    return parser.parse_args()
