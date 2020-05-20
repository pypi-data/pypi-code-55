import logging
import os


TOKEN = None
"""API token"""

LOGGING_LEVEL = logging._levelToName[logging.ERROR]
"""Level that we should log at by default. """

LOG_FILE_PATH = os.path.join(os.path.expanduser("~"), ".qalx.log")
"""The path where log files will be stored.

 .. note::
    The default value is evaluated on our build system.
    Your default location will be ~/.qalx.log or %USERPROFILE%/.qalx.log"""

UNPACK_SET = True
"""
Should the items in a set be de-referenced when doing a `get` or `find_one` query?

.. note::
    Sets are not unpacked when doing a `find` query
"""

UNPACK_BLUEPRINT = True
"""Should the item blueprints in a set blueprint be de-referenced?"""

UNPACK_GROUP = False
"""
Should the sets in a group be de-referenced when doing a `get` or `find_one` query?

.. note::
    Groups are not unpacked when doing a `find` query
"""

MSG_BLACKOUTSECONDS = 30
"""
After this time in seconds the message will be returned to the queue if
it has not been deleted.

.. note::
    Workers automatically issue a heartbeat to the queue while the job is being
    processed to keep extending the blackout during processing
"""

MAX_RETRY_500 = 2
"""How many times should pyqalx retry the request when receiving a 5XX error
back from the API?"""
