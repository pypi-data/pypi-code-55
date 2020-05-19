"""Lightweight Python module to discover and control WiLight devices."""
#from .wilight_device import Device as WiLightDevice  # noqa F401
from .discovery import discover_devices  # noqa F401
from .subscribe import SubscriptionRegistry  # noqa F401
