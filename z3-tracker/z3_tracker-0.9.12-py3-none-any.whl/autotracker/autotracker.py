'''
Main autotracker process
'''

import asyncio
import importlib
import logging as log
import queue
import threading

from ..config import CONFIG

from .exceptions import AutotrackerException, NoConnection, ParseError, NoDevice
from . import usb2snes

gui = importlib.import_module(
    '..{0:s}.autotracker'.format(CONFIG['gui']), package=__package__)

DATA = {'items': queue.Queue()}
INTERFACES = {'items': None}
STOP = threading.Event()

__all__ = 'DATA', 'INTERFACES', 'STOP', 'thread'


async def _autotrack(memview: usb2snes.MemoryReader) -> None:
    '''
    Run autotracker routines.

    Args:
        memview: console memory reader
    Raises:
        AutotrackerException: on connection loss
    '''

    interval = 0
    while not STOP.is_set():

        # Check for config changes.
        for _ in range(interval):
            if not CONFIG['autotracking']:
                return
            if CONFIG['usb2snes_device'] not in memview.device:
                return
            if STOP.wait(timeout=0.33):
                return
        interval = 5 * 3

        # Check whether Zelda 3 is running.
        ingame = await memview.check_game_status()
        if not ingame:
            for w in INTERFACES.values():
                w.autotrack.set_state('off')
            continue
        for w in INTERFACES.values():
            w.autotrack.set_state('on')

        # Check inventory.
        items = await memview.check_items()
        if INTERFACES['items'].autotrack.toggle:
            INTERFACES['items'].set_all(items)


async def _main() -> None:
    '''
    Autotracker loop
    '''

    memview = usb2snes.MemoryReader()

    while not STOP.wait(timeout=0.3):
        if gui.INFOSTRING is None or gui.INFOTEXT is None or gui.FRAME is None:
            continue
        if not CONFIG['autotracking']:
            for w in INTERFACES.values():
                w.autotrack.disable()
            continue
        else:
            for w in INTERFACES.values():
                w.autotrack.enable()

        log.debug('Starting autotracker.')
        quick_retry = False

        try:
            await memview.connect()
        except (OSError, NoConnection):
            gui.set_info(
                "Could not connect to QUsb2snes server '{0:s}'.".format(
                CONFIG['usb2snes_server']),
                     'error')
        except ParseError:
            gui.set_info("Unexpected message from QUsb2snes server.", 'error')
        except NoDevice:
            pass
        else:
            gui.set_info(
                'Connected to device: {0:s}'.format(memview.device), 'info',
                refreshbutton=False)
            for w in INTERFACES.values():
                w.autotrack.enable()
            try:
                await _autotrack(memview)
            except AutotrackerException:
                log.error('Lost connection to QUsb2snes.')
                gui.set_info('Lost connection to QUsb2snes.', 'error')
                quick_retry = True
            else:
                if STOP.is_set():
                    log.info('Autotracker stopped.')
                    return
                log.info(
                    '%s autotracker.',
                    'Restarting' if CONFIG['autotracking'] else 'Stopping')
                gui.set_info('')
                continue
            finally:
                await memview.disconnect()

        for w in INTERFACES.values():
            w.autotrack.set_state('error')

        infotxt = gui.INFOSTRING.get()
        if infotxt:
            infotxt += '\n\n'
        else:
            infotxt = 'Autotracker: '
        counter = 5 if quick_retry else 20
        while counter > 0:
            if not CONFIG['autotracking']:
                break
            gui.set_info(infotxt + 'Restarting in {0:d}s.'.format(counter))
            subcounter = 0
            for _ in range(5):
                if STOP.wait(timeout=0.2) or gui.REFRESH.is_set():
                    counter = 0
                    gui.REFRESH.clear()
                    break
            counter -= 1
        else:
            if STOP.is_set():
                log.info('Autotracker stopped.')
                return
            log.debug('Restarting autotracker.')
            gui.set_info('')
            continue
        gui.set_info('')
        log.info('Autotracker stopped.')


def thread(windows: dict) -> None:
    '''
    Autotracker thread

    Args:
        windows: tracker windows
    '''

    asyncloop = asyncio.new_event_loop()
    asyncio.set_event_loop(asyncloop)

    try:
        asyncio.run(_main())
    except:
        gui.set_info(
            'Autotracker has crashed. Please restart z3-tracker.', 'error')
        raise
