# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas.motl@terkin.org>
# License: GNU Lesser General Public License, Version 3
import smbus
import struct


class PiUSV:
    """
    Driver for reading status flags and parameters from RPI USV+ Raspberry Pi - USV+.
    https://www.reichelt.de/raspberry-pi-usv-rpi-usv-p169883.html
    """

    status_definition = {
        'usb_power': 0x01,
        'external_power': 0x02,
        'battery_low': 0x04,
        'battery_charging': 0x08,
        'battery_full': 0x10,
        'button_s1': 0x20,
    }

    parameter_names = [
        'battery_voltage',
        'device_current',
        'device_voltage',
        'usb_voltage',
        'external_voltage',
    ]

    def __init__(self, bus):
        self.bus = bus
        self.address = 0x18

    def read(self):
        """
        Read both parameters and status flags and return as dictionary.
        """

        # Read parameters and status.
        status = self.read_status()
        parameters = self.read_parameters()

        # Merge parameters and status.
        data = {}
        data.update(parameters)
        data.update(status)
        return data

    def read_status(self):
        """
        Read and decode all status flags.
        """

        # Signal reading status flags.
        self.bus.write_byte(self.address, 0x00)

        # Read status byte.
        status_byte = self.bus.read_byte(self.address)

        # Decode status byte into dictionary with names.
        status = {}
        for status_name, status_mask in self.status_definition.items():
            status[status_name] = bool((status_byte & status_mask) == status_mask)

        return status

    def read_parameters(self):
        """
        Read and decode all parameters.
        ["U_Batt (V)", "I_Rasp (A)", "U_Rasp (V)", "U_USB  (V)", "U_ext  (V)"].
        """

        # Signal reading parameters.
        self.bus.write_byte(self.address, 0x02)

        # Read raw values into bytearray buffer.
        buffer = bytearray()
        for _ in range(10):
            item = self.bus.read_byte(self.address)
            buffer.append(item)

        # Decode binary data.
        # https://docs.python.org/3/library/struct.html
        values_raw = struct.unpack('>hhhhh', buffer)

        # Apply scaling.
        values = map(lambda x: x / 1000.0, values_raw)

        # Mix-in parameter names.
        data = dict(zip(self.parameter_names, values))

        return data

    def read_firmware_version(self):
        """
        Read firmware version.
        """

        # Signal reading firmware version.
        self.bus.write_byte(self.address, 0x01)

        # Read 12 characters.
        version = ''
        for _ in range(12):
            version += chr(self.bus.read_byte(self.address))

        return version


def main():
    bus = smbus.SMBus(1)

    # Patch status definition for old firmwares. Unklar!
    #PiUSV.status_definition['usb_power'] = 0x02
    #PiUSV.status_definition['external_power'] = 0x01

    piusv = PiUSV(bus)

    print('Firmware version:', piusv.read_firmware_version())
    print('Data:', piusv.read())


if __name__ == '__main__':
    main()
