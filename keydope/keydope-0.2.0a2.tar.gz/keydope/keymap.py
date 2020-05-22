from typing import Optional, List, Dict, Tuple
import logging
import logging.handlers
import time

from keydope.keycodes import Key, Action, KeyAction
from keydope import mods
from keydope import key_parsing
from keydope import util
from keydope import devices

MULTI_PURPOSE_SINGLE_KEY_THRESHOLD = 0.1

logger = logging.getLogger(__name__)


class WindowClassCondition:

    def __init__(self, include_regex, exclude_regex):
        self.include_regex = include_regex
        self.exclude_regex = exclude_regex

    def __call__(self, state, key_action):
        focused_window = util.get_active_window_metadata()
        if not focused_window:
            logger.error('Could not get focused window metadata')
            return False
        if self.exclude_regex and self.exclude_regex.match(
                focused_window.window_class):
            return False
        if not self.include_regex:
            return True
        return self.include_regex.match(focused_window.window_class)

    def to_yaml(self):
        yaml_object = {'type': 'focused_window'}
        if self.include_regex:
            yaml_object['include_regex'] = self.include_regex.pattern
        if self.exclude_regex:
            yaml_object['exclude_regex'] = self.exclude_regex.pattern
        return yaml_object


class KeyActionCondition:

    def __init__(self, include_regex, exclude_regex, key_actions):
        self.include_regex = include_regex
        self.exclude_regex = exclude_regex
        self.key_actions = key_actions

    def __call__(self, state, key_action):
        pass

    def to_yaml(self):
        yaml_object = {'type': 'key_action'}
        if self.include_regex:
            yaml_object['include_regex'] = self.include_regex.pattern
        if self.exclude_regex:
            yaml_object['exclude_regex'] = self.exclude_regex.pattern
        yaml_object['key_actions'] = [
            keyaction.name for keyaction in self.key_actions
        ]
        return yaml_object


class SetKeymapAction:

    def __init__(self, keymap):
        self.keymap = keymap

    def __call__(self, state, key_action):
        logger.info('Switching to keymap: %s', self.keymap.name)
        state.active_keymap = self.keymap

    def to_yaml(self):
        return {'next_keymap': self.keymap.to_yaml()}


class PressComboAction:

    def __init__(self, output_device: devices.OutputDevice, combo):
        self.output_device = output_device
        self.combo = combo

    def __call__(self, state, key_action):
        # self.output_device.send_combo(self.combo)
        pass

    def to_yaml(self):
        return {'output': key_parsing.combo_to_str(self.combo)}


class Mapping:

    def __init__(self, name, conditions, actions):
        self.name = name
        self.conditions = conditions
        self.actions = actions

    def to_yaml(self):
        yaml_object = {'name': self.name, 'conditions': [], 'actions': []}
        for condition in self.conditions:
            yaml_object['conditions'].append(condition.to_yaml())
        for action in self.actions:
            yaml_object['actions'].append(action.to_yaml())
        return yaml_object


class Keymap:

    def __init__(self, name, mappings):
        self.name = name
        self.mappings = mappings

    def process_event(self, state, key_action):
        mapping_matched = False
        for mapping in self.mappings:
            if not all(cond(state, key_action) for cond in mapping.conditions):
                continue
            for action in mapping.actions:
                action(state, key_action)
            mapping_matched = True
            break
        if not mapping_matched:
            pass

    def to_yaml(self):
        yaml_object = []
        # if self.name:
        #     yaml_object['name'] = self.name
        for mapping in self.mappings:
            yaml_object.append(mapping.to_yaml())
        return yaml_object


class KeyProcessorState:

    def __init__(self, top_level_keymap):
        self.active_keymap = top_level_keymap
        self.pending_key_actions = []
        self.pressed_modifier_keys = set()
        self.key_action_to_last_timestamp = {}
        self.last_key_action = None


class KeyProcessor:

    def __init__(self, output_device, top_level_keymap, fallback_keymap=None):
        self.output_device = output_device
        self.top_level_keymap = top_level_keymap
        self.fallback_keymap = fallback_keymap
        self.state = KeyProcessorState(top_level_keymap)

    # pylint: disable=unused-argument
    def on_event(self,
                 key_action: KeyAction,
                 input_device_name: Optional[str] = None,
                 active_window: Optional[util.WindowMetadata] = None):
        if key_action.key == Key.PAUSE:
            raise util.RescueRequested()
        self.state.active_keymap.process_event(self.state, key_action)
