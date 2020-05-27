
from .lib.singleton import Singleton
from .lib.notify import Notify
from .lib.keyring import Keyring

from .config.resource import Resource
from .config.settings import Settings
from .config.cache import Cache

from .navigator.navigator import Navigator
from .navigator.fsNavigator import FSNavigator
from .navigator.kpNavigator import KPNavigator
from .navigator.kpEntryNavigator import KPEntryNavigator

def main():
	FSNavigator().open()
