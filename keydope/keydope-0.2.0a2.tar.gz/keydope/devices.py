import io
import logging
import os
import re
import sys
import threading
import time
from typing import Iterable, List, Optional, Set

import evdev
import inotify_simple
from evdev.uinput import UInputError

from keydope import mods
from keydope.keycodes import KEY_CODES, Action, Key, KeyAction

OUTPUT_DEVICE_NAME = 'keydope-fake-output-device'
_INPUT_DEVICES_DIR = '/dev/input'
# Devices that are known to masquerade as keyboards.
_DEFAULT_EXCLUDE_RE = re.compile(r'Yubico')

_PERMISSION_ERRORS_HELP = '''
Make sure that you have executed keydope with sufficient privileges such as:

    $ sudo keydope config.py
'''

logger = logging.getLogger(__name__)


class OutputDevice:

    def __init__(self, uinput_device: evdev.uinput.UInput):
        self.uinput_device = uinput_device
        # Keys that change the state of the downstream keyboard handler (X11 in
        # this case). They must be tracked in order to predictably control the
        # downstream keyboard handler regardless of the previously pressed keys.
        self.pressed_mod_keys = set()

    def _update_modifier_key_pressed(self, key_action: KeyAction):
        if key_action.key in mods.get_all_modifier_keys():
            if key_action.action.is_pressed():
                self.pressed_mod_keys.add(key_action.key)
            else:
                self.pressed_mod_keys.discard(key_action.key)

    def _send_sync(self) -> None:
        self.uinput_device.syn()

    def send_event(self, event) -> None:
        self.uinput_device.write_event(event)
        self._send_sync()

    def send_key_action(self, key_action: KeyAction) -> None:
        logger.debug('Sending %s', key_action)
        self._update_modifier_key_pressed(key_action)
        # pylint: disable=no-member
        self.uinput_device.write(evdev.ecodes.EV_KEY, key_action.key.value,
                                 key_action.action.value)
        self._send_sync()

    def get_modifier_keys(self) -> Set[Key]:
        return self.pressed_mod_keys

    def set_modifier_keys(self, modifier_keys: Iterable[Key]) -> None:
        modifier_to_key = {}
        for key in modifier_keys:
            mod = mods.key_to_modifier(key)
            if not mod:
                raise ValueError('Not a modifier key: {}'.format(key.name))
            if mod in modifier_to_key:
                logging.info(
                    'Got multiple keys for the same modifier. '
                    'Modifier: %s, Keys: %s, %s', mod, modifier_to_key[mod],
                    key)
                continue
            modifier_to_key[mod] = key
        for modifier in set(mods.Modifier) - modifier_to_key.keys():
            for modifier_key in mods.modifier_to_keys(modifier):
                if modifier_key in self.pressed_mod_keys:
                    self.send_key_action(KeyAction(modifier_key,
                                                   Action.RELEASE))
        for modifier in modifier_to_key:
            modifier_keys = mods.modifier_to_keys(modifier)
            if any(modifier_key in self.pressed_mod_keys
                   for modifier_key in modifier_keys):
                continue
            modifier_key = modifier_to_key[modifier]
            self.send_key_action(KeyAction(modifier_key, Action.PRESS))


def get_uinput_device() -> evdev.uinput.UInput:
    return evdev.uinput.UInput(name=OUTPUT_DEVICE_NAME)


# Helper for making it clearer to users that there are permission errors.
def get_uinput_device_or_die() -> OutputDevice:
    if not os.path.exists('/dev/uinput'):
        sys.exit('Can\'t find /dev/uinput, make sure your kernel is '
                 'configured correctly.')
    try:
        return OutputDevice(get_uinput_device())
    except UInputError:
        sys.exit('Failed to open `uinput` in write mode.\n' +
                 _PERMISSION_ERRORS_HELP)


def _is_keyboard_device(device: evdev.InputDevice) -> bool:
    '''Guesses if the device is a keyboard'''
    capabilities = device.capabilities(verbose=False)
    key_capabilities = capabilities.get(1)
    if not key_capabilities:
        return False
    supported_keys = set()
    for keycode in key_capabilities:
        if keycode in KEY_CODES:
            supported_keys.add(Key(keycode))
    if Key.SPACE not in supported_keys or \
       Key.A not in supported_keys or \
       Key.Z not in supported_keys:
        # Doesn't support common keys, not keyboard.
        return False
    # Originally, this code was filtering out devices with mouse buttons, so I
    # assume some mice may have incorrectly reported keyboard keys, causing a
    # false positive in the keyboard classification.
    # However, keyboards with touchpads, like Logitech K400 Plus and K830, also
    # report mouse keys, and they're valid keyboards, so filtering out devices
    # with mouse buttons will cause a false negative. Therefore the current
    # approach is to use these devices, but log this decision.
    if Key.BTN_MOUSE in supported_keys:
        logger.info(
            'Device %s supports mouse buttons but is classified as a keyboard.',
            device.name)
    return True


def format_device_list(devices: List[evdev.InputDevice]) -> str:
    device_format = '{1.fn:<20} {1.name:<35} {1.phys}'
    device_lines = [device_format.format(n, d) for n, d in enumerate(devices)]
    header_lines = []
    header_lines.append('-' * len(max(device_lines, key=len)))
    header_lines.append('{:<20} {:<35} {}'.format('Device', 'Name', 'Phys'))
    header_lines.append('-' * len(max(device_lines, key=len)))
    result = io.StringIO()
    result.writelines(line + '\n' for line in header_lines)
    result.writelines(line + '\n' for line in device_lines)
    return result.getvalue()


class InputDevicesManager:

    def __init__(self, include_regex=None, exclude_regex=None):
        self._include_regex = include_regex
        self._exclude_regex = exclude_regex
        self._devices: List[evdev.InputDevice] = []
        if not self._include_regex and not self._exclude_regex:
            logger.info('No device filters specified, keydope will auto-select '
                        'keyboard-looking devices.')
        self._lock = threading.Lock()
        self._reload_managed_devices()

    # Returns a device if it passes the filters.
    def _maybe_get_device(self, path: str) -> Optional[evdev.InputDevice]:
        if not os.access(path, os.R_OK):
            logging.info('Filtering out non-readable device: %s', path)
            return None
        device = evdev.InputDevice(path)
        # Exclude the device we use for output and non-keyboard devices.
        if device.name == OUTPUT_DEVICE_NAME or not _is_keyboard_device(device):
            logging.info('Filtering out non-keyboard device: %s (%s)',
                         device.fn, device.name)
            return None
        if _DEFAULT_EXCLUDE_RE.match(device.name):
            logging.info('Filtering out default excluded device: %s (%s)',
                         device.fn, device.name)
            return None
        if self._include_regex is not None and not self._include_regex.match(
                device.name):
            return None
        if self._exclude_regex is not None and self._exclude_regex.match(
                device.name):
            return None
        return device

    def _detect_managed_devices(self):
        device_paths = _list_device_paths()
        if not device_paths:
            logger.warning('No input devices seen by keydope. Do you have '
                           'read permission on /dev/input/*?')
        managed_devices = []
        for device_path in device_paths:
            maybe_device = self._maybe_get_device(device_path)
            if maybe_device:
                managed_devices.append(maybe_device)
        return managed_devices

    def _maybe_reload_managed_devices(self):
        if self._lock.locked():
            logger.info('Reloading devices already in progress, skipping')
            return
        with self._lock:
            self._reload_managed_devices()

    def _reload_managed_devices(self):
        start_time = time.time()
        detected_devices = self._detect_managed_devices()
        logger.debug('Detecting devices duration: {:.5f}'.format(time.time() -
                                                                 start_time))
        if not detected_devices:
            logger.info('No input devices selected, keydope will be inactive')
            return
        logger.info('Enabling remapping on the following devices:\n%s',
                    format_device_list(detected_devices))
        # Grab any newly managed devices.
        for device in detected_devices:
            if device not in self._devices:
                logger.info(f'Grabbing device: {device.fn} ({device.name})')
                device.grab()
        # Ungrab any devices no longer managed.
        for device in self._devices:
            if device not in detected_devices:
                # According to a commit in xkeysnail (see URL below), sometimes
                # devices that are not actually removed are considered removed,
                # so we must always try to ungrab them. Otherwise, the device
                # might be locked.
                # https://github.com/mooz/xkeysnail/commit/1612e5f378d622a2979d904d0a3986a19ca0249b
                try_ungrab_device(device)
        self._devices = detected_devices
        logger.debug('Reloading devices duration: {:.5f}'.format(time.time() -
                                                                 start_time))

    @property
    def devices(self) -> List[evdev.InputDevice]:
        return self._devices

    def release_managed_devices(self):
        for device in self.devices:
            try_ungrab_device(device)

    def handle_error(self, device: evdev.InputDevice, error: OSError):
        start_time = time.time()
        logger.warning('Got OS error: %s', error)
        if not os.access(device.fn, os.R_OK):
            logger.info('Device no longer readable: %s', device)
        self._devices = [d for d in self._devices if d != device]
        self._reload_managed_devices()
        logger.debug('Error handling duration: {:.5f}'.format(time.time() -
                                                              start_time))

    def _maybe_remove_device(self, device_path: str):
        updated_devices = []
        for device in self.devices:
            if device.fn == device_path:
                logger.debug(f'Removing device: {device.fn} ({device.name})')
                try_ungrab_device(device)
            else:
                updated_devices.append(device)
        self._devices = updated_devices

    # NOTE: I'm not calling _reload_managed_devices here because it's very slow
    # (around 1 sec). It seems the slowness is because of the evdev.InputDevice
    # constructor.
    def handle_inotify_event(self, event: inotify_simple.Event) -> None:
        logger.debug(f'inotify event: {event}')
        device_path = os.path.join(_INPUT_DEVICES_DIR, event.name)
        flags = inotify_simple.flags
        deleted_or_moved = bool(event.mask & flags.DELETE or
                                event.mask & flags.MOVED_TO)
        added = bool(event.mask & flags.CREATE or event.mask & flags.MOVED_FROM)
        read_permission_removed = bool(event.mask & flags.ATTRIB and
                                       not os.access(device_path, os.R_OK))
        logger.debug('deleted: %s, added: %s, read permission removed: %s',
                     deleted_or_moved, added, read_permission_removed)
        if deleted_or_moved or read_permission_removed:
            self._maybe_remove_device(device_path)
            return
        if not added:
            logger.info('Not handling inotify event')
            return
        maybe_device = self._maybe_get_device(device_path)
        if not maybe_device:
            return
        logger.debug(f'Enabling remapping on device {maybe_device}')
        try:
            maybe_device.grab()
            self._devices.append(maybe_device)
        except IOError:
            # Only log errors on new devices
            logger.error('IOError when grabbing new device: %s',
                         maybe_device.name)


# Helper for making it harder to new users to miss errors by dying with
# appropriate error messages.
def get_input_devices_manager_or_die(include_regex=None,
                                     exclude_regex=None) -> InputDevicesManager:
    '''Selects devices from the list of accessible input devices.'''
    device_paths = _list_device_paths()
    if not device_paths:
        sys.exit('Error: no input devices seen by keydope. '
                 'Do you have read permission on /dev/input/?')
    manager = InputDevicesManager(include_regex, exclude_regex)
    if not manager.devices:
        sys.exit('Error: no input devices selected. Run with --log-level=debug '
                 '--log-to-stdout to see why devices are filtered out')
    return manager


def _list_device_paths() -> List[str]:
    device_paths = []
    for name in os.listdir(_INPUT_DEVICES_DIR):
        if name.startswith('event'):
            device_paths.append(os.path.join(_INPUT_DEVICES_DIR, name))
    return device_paths


def add_devices_watch(inotify: inotify_simple.INotify) -> None:
    flags = inotify_simple.flags
    return inotify.add_watch(
        _INPUT_DEVICES_DIR,
        # Watch for new devices, removed devices, and changed attributes, that
        # may make the device readable/unreadable.
        flags.CREATE | flags.MOVED_FROM | flags.MOVED_TO | flags.DELETE |
        flags.ATTRIB)


# According to a commit in xkeysnail (see below), ungrabbing sometimes fails and
# needs to be ignored.
# https://github.com/mooz/xkeysnail/commit/d1f0121542cc0f798a5a529c358b10beea36874f
def try_ungrab_device(input_device):
    try:
        input_device.ungrab()
    except OSError:
        logger.info('Failed ungrabbing device: %s', input_device)
