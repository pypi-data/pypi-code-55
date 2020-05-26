""" Callable app to manage the daemon.
"""

# Imports
import sys
import logging
from logging import config
from pkg_resources import resource_filename

# Third party
from zc.lockfile import LockError
from lab_utils.socket_comm import Client

# Local packages
from .Monitor import Monitor


def tpg_256a_pressure_monitor():
    """The main routine. It parses the input argument and acts accordingly."""

    # Either one of two options:
    # Start the server, if 'start' was given in the arguments, regardless of everything else
    if 'start' in sys.argv or len(sys.argv) < 2:
        # Setup logging
        logging.config.fileConfig(resource_filename(__name__, 'conf/logging.ini'))

        try:
            # Start the monitor
            mon = Monitor(config_file=resource_filename(__name__, 'conf/server.ini'))
            mon.handle.config(resource_filename(__name__, 'conf/tpg_256a.ini'))
            # mon.db.config(resource_filename(__name__, 'conf/database.ini'))
            mon.start_daemon()
        except LockError:
            logging.error('Daemon is probably running elsewhere')
            exit(1)
        else:
            exit(0)

    # Send a command (the arguments) to a running server
    else:
        try:
            # Start a client
            c = Client(config_file=resource_filename(__name__, 'conf/server.ini'))
            print('Opening connection to server on {h}:{p}'.format(
                h=c.host,
                p=c.port
            ))

            # Send message and get reply
            msg = ' '.join(sys.argv[1:])
            print('Sending message: ', msg)
            reply = c.send_message(msg)
            print(reply)
        except OSError as e:
            print('TCP Socket error! Maybe the server is not running?')
