'''
Git Project Manager

Usage:
  gp -l | --list
  gp -n | --new
  gp -b | --bug
  gp -s | --show <id>
  gp -c | --close <id>
  gp -h | --help
  gp -v | --version

Options:
  -l --list     Show issues list from current Milestone
  -n --new     Create new issue without label
  -b --bug     Create new issue as bug
  -s --show     Show an issue specifying his ID
  -c --close     Close an issue specifying his ID
  -h --help     Show this screen.
  -v --version     Show version.
'''

import os
import sys
import yaml

import gitlab
from docopt import docopt
from github import Github

def main():
    arguments = docopt(__doc__)

    try:
        print(arguments)
    except KeyboardInterrupt:
        sys.exit("Exiting...")
    except Exception as e:
        print(e)