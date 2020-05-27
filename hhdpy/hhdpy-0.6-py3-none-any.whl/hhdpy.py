# -*- coding: utf-8 -*-

import sys
import argparse

USAGE = """
USAGE :
    python get_in_bw.py --url http://172.217.25.206/dl/android/studio/install/3.2.1.0/android-studio-ide-181.5056338-windows.exe
"""

def main(args):
    parser = argparse.ArgumentParser(
        epilog=USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--url", help="다운로드 속도측정 타겟 URL")
    options = parser.parse_args(args)

    print("hhd main options.url[{}]".format(options.url))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))