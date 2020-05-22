import collections
import csv
import itertools
import logging
import os
import queue
import threading
import time
from typing import Optional

from keydope import key_parsing, mods, util
from keydope.keycodes import Action, KeyAction

# from sqlalchemy.ext.declarative import declarative_base, declared_attr
# from sqlalchemy import (Index, Column, Boolean, Integer, Unicode, DateTime,
#                         Binary, ForeignKey, create_engine)
# import sqlalchemy.orm

# def create_sessionmaker(fname):
#     engine = create_engine('sqlite:///%s' % fname)
#     Base.metadata.create_all(engine)
#     return sqlalchemy.orm.sessionmaker(bind=engine)

# ENCRYPTER = None

# Base = declarative_base()

# class Window(Base):
#     wm_class = Column(Unicode, index=True)
#     wm_instance = Column(Unicode, index=True)
#     title = Column(Unicode, index=True)

# class KeystrokeStats(Base):
#     id = Column(Integer, primary_key=True)
#     keys = Column(Unicode, index=True)
#     window_id = Column(
#         Integer, ForeignKey('window.id'), nullable=False, index=True)
#     window = sqlalchemy.orm.relationship(
#         "Window", backref=sqlalchemy.orm.backref('windows'))

FLUSH_INTERVAL = 60 * 5
MIN_LOGGED_KEYPRESS_OCCURENCES = 5

COMBOS_FILENAME = 'combos'
COMBOS_FILE_FIELDS = [
    'timestamp',
    'combo',
    'window_class',
    'window_instance',
    'window_title',
]

KEYPRESS_SEQUENCES_FILENAME = 'sequences'
MAX_SEQUENCE_LEN = 3

logger = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class FileStatsAggregator:

    def __init__(self, output_directory: str):
        self.output_directory = output_directory
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        self._last_flush_time = time.time()
        self.keypress_sequence = collections.deque(maxlen=MAX_SEQUENCE_LEN)
        self.keypress_sequence_counts = collections.Counter()
        self._keypress_sequence_lock = threading.Lock()
        self._combo_file_lock = threading.Lock()
        self._active_threads = []
        self._combos_queue = queue.Queue()
        self._key_actions_queue = queue.Queue()

    def register_key_action(self,
                            key_action: KeyAction,
                            window: Optional[util.WindowMetadata],
                            block=False):
        if key_action.action != Action.PRESS:
            return
        if not window:
            window = util.WindowMetadata()
        if not block:
            self._key_actions_queue.put((key_action, window))
            return
        with self._keypress_sequence_lock:
            self.keypress_sequence.append(key_action.key)
            for i in range(len(self.keypress_sequence)):
                sequence = tuple(
                    itertools.islice(self.keypress_sequence, i, None))
                self.keypress_sequence_counts[sequence] += 1
        self._flush_sequences_if_needed()

    def _flush_sequences_if_needed(self):
        now = time.time()
        if now < self._last_flush_time + FLUSH_INTERVAL:
            return
        self._last_flush_time += FLUSH_INTERVAL
        sequence_file_path = os.path.join(self.output_directory,
                                          KEYPRESS_SEQUENCES_FILENAME)
        with self._keypress_sequence_lock:
            sequences_to_flush = []
            for sequence, count in self.keypress_sequence_counts.items():
                if count >= MIN_LOGGED_KEYPRESS_OCCURENCES:
                    sequences_to_flush.append((sequence, count))
            logger.debug('Flushing stats about %d key sequences',
                         len(sequences_to_flush))
            with open(sequence_file_path, 'a', encoding='utf8') as f:
                writer = csv.writer(f)
                for sequence, count in sequences_to_flush:
                    sequence_str = ' -> '.join(key.name for key in sequence)
                    writer.writerow([int(now), sequence_str, count])
                    del self.keypress_sequence_counts[sequence]

    def register_combo(self,
                       combo: mods.Combo,
                       action: Action,
                       window: util.WindowMetadata,
                       block=False):
        if action != Action.PRESS:
            return
        # Only log combos with more than one key.
        if len(combo.keys) < 2:
            return
        if not window:
            window = util.WindowMetadata()
        if not block:
            self._combos_queue.put((combo, action, window))
            return
        combo_file_path = os.path.join(self.output_directory, COMBOS_FILENAME)
        with self._combo_file_lock:
            with open(combo_file_path, 'a', encoding='utf8') as f:
                writer = csv.DictWriter(f, COMBOS_FILE_FIELDS)
                writer.writerow({
                    'timestamp': int(time.time()),
                    'combo': key_parsing.combo_to_str(combo),
                    'window_class': window.window_class,
                    'window_instance': window.window_instance,
                    'window_title': window.title,
                })

    def start_background_threads(self):
        assert not self._active_threads

        def _process_key_actions():
            while True:
                args = self._key_actions_queue.get()
                self.register_key_action(*args, block=True)

        def _process_combos():
            while True:
                args = self._combos_queue.get()
                self.register_combo(*args, block=True)

        self._active_threads = [
            threading.Thread(target=_process_key_actions),
            threading.Thread(target=_process_combos),
        ]
        for thread in self._active_threads:
            # Don't wait for these thread after the main thread exits.
            thread.daemon = True
            thread.start()

    def join(self):
        for thread in self._active_threads:
            thread.join()
