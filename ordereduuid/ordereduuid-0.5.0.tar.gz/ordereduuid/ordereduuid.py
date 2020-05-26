"""Generate secure UUIDs ordered by time created."""
# Author: Jaron S. C. Powser

# Standard Library Imports
import secrets
import time
import uuid
from datetime import datetime, timedelta, timezone


class OrderedUUID(uuid.UUID):
    """Generates a UUID ordered by time."""

    # Time offset used by Python uuid module
    # See https://github.com/python/cpython/blob/3.8/Lib/uuid.py
    #     function uuid1()
    _TIME_OFFSET = 0x1b21dd213814000
    _TIME_MASK = 0x0fffffffffffffff
    _TIME_UPPER_MASK = 0x0ffffffffffff000
    _TIME_LOWER_MASK = 0x0fff
    _CLOCK_SEQ_AND_VARIANT_BITS = 16

    _MIN_NONSTANDARD_VERSION = 6
    _MAX_NONSTANDARD_VERSION = 15

    _MAC_BITS = 48
    _MAX_MAC_VALUE = 0xffffffffffff
    _MULTICAST_MAC_MASK = 0x10000000000

    _last_timestamp = 0

    def __init__(
            self, clock_seq=None, random_node=True, imitate_uuid4=False
    ):
        self._imitate_uuid4 = imitate_uuid4
        time_and_version = self._generate_time_andversion()
        clock_seq_and_variant = (
            self._get_clock_seq_and_variant(clock_seq)
        )
        if random_node:
            node = secrets.randbits(
                OrderedUUID._MAC_BITS
            ) | OrderedUUID._MULTICAST_MAC_MASK
        else:
            node = uuid.getnode()

        uuid_int = (
            (time_and_version << 64)
            + (clock_seq_and_variant << 48)
            + node
        )
        super(OrderedUUID, self).__init__(int=uuid_int)

    def __setattr__(self, name, value):
        # Create a one-time exception to UUID immutability
        if(name == '_imitate_uuid4' and '_imitate_uuid4' not in dir(self)):
            object.__setattr__(self, name, value)
        else:
            super(OrderedUUID, self).__setattr__(name, value)

    @property
    def imitate_uuid4(self):
        return self._imitate_uuid4

    @property
    def time(self):
        if self._imitate_uuid4:
            uuid_int = self.int
            time_upper = (uuid_int >> 68) & OrderedUUID._TIME_UPPER_MASK
            time_lower = (uuid_int >> 64) & OrderedUUID._TIME_LOWER_MASK
            uuid_time = time_upper + time_lower
        else:
            uuid_time = (self.int >> 64) & OrderedUUID._TIME_MASK
        return uuid_time

    @property
    def time_low(self):
        return self.time & 0xffffffff

    @property
    def time_mid(self):
        return super(OrderedUUID, self).time_mid

    @property
    def time_hi_version(self):
        if self._imitate_uuid4:
            time_hi = self.int >> 116
            version = self.version
            time_hi_version = (version << 12) + time_hi
        else:
            time_hi_version = self.int >> 112
        return time_hi_version

    @property
    def asctime_local(self):
        return time.asctime(time.localtime(self.time_seconds))

    @property
    def asctime_utc(self):
        return time.asctime(time.gmtime(self.time_seconds))

    @property
    def ctime(self):
        return time.ctime(self.time_seconds)

    @property
    def datetime(self):
        """Return a timezone-naive datetime"""
        return datetime.fromtimestamp(self.time_seconds)

    @property
    def datetime_local(self):
        """Return a timezone-aware datetime object in local time."""
        calculated_delta = (datetime.now() - datetime.utcnow())
        # Round seconds to nearest 100; determine hour offset
        rounded_delta = timedelta(
            days=calculated_delta.days,
            seconds=round(calculated_delta.seconds, -2)
        )
        datetime_local = datetime.fromtimestamp(
            self.time_seconds, timezone(rounded_delta)
        )
        return datetime_local

    @property
    def datetime_utc(self):
        """Return a timezone-aware datetime object in UTC."""
        return datetime.fromtimestamp(self.time_seconds, timezone.utc)

    @property
    def time_precise(self):
        return self.time - OrderedUUID._TIME_OFFSET

    @property
    def time_micros(self):
        return self.time_precise // 10

    @property
    def time_millis(self):
        return self.time_precise // 10000

    @property
    def time_nanos(self):
        return self.time_precise * 100

    @property
    def time_seconds(self):
        return self.time_precise // 10000000

    def to_uuid1(self):
        return uuid.UUID(
            fields=(self.time_low, self.time_mid, self.time_hi_version,
                    self.clock_seq_hi_variant, self.clock_seq_low,
                    self.node), version=1
        )

    def to_uuid4(self):
        if self._imitate_uuid4:
            uuid4 = uuid.UUID(int=self.int)
        else:
            time_and_version = self._encode_time_and_version(
                self.time, imitate_uuid4=True
            )
            uuid_int = (
                time_and_version << 64
                + (self.int & 0xffffffffffffffff)
            )
            uuid4 = uuid.UUID(int=self.int)
        return uuid4

    def _get_clock_seq_and_variant(self, clock_seq):
        if clock_seq is None:
            clock_seq = secrets.randbits(
                OrderedUUID._CLOCK_SEQ_AND_VARIANT_BITS
            )

        if self._imitate_uuid4:
            # Set most significant clock sequence bits to 0b10...
            #     Indicates RFC 4122 compatibility
            clock_seq_and_variant = (clock_seq | 0x8000) & 0xbfff
        else:
            # Set most significant clock sequence bits to 0b111...
            #     Indicates a variant reserved for future use
            clock_seq_and_variant = clock_seq | 0xe000
        return clock_seq_and_variant

    def _generate_time_andversion(self):
        """Generate a timestamp for use with an OrderedUUID."""
        timestamp = (
            (time.time_ns() // 100) + OrderedUUID._TIME_OFFSET
        ) & OrderedUUID._TIME_MASK
        if timestamp <= OrderedUUID._last_timestamp:
            timestamp = timestamp + 1
        if timestamp > OrderedUUID._TIME_MASK:
            raise Exception('Timestamp generated is too high.')

        OrderedUUID._last_timestamp = timestamp
        time_and_version = self._encode_time_and_version(timestamp) 
        return time_and_version

    def _encode_time_and_version(self, timestamp, imitate_uuid4=None):
        if self._imitate_uuid4:
            version = 4
            time_upper = timestamp & OrderedUUID._TIME_UPPER_MASK
            time_lower = timestamp & OrderedUUID._TIME_LOWER_MASK
            time_and_version = (
                (time_upper << 4) + (version << 12) + time_lower
            )
        else:
            # Set four version bits to nonstandard value
            version = secrets.choice(
                range(OrderedUUID._MIN_NONSTANDARD_VERSION,
                      OrderedUUID._MAX_NONSTANDARD_VERSION + 1)
            )
            time_and_version = (timestamp << 4) + version
        return time_and_version
