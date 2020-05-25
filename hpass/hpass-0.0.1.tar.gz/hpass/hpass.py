import sys
import argparse
from colorama import init, Fore


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser(description='Hello Password')
    parser.add_argument('-v', '--version', help='查看版本信息', action='version', version='%(prog)s v0.0.1')


if __name__ == '__main__':
    main()
