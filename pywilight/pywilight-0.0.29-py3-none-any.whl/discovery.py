"""Module to discover WiLight devices."""
import logging
import requests

from . import ssdp
from .wilight_device.api.xsd import device as deviceParser
from .wilight_device import Device

_LOGGER = logging.getLogger(__name__)


MANUFACTURER = 'All Automacao Ltda'


def discover_devices(ssdp_st=None, max_devices=None,
                     match_serial=None,
                     rediscovery_enabled=True):
    """Find WiLight devices on the local network."""
    ssdp_st = ssdp_st or ssdp.ST
    ssdp_entries = ssdp.scan(ssdp_st, max_entries=max_devices,
                             match_serial=match_serial)

    wilights = []

    for entry in ssdp_entries:
        if entry.match_device_description(
                {'manufacturer': MANUFACTURER}):
            serialNumber = entry.description.get('device').get('serialNumber')
            device = device_from_description(
                description_url=entry.location, serialNumber=serialNumber,
                rediscovery_enabled=rediscovery_enabled)

            if device is not None:
                wilights.append(device)

    return wilights


def device_from_description(description_url, serialNumber, rediscovery_enabled=True):
    """Return object representing WiLight device running at host, else None."""
    xml = requests.get(description_url, timeout=10)
    mac = deviceParser.parseString(xml.content).device.macAddress
    model = deviceParser.parseString(xml.content).device.modelName
    serial_number = serialNumber or deviceParser.parseString(xml.content).device.serialNumber
    key = deviceParser.parseString(xml.content).device.modelNumber

    if serial_number is None:
        _LOGGER.debug(
            'No serial number was supplied or found in setup xml at: %s.',
            description_url)

    return wilight_from_model_serial_and_location(
        description_url, mac, model, serial_number, key,
        rediscovery_enabled=rediscovery_enabled)

def wilight_from_model_serial_and_location(location, mac, model, serial_number, key,
                                  rediscovery_enabled=True):
    """Create device class based on the device input data."""
    if mac is None:
        return None
    if model is None:
        return None
    if len(mac) < 17:
        return None
    if len(model) < 15:
        return None
    if serial_number is None:
        return None
    if len(serial_number) != 12:
        return None
    if location is None:
        return None
    host = location.split('/', 3)[2].split(':', 1)[0]
    type_mode = model.split(' ', 1)[1].split('-', 1)
    type = type_mode[0][0:4]
    swversion = type_mode[0][4:16]
    mode = type_mode[1]

    return Device(host=host, mac=mac, serial_number=serial_number, type=type,
                    swversion=swversion,mode=mode,
                    key=key, rediscovery_enabled=rediscovery_enabled)
