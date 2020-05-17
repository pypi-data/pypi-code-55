"""This module contains patches for components used by AMNES."""

import threading

from Pyro5.api import Daemon
from Pyro5.api import config as pyro5_config
from Pyro5.svr_threads import Housekeeper

__LOCK = threading.Lock()


def __pyro5_housekeeper_init(self: Housekeeper, daemon: Daemon) -> None:
    super(Housekeeper, self).__init__(name="Pyro-Housekeeper")
    self.pyroDaemon = daemon
    self.stop = threading.Event()
    self.daemon = True
    self.waittime = min(
        pyro5_config.POLLTIMEOUT or 0, max(pyro5_config.COMMTIMEOUT or 0, 5)
    )


def patch() -> None:
    """Patch components used by AMNES.

    This method can only be called once.
    """
    __LOCK.acquire()
    Housekeeper.__init__ = __pyro5_housekeeper_init
