import argparse


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="log to console", action="store_true")
    parser.add_argument("-s", "--safe", help="ask for confirmation before executing any operations", action="store_true")
    parser.add_argument("-c", "--configuration", help="re-input configuration values", action="store_true")
    parser.add_argument("-e", "--echo", help="echo configuration values", action="store_true")
    return parser.parse_args()