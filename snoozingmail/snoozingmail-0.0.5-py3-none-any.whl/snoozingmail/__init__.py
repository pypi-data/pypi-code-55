"""snoozingmail is a python3 wrapper around the gmail api.

The 'Snoozin' object is the primary interface to the api.
To perform actions further than the methods in the Snoozin
object, you can utilize the creds, modify, read and send
modules for more granular access to the gmail api.
"""

from .snoozin import Snoozin
from .gmail import creds, modify, read, send

__all__ = ['Snoozin', 'creds', 'modify', 'read', 'send']
