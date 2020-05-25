""" Initializes Information subclasses. """
from tlnetcard_python.monitor.information.ups_properties import UpsProperties
from tlnetcard_python.monitor.information.battery_parameters import BatteryParameters
from tlnetcard_python.monitor.information.in_out_parameters import InOutParameters
from tlnetcard_python.monitor.information.identification import Identification
from tlnetcard_python.monitor.information.status_indication import StatusIndication
from tlnetcard_python.monitor.information.shutdown_agent import ShutdownAgent

# Functions which all classes share.
from tlnetcard_python.monitor.information.information import *
