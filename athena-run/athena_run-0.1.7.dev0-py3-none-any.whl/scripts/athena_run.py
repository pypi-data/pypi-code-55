#!/usr/bin/env python
from __future__ import print_function

from distutils import spawn
import os
import sys
import logging

USAGE = """
Usage: athena-run <my_program>

Example: athena-run python main.py
"""

log = logging.getLogger(__name__)

def _root():
    return os.path.dirname(__file__)


def _add_bootstrap_to_pythonpath(bootstrap_dir):
    """
    Add our bootstrap directory to the head of $PYTHONPATH to ensure
    it is loaded before program code
    """
    python_path = os.environ.get('PYTHONPATH', '')

    if python_path:
        new_path = "%s%s%s" % (bootstrap_dir, os.path.pathsep,
                os.environ['PYTHONPATH'])
        os.environ['PYTHONPATH'] = new_path
    else:
        os.environ['PYTHONPATH'] = bootstrap_dir


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        return

    log.debug("sys.argv: %s", sys.argv)

    root_dir = _root()
    bootstrap_dir = os.path.join(root_dir, 'bootstrap')
    log.debug("athena bootstrap: %s", bootstrap_dir)

    _add_bootstrap_to_pythonpath(bootstrap_dir)
    log.debug("PYTHONPATH: %s", os.environ['PYTHONPATH'])
    log.debug("sys.path: %s", sys.path)

    executable = sys.argv[1]

    # Find the executable path
    executable = spawn.find_executable(executable)
    log.debug("program executable: %s", executable)

    if 'ATHENA_SERVICE_NAME' not in os.environ:
        # infer service name from program command-line
        service_name = os.path.basename(executable)
        os.environ['ATHENA_SERVICE_NAME'] = service_name

    os.execl(executable, executable, *sys.argv[2:])
