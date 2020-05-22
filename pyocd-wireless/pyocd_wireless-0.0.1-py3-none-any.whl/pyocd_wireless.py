# -*- coding: utf-8 -*-
"""
CMSIS-DAP over Bluetooth LE Makerdiary DAP GATT Service (MDS)

Requirement:

    + pyocd
    + bleak - tested with Python 3.6, not support Python 3.8 yet
    
    `pip3 install pyocd pyocd bleak`
"""

import queue
import sys
import threading
import traceback

import asyncio
import bleak

from pyocd.probe.pydapaccess.interface.interface import Interface
from pyocd.probe.pydapaccess.dap_access_api import DAPAccessIntf
from pyocd.probe.pydapaccess.dap_access_cmsis_dap import DAPAccessCMSISDAP
from pyocd.probe.cmsis_dap_probe import CMSISDAPProbe
from pyocd.core.helpers import ConnectHelper
from pyocd.core.session import Session
from pyocd.__main__ import PyOCDTool

import logging

bleak._logger.setLevel(logging.WARNING)

# Makerdiary DAP GATT Service (MDS)
MDS_SERVICE_UUID = '0b1e0cd1-0000-6d61-6b65-726469617279'
MDS_RX_CHARACTERISTIC_UUID = '0b1e0cd2-0000-6d61-6b65-726469617279'
MDS_TX_CHARACTERISTIC_UUID = '0b1e0cd3-0000-6d61-6b65-726469617279'


class Executor:
    """In most cases, you can just use the 'execute' instance as a
    function, i.e. y = await execute(f, a, b, k=c) => run f(a, b, k=c) in
    the executor, assign result to y. The defaults can be changed, though,
    with your own instantiation of Executor, i.e. execute =
    Executor(nthreads=4)"""

    def __init__(self, loop, nthreads=1):
        from concurrent.futures import ThreadPoolExecutor
        self._ex = ThreadPoolExecutor(nthreads)
        self._loop = loop

    def __call__(self, f, *args, **kw):
        from functools import partial
        return self._loop.run_in_executor(self._ex, partial(f, *args, **kw))


async def ble_task(loop, interface):
    execute = Executor(loop)
    print('Connecting {}...'.format(interface.mac_address))
    async with bleak.BleakClient(interface.mac_address, loop=loop) as client:
        interface.connected = await client.is_connected()
        interface.connect_event.set()
        if not interface.connected:
            print('Failed to connect {}'.format(interface.mac_address))
            return
        print('Connected')

        max_packet_size = 525
        array = bytearray()

        def notification_handler(sender, data):
            # print(data)
            array.extend(data)
            if (len(data) < max_packet_size):
                # print('rx: {}'.format(list(array)))
                # print('rx {} bytes'.format(len(array)))
                interface.rx_queue.put(array.ljust(
                    interface.packet_size, b'\x00'))
                array.clear()

        await client.start_notify(MDS_TX_CHARACTERISTIC_UUID, notification_handler)
        while True:
            data = await execute(interface.tx_queue.get)
            if data is None:
                break

            # remove zero padding
            while len(data) > 1 and data[-1] == 0:
                data.pop()

            # print('tx: {}'.format(data))
            # print('tx {} bytes'.format(len(data)))
            for i in range(0, len(data), max_packet_size):
                await client.write_gatt_char(MDS_RX_CHARACTERISTIC_UUID, bytearray(data[i:i+max_packet_size]))
            if len(data) % max_packet_size == 0:
                # send an extra packet
                await client.write_gatt_char(MDS_RX_CHARACTERISTIC_UUID, b'\x00')
        await client.stop_notify(MDS_TX_CHARACTERISTIC_UUID)
        interface.connected = False


class BLE(Interface):
    """! @brief CMSIS-DAP BLE interface class using bleak for the backend.
    """

    def __init__(self, address=None):
        super(BLE, self).__init__()
        self.mac_address = address
        self.connected = False
        self.connect_event = threading.Event()
        self.rx_queue = queue.Queue()
        self.tx_queue = queue.Queue()
        self.thread = None
        self.packet_count = 64
        self.packet_size = 512

    def open(self):
        if not self.connected:
            self.connect_event.clear()
            self.thread = threading.Thread(target=self.task)
            self.thread.daemon = True
            self.thread.start()
            self.connect_event.wait()
            if not self.connected:
                raise DAPAccessIntf.DeviceError(
                    'Failed to connect the device {}'.format(self.mac_address))

    def task(self):
        try:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(ble_task(loop, self))
        except Exception:
            self.connect_event.set()
            traceback.print_exc()

    @staticmethod
    def get_all_connected_interfaces():
        return []

    def get_serial_number(self):
        return self.mac_address

    def set_packet_count(self, count):
        # print('packet count {}'.format(count))
        self.packet_count = count

    def set_packet_size(self, size):
        # print('packet size {}'.format(size))
        pass

    def write(self, data):
        self.tx_queue.put(data)

    def read(self):
        return self.rx_queue.get(timeout=3)

    def close(self):
        if self.connected:
            self.tx_queue.put(None)
            self.thread.join(timeout=3)
            self.thread = None


def session_with_wireless_probe(blocking=True, return_first=False, unique_id=None,
                                auto_open=True, options=None, **kwargs):

    if unique_id is None:
        print('Searching Bluetooth LE probes...')
        devices = asyncio.get_event_loop().run_until_complete(bleak.discover())
        devices = list(
            filter(lambda dev: MDS_SERVICE_UUID in dev.metadata['uuids'], devices))
        if len(devices) == 0:
            print('No found any Bluetooth LE probes')
            return
        elif len(devices) == 1:
            print('Found {} {}'.format(devices[0].address, devices[0].name))
            unique_id = devices[0].address
        else:
            print(' #  MAC                 RSSI  NAME')
            print('================================================')
            for i, dev in enumerate(devices):
                print(' {}) {}  {}    {}'.format(
                    i, dev.address, dev.rssi, dev.name))

            try:
                line = input("Enter the number of the device or 'q' to quit> ")
                if line.strip().lower() == 'q':
                    return
                n = int(line)
                unique_id = devices[n].address
            except Exception:
                traceback.print_exc()
                return

    interface = BLE(address=unique_id)
    daplink = DAPAccessCMSISDAP(None, interface=interface)
    probe = CMSISDAPProbe(daplink)
    return Session(probe, auto_open=auto_open, options=options, **kwargs)


def list_connected_probes():
    print('Searching Bluetooth LE probes...')
    devices = asyncio.get_event_loop().run_until_complete(bleak.discover())
    devices = list(
        filter(lambda dev: MDS_SERVICE_UUID in dev.metadata['uuids'], devices))
    if len(devices) == 0:
        print('No found any Bluetooth LE probes')
        return
    else:
        print(' #  MAC                 RSSI  NAME')
        print('================================================')
        for i, dev in enumerate(devices):
            print(' {}) {}  {}    {}'.format(
                i, dev.address, dev.rssi, dev.name))


# Monkey Patch
ConnectHelper.list_connected_probes = list_connected_probes
ConnectHelper.session_with_chosen_probe = session_with_wireless_probe


def main():
    sys.exit(PyOCDTool().run())


if __name__ == "__main__":
    main()
