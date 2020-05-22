import logging
import queue
import select
import threading
import time
from typing import List

import evdev
import inotify_simple

from keydope import devices, session
from keydope.keycodes import Action, Key, KeyAction

_ACTIVE_TTY_PATH = '/sys/class/tty/tty0/active'

logger = logging.getLogger(__name__)

# pylint: disable=broad-except


# If the sdnotify library is available, notify systemd that the process started.
def _maybe_notify_we_started():
    try:
        # pylint: disable=import-outside-toplevel
        import sdnotify
        logger.info('Notifying systemd we started')
        sdnotify.SystemdNotifier().notify('READY=1')
    except ImportError:
        pass


# pylint: disable=too-many-locals,too-many-branches,too-many-statements
def loop(input_devices_manager: devices.InputDevicesManager,
         output_device: devices.OutputDevice,
         key_processor) -> None:

    events_queue = queue.Queue()
    processing_exceptions = queue.Queue()

    def process_events():
        while True:
            input_device, event = events_queue.get()
            try:
                # pylint: disable=no-member
                if event.type != evdev.ecodes.EV_KEY:
                    output_device.send_event(event)
                    continue
                start_time = time.time()
                key_action = KeyAction(Key(event.code), Action(event.value))
                key_processor.on_event(key_action, input_device.name)
                processing_duration = time.time() - start_time
                logger.debug(
                    'Processing duration: {:.5f}'.format(processing_duration))
            except OSError as e:
                input_devices_manager.handle_error(input_device, e)
            # pylint: disable=broad-except
            except Exception as e:
                processing_exceptions.put(e)
                return

    # daemon: don't wait for this thread after the main thread exits.
    processing_thread = threading.Thread(target=process_events,
                                         name='keyboard_remapper',
                                         daemon=True)
    processing_thread.daemon = True
    processing_thread.start()

    inotify = inotify_simple.INotify()
    # Watch descriptor for the active TTY.
    active_tty_wd = inotify.add_watch(_ACTIVE_TTY_PATH,
                                      inotify_simple.flags.MODIFY)
    devices.add_devices_watch(inotify)

    def process_inotify_events():
        for event in inotify.read():
            if event.wd == active_tty_wd:
                with open(_ACTIVE_TTY_PATH) as f:
                    active_tty = f.read().strip()
                # TODO: stop processing keybindings when active TTY is not
                # configured to be active.
                logging.info(f'Active TTY changed to: {active_tty}')
            else:
                input_devices_manager.handle_inotify_event(event)

    def on_session_change(active_session):
        if active_session:
            # TODO: stop processing keybindings when active session is not
            # configured to be active and/or has x11 running.
            logging.debug(f'Active session type: {active_session["Type"]}')
        else:
            logging.debug('No active session')

    session_monitor = session.get_session_monitor()
    # daemon: don't wait for this thread after the main thread exits.
    session_monitor_thread = threading.Thread(target=session_monitor.monitor,
                                              args=(on_session_change,),
                                              name='session_monitor',
                                              daemon=True)
    session_monitor_thread.daemon = True
    session_monitor_thread.start()

    _maybe_notify_we_started()

    try:
        while True:
            try:
                if not processing_exceptions.empty():
                    raise processing_exceptions.get(block=False)
                waitables = input_devices_manager.devices + [inotify]
                readables, _, _ = select.select(waitables, [], [])
                for readable in readables:
                    if isinstance(readable, inotify_simple.INotify):
                        process_inotify_events()
                        continue
                    for event in readable.read():
                        events_queue.put((readable, event))
            except queue.Empty:
                pass
            except ValueError as e:
                logging.debug(e.__dict__)
            except IOError as e:
                if e.errno == 19:
                    logging.info('Device disappeared: %s', e)
    finally:
        inotify.close()
