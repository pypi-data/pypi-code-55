import collections
import logging
import time
from typing import Dict, List, Optional, Tuple

from keydope import devices, key_dist, key_parsing, mods, stats, util
from keydope.keycodes import Action, Key, KeyAction

RESCUE_PERIOD_DURATION = 60
RESCUE_MIN_RECENT_PRESSES = 3

logger = logging.getLogger(__name__)

# e.g, {Key.LEFT_CTRL: [Key.ESC, Key.LEFT_CTRL]}
MultipurposeMap = Dict[Key, Tuple[Key, Key, float]]


def _is_condition_met(condition, wm_class: Optional[str] = None):
    if condition is None:
        return True
    if not wm_class:
        return False
    if callable(condition):
        return condition(wm_class)
    if hasattr(condition, 'search'):
        return bool(condition.search(wm_class))
    return False


# pylint: disable=too-many-instance-attributes
class KeyProcessor:

    def __init__(self,
                 output_device: devices.OutputDevice,
                 active_window_getter,
                 stats_aggregator: Optional[stats.FileStatsAggregator] = None):
        # Injected dependencies.
        self.output_device = output_device
        self.stats_aggregator = stats_aggregator
        self.active_window_getter = active_window_getter

        # Keymap configuration.
        self._toplevel_keymaps = []
        self._multipurpose_map = {}
        self._last_key_action = time.time()

        # State variables.
        self._active_keymaps = []
        # Keys that were pressed in the "input", even if they weren't passed to
        # the output device. For example, if "Ctrl-a" is mapped to "Alt-c",
        # "Ctrl" and "a" will be in this set, but not "Alt-c".
        self._pressed_input_keys = set()
        # We need to guarantee that every key we send to the output device for
        # pressing will also have a corresponding release event.  To this end,
        # we assign every key that we output to the output device to a key that
        # was pressed to generate it. For example, if "Ctrl-a" is mapped to
        # "Super-Shift-b", "Ctrl" will be mapped to ["Super", "Shift"] and "a"
        # will be mapped to "b".  This way, when "Ctrl" is released, both
        # "Super" and "Shift" will be released, and if "a" is released, "b" will
        # be released.
        self._key_release_mapping = {}
        self._last_key_pressed = None
        self._keypress_to_last_timestamps = collections.defaultdict(
            lambda: collections.deque(maxlen=5))

    # pylint: disable=unused-argument
    def on_event(self,
                 key_action: KeyAction,
                 input_device_name: Optional[str] = None):
        now = time.time()
        if key_action == KeyAction(Key.PAUSE, Action.PRESS):
            self._rescue_if_needed(key_action.key, now)
        if now >= self._last_key_action + 120 and (
                self.output_device.get_modifier_keys()):
            logger.warning(
                'Found pressed physical mods after long time without activity: '
                '%s', self.output_device.get_modifier_keys())
        self._last_key_action = now
        self.process_key_action(key_action)

    def _rescue_if_needed(self, rescue_key: Key, now_timestamp: float):
        num_recent_presses = 1 + sum(
            timestamp >= now_timestamp - RESCUE_PERIOD_DURATION
            for timestamp in self._keypress_to_last_timestamps[rescue_key])
        logger.info('Rescue key %s was pressed %s times in the last %s seconds',
                    rescue_key.name, num_recent_presses, RESCUE_PERIOD_DURATION)
        if num_recent_presses >= RESCUE_MIN_RECENT_PRESSES:
            raise util.RescueRequested()
        logger.info(
            'Ignoring rescue key because only %s/%s presses were '
            'encountered in the last %s seconds', num_recent_presses,
            RESCUE_MIN_RECENT_PRESSES, RESCUE_PERIOD_DURATION)

    def process_key_action(self, original_key_action: KeyAction):
        logger.debug('Original input event: %s', original_key_action)
        try:
            active_window = self.active_window_getter()
        except OSError as e:
            logger.warning('Error getting active window: %s', e)
            active_window = None
        if self.stats_aggregator:
            self.stats_aggregator.register_key_action(original_key_action,
                                                      active_window)
        key_actions = [original_key_action]
        if original_key_action.key in self._multipurpose_map:
            key_actions = self._process_multipurpose_key(original_key_action)
            logger.debug('Key actions derived from multipurpose map: %s',
                         key_actions)
        if original_key_action.action == Action.PRESS:
            self._last_key_pressed = original_key_action.key
            self._keypress_to_last_timestamps[original_key_action.key].append(
                time.time())
        for key_action in key_actions:
            if key_action.action == Action.RELEASE:
                self.release_mapped_keys(key_action.key)
            else:
                self.transform_key(key_action, active_window)

    def transform_key(self,
                      key_action: KeyAction,
                      active_window: Optional[util.WindowMetadata] = None):
        wm_class = active_window.window_class if active_window else None
        self._set_active_keymaps(wm_class)
        input_combo = self.get_input_combo(key_action.key)
        if self.stats_aggregator:
            self.stats_aggregator.register_combo(input_combo, key_action.action,
                                                 active_window)
        logger.debug('Input combo: %s %s, pressed mods: %s',
                     key_parsing.combo_to_str(input_combo),
                     key_action.action.name,
                     self.output_device.get_modifier_keys())
        # _active_keymaps: [global_map, local_1, local_2, ...]
        for mappings in self._active_keymaps:
            mapped_commands = None
            for combo_spec in mappings:
                if combo_spec.match(input_combo):
                    mapped_commands = mappings[combo_spec]
                    break
            if not mapped_commands:
                continue
            # Found key in 'mappings'. Execute commands defined for the key.
            reset_mode = self.handle_commands(key_action, mapped_commands)
            if reset_mode:
                self._active_keymaps = []
            return
        # Not found in all keymaps
        self._send_mapped_combo(key_action, input_combo)
        self._active_keymaps = []

    def handle_commands(self, key_action: KeyAction, commands):
        if not isinstance(commands, list):
            commands = [commands]
        # Execute commands
        for command in commands:
            if isinstance(command, mods.Combo):
                self._send_mapped_combo(key_action, command)
            # Go to next keymap
            elif isinstance(command, dict):
                self._active_keymaps = [command]
                return False
            else:
                raise NotImplementedError(
                    'Unsupported command: {}'.format(command))
        # Reset keymap in ordinary flow
        return True

    def get_input_combo(self, input_key: Key):
        return mods.Combo(self._pressed_input_keys | {input_key})

    def _set_active_keymaps(self, wm_class: Optional[str] = None):
        if self._active_keymaps:
            return
        self._active_keymaps = []
        keymap_names = []
        for condition, mappings, name in self._toplevel_keymaps:
            if _is_condition_met(condition, wm_class):
                self._active_keymaps.append(mappings)
                keymap_names.append(name)
        logger.debug("WM_CLASS '%s' | active keymaps = %s", wm_class,
                     keymap_names)

    def _update_pressed_input_keys(self, key: Key, action: Action):
        if action.is_pressed():
            self._pressed_input_keys.add(key)
        else:
            self._pressed_input_keys.discard(key)

    def _send_mapped_combo(self, input_key_action: KeyAction,
                           output_combo: mods.Combo):
        assert input_key_action.action.is_pressed()
        self._update_pressed_input_keys(input_key_action.key, Action.PRESS)
        input_combo = self.get_input_combo(input_key_action.key)
        mapping = key_dist.map_key_sets(input_combo.keys, output_combo.keys)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                'Key release mapping: %s',
                {i.name: [k.name for k in j] for i, j in mapping.items()})
        self._key_release_mapping.update(mapping)
        mod_output_keys = output_combo.get_mod_keys()
        self.output_device.set_modifier_keys(mod_output_keys)
        nearest_output_key = min(
            output_combo.keys,
            key=lambda k: key_dist.key_distance(k, input_key_action.key))
        # If the action is PRESS, we probably already pressed the modifier keys
        # when calling set_modifier_keys. Therefore, we only send another input
        # event if the mapped output key is not a modifier, or if the action is
        # REPEAT.
        if not mods.key_to_modifier(nearest_output_key) or (
                input_key_action.action == Action.REPEAT):
            self.output_device.send_key_action(
                KeyAction(nearest_output_key, input_key_action.action))

    def release_mapped_keys(self, input_key: Key):
        self._update_pressed_input_keys(input_key, Action.RELEASE)
        if input_key in self._key_release_mapping:
            mapped_output_keys = self._key_release_mapping[input_key]
        else:
            # If it's not in the key release mapping, it probably means that the
            # key press was done before keydope was started, and we only got the
            # release. In this case, just release the input key.
            mapped_output_keys = [input_key]
        for mapped_output_key in mapped_output_keys:
            self.output_device.send_key_action(
                KeyAction(mapped_output_key, Action.RELEASE))
        if input_key in self._key_release_mapping:
            del self._key_release_mapping[input_key]

    def define_keymap(self, condition, mappings,
                      name: str = 'Anonymous keymap'):
        self._toplevel_keymaps.append((condition, mappings, name))
        return mappings

    def define_multipurpose_modmap(self,
                                   multipurpose_remappings: MultipurposeMap):
        '''Defines multipurpose modmap (multi-key translations)

        Give a key two different meanings. One when pressed and released alone
        and one when it's held down together with another key (making it a
        modifier key).

        Example:

        define_multipurpose_modmap(
            {Key.CAPSLOCK: (Key.ESC, Key.LEFT_CTRL, 0.1),
        })
        '''
        for mapping in multipurpose_remappings.values():
            assert len(mapping) == 3
        self._multipurpose_map = multipurpose_remappings

    def _process_multipurpose_key(self,
                                  key_action: KeyAction) -> List[KeyAction]:
        assert key_action.key in self._multipurpose_map
        single_key, mod_key, timeout = self._multipurpose_map[key_action.key]
        if key_action.action.is_pressed():
            self._update_pressed_input_keys(mod_key, Action.PRESS)
            return []
        key_press_timestamps = self._keypress_to_last_timestamps[key_action.key]
        last_timestamp = key_press_timestamps[-1] if key_press_timestamps else 0
        duration_since_press = time.time() - last_timestamp
        if key_action.key != self._last_key_pressed or (duration_since_press >=
                                                        timeout):
            if key_action.key in self._pressed_input_keys:
                return [KeyAction(mod_key, Action.RELEASE)]
            return []
        logger.debug('Single key press-release: %s', single_key.name)
        self._update_pressed_input_keys(mod_key, Action.RELEASE)
        return [
            KeyAction(single_key, Action.PRESS),
            KeyAction(single_key, Action.RELEASE),
        ]
