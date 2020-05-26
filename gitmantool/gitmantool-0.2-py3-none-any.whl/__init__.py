'''
Git Manager Tool

Usage:
  gm -l | --list
  gm -n | --new
  gm -b | --bug
  gm -s | --show <id>
  gm -c | --close <id>
  gm -h | --help
  gm -v | --version

Options:
  -l --list     Show issues list from current Milestone
  -n --new     Create new issue without label
  -b --bug     Create new issue as bug
  -s --show     Show an issue specifying his ID
  -c --close     Close an issue specifying his ID
  -h --help     Show this screen.
  -v --version     Show version.
'''

import sys
from docopt import docopt

from .handler import run_handler


# ─── MAIN ───────────────────────────────────────────────────────────────────────

def main():
    arguments = docopt(__doc__)

    try:
        run_handler(arguments)
    except KeyboardInterrupt:
        sys.exit("Exiting...")
    except Exception as e:
        print(e)