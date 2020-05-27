'''
Console memory reader and interpreter
'''


import importlib
import json
import logging as log
import threading
import websockets

from ..config import CONFIG

from . import addresses
from .exceptions import AutotrackerException, NoConnection, ParseError, NoDevice
from .items import ITEMS

gui = importlib.import_module(
    '..{0:s}.autotracker'.format(CONFIG['gui']), package=__package__)

CONNECTED = threading.Event()
DEVICES = {''}

__all__ = 'CONNECTED', 'DEVICES', 'MemoryReader'


class MemoryReader(object):
    '''
    Console memory reader

    Instance variables:
        device: currently connected device
        socket: websocket object
    '''

    def __init__(self):
        '''
        No arguments
        '''

        self.device = ''
        self.socket = None

    async def connect(self) -> None:
        '''
        Establish connection with USB2SNES server.

        Raises:
            NoConnection, ParseError: on failure
        '''

        log.info("Connecting autotracker to server '%s'.",
                 CONFIG['usb2snes_server'])
        asyncio = importlib.import_module('asyncio')
        serveraddr = (
            'ws://{0:s}'.format(CONFIG['usb2snes_server'])
            if not CONFIG['usb2snes_server'].startswith('ws://')
            else CONFIG['usb2snes_server'])
        try:
            self.socket = await asyncio.wait_for(websockets.connect(
                serveraddr, ping_timeout=None, ping_interval=None), 1)
        except (websockets.InvalidURI, websockets.InvalidHandshake) as err:
            CONNECTED.clear()
            log.error('Received %s: %s', type(err), str(err))
            raise NoConnection() from err
        except asyncio.TimeoutError as err:
            CONNECTED.clear()
            log.error('Connection attempt timed out.')
            raise NoConnection() from err
        log.debug('Connection successful.')

        try:
            devices = await self._retrieve_devices()
        except AutotrackerException:
            await self.disconnect()
            raise

        if not CONFIG['usb2snes_device']:
            if devices:
                gui.set_info(
                    'Connected to server. Please specify device in settings.',
                    'info')
            else:
                gui.set_info(
                    'Connected to server. Could not find any devices.',
                    'error')
            await self.disconnect()
            raise NoDevice()

        try:
            await self._choose_device(CONFIG['usb2snes_device'])
        except NoDevice:
            gui.set_info(
                "Connected to server. Could not find device '{0:s}'.".format(
                    CONFIG['usb2snes_device']),
                'error')
            await self.disconnect()
            raise
        except AutotrackerException:
            await self.disconnect()
            raise

    async def disconnect(self) -> None:
        '''
        Close connection with USB2SNES server.
        '''

        CONNECTED.clear()
        self.device = ''
        try:
            await self.socket.close()
        except AttributeError:
            pass
        else:
            self.socket = None

    async def _reconnect(self) -> None:
        '''
        Re-establish connection.

        Raises:
            NoConnection, ParseError: on failure
        '''

        await self.disconnect()
        await self.connect()

    async def _retrieve_devices(self) -> list:
        '''
        Retrieve devices found by USB2SNES.

        Returns:
            list: list of devices
        Raises:
            NoConnection: if connection to server failed
            ParseError: if server reply was not understood
        '''

        log.debug('Retrieving available devices.')
        ret = await self._send('DeviceList')
        log.debug('Found devices: %s', str(ret))
        DEVICES.clear()
        DEVICES.add('')
        DEVICES.update(ret)
        return ret

    async def _choose_device(self, device: str) -> None:
        '''
        Select device to use as tracker source.

        Args:
            device: device identifier, taken from self._retrieve_devices()
        Raises:
            NoConnection: if connection to server failed
            ParseError: if server reply was not understood
            NoDevice: if chosen device could not be found
        '''

        devices = await self._retrieve_devices()
        for dev in devices:
            if device.upper() in dev.upper():
                device = dev
                break
        else:
            log.error("Could not find device '%s'.", device)
            raise NoDevice("Could not find device '{0:s}'.".format(device))
        log.info("Connecting to device '%s'.", device)
        await self._send('Attach', [device], noreply=True)
        deviceinfo = await self._send('Info')
        if not deviceinfo:
            raise NoDevice(
                "Could not attach to device '{0:s}'.".format(device))
        log.info('Connection established.')
        self.device = device
        CONNECTED.set()

    async def _send(self, query: str, args: object = None,
                    noreply: bool = False, hexreply: bool = False) -> object:
        '''
        Send message to server.

        Args:
            query: query to send to server
            args: query argument(s)
            noreply: if True, don't expect reply from server
            hexreply: if True, expect server reply as raw hex
        Returns:
            object: reply from server
        Raises:
            NoConnection: if server connection failed
        '''

        sendobject = {'Opcode': query, 'Space': 'SNES'}
        if args:
            sendobject['Operands'] = args
        log.debug('Send: %s', str(sendobject))
        await self.socket.send(json.dumps(sendobject))
        if noreply:
            return
        try:
            reply = await self.socket.recv()
        except websockets.ConnectionClosed as err:
            log.debug('Connection closed unexpectedly.')
            raise NoConnection() from err
        try:
            reply = json.loads(reply)
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError) as err:
            if not hexreply:
                log.debug('Malformed reply: %s', reply)
                raise NoConnection() from err
        log.debug('Received: %s', str(reply))
        if hexreply:
            ret = reply
        else:
            try:
                ret = reply['Results']
            except KeyError:
                log.debug('Missing reply: %s', reply)
                raise ParseError()
        return ret

    async def _read_memory(self, address: int, length: int) -> bytearray:
        '''
        Read console memory.

        Args:
            address: address of first byte to read
            length: number of bytes to read
        Returns:
            bytearray: memory content
        '''

        ret = await self._send(
            'GetAddress', [hex(address), hex(length)], hexreply=True)
        return ret

    async def check_game_status(self) -> bool:
        '''
        Check whether game is running.

        Returns:
            bool: True if game is running and ready for memory access
        '''

        log.debug('Checking game status.')
        ret = await self._read_memory(*addresses.GAMEMODE)
        ingame = int.from_bytes(ret, 'big')
        log.debug('Game mode: %x', ingame)
        if ingame in (0x07, 0x09, 0x0b, 0x0e):
            return True
        return False

    async def check_items(self) -> dict:
        '''
        Retrieve items currently in Link's possession.

        Returns:
            dict: {'item identifier': stepping}
        '''

        log.debug('Checking items.')
        itemmem = await self._read_memory(*addresses.ITEMS)
        ret = {}
        for item in ITEMS:
            log.debug("Item '%s'", item)
            ret[item] = _parse_item(itemmem, ITEMS[item])
        return ret


def _parse_item(memory: bytearray, condition: object, sub: bool = False) -> int:
    '''
    Parse entry from autotracker.items.ITEMS.

    Args:
        memory: CPU memory banks from 7ef340 to 7ef3b9
        condition: member of autotracker.items.ITEMS
        sub: if True, is subcheck
    Returns:
        int: highest fulfilled item stepping
    '''

    def soffset(a):
        return a - 0x340
    if isinstance(condition, int):
        log.debug('Exists: %x:%x -> %d', condition, memory[soffset(condition)],
                  int(bool(memory[soffset(condition)])))
        return int(bool(memory[soffset(condition)]))
    if isinstance(condition, dict):
        dictionary = condition
        address = None
        check = True
    else:
        address, dictionary = condition
        log.debug('Exists: %x:%x -> %d', address, memory[soffset(address)],
                  int(bool(memory[soffset(address)])))
        if not sub:
            check = bool(memory[soffset(address)])
        else:
            check = True
    if check and 'flag' in dictionary:
        log.debug(
            'Flag: %x:%x & %x == %x -> %d', dictionary['flag'][0],
            memory[soffset(dictionary['flag'][0])], dictionary['flag'][1],
            memory[soffset(dictionary['flag'][0])] & dictionary['flag'][1],
            ((memory[soffset(dictionary['flag'][0])] & dictionary['flag'][1])
             == dictionary['flag'][1]))
        check = (
            (memory[soffset(dictionary['flag'][0])] & dictionary['flag'][1])
            == dictionary['flag'][1])
    if check and 'is' in dictionary:
        assert address is not None
        log.debug(
            'IS: %x:%x == %x -> %d', address, memory[soffset(address)],
            dictionary['is'], memory[soffset(address)] == dictionary['is'])
        check = memory[soffset(address)] == dictionary['is']
    if check and 'min' in dictionary:
        assert address is not None
        log.debug(
            'MIN: %x:%x >= %x -> %d', address, memory[soffset(address)],
            dictionary['min'], memory[soffset(address)] >= dictionary['min'])
        check = memory[soffset(address)] >= dictionary['min']
    if check and 'choice' in dictionary:
        c = False
        log.debug('Choice BEGIN')
        for ch in dictionary['choice']:
            c |= _parse_item(memory, ch)
        log.debug('Choice END -> %d', c)
        check = c
    if check and 'step' in dictionary:
        steps = list(dictionary['step'].keys())
        steps.sort(reverse=True)
        for s in steps:
            log.debug('Step: %d', s)
            if dictionary['step'][s] is None:
                log.debug('Step always TRUE')
                check = s
                break
            if _parse_item(memory, dictionary['step'][s], sub=True):
                log.debug('Step RESULT -> %d', s)
                check = s
                break
        else:
            check = False
    return check
