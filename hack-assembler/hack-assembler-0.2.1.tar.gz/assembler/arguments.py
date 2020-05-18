import argparse


def args_parser():
    parser = argparse.ArgumentParser(description='Generates hack machine binary code from symbolic form.')
    parser.add_argument('file', nargs='?', type=str, action='store',
                        help='File path with assembly code')

    parser.add_argument('--debug', default=False, action='store_true',
                        help='debug process of assembler')

    return parser.parse_args()
