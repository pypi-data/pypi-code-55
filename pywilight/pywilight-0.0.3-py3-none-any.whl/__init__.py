"""Lightweight Python module to discover and control WiLight devices."""
from .protocol import create_wilight_connection # noqa F401

#from .wilight_device import Device as WiLightDevice  # noqa F401
from .discovery import discover_devices  # noqa F401
from .subscribe import SubscriptionRegistry  # noqa F401
