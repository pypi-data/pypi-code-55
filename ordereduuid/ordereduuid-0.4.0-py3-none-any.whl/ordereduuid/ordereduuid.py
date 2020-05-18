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
    _CLOCK_SEQ_AND_VARIANT_BITS = 16

    _MAC_BITS = 48
    _MAX_MAC_VALUE = 0xffffffffffff
    _MULTICAST_MAC_MASK = 0x10000000000

    _last_timestamp = 0

    def __init__(
            self, clock_seq=None, random_node=True, imitate_UUID4=False
    ):
        self._imitate_UUID4 = imitate_UUID4
        timestamp = self._get_timestamp()
        if imitate_UUID4:
            return NotImplemented
        else:
            time_and_version = timestamp + (0xf << 60)

        # OR clock sequence bits to indicate RESERVED_FUTURE variant
        # See https://github.com/python/cpython/blob/3.8/Lib/uuid.py
        #     RESERVED_FUTURE string definition
        if clock_seq is None:
            clock_seq_and_variant = (
                secrets.randbits(
                    OrderedUUID._CLOCK_SEQ_AND_VARIANT_BITS
                ) | 0xE000
            )
        else:
            clock_seq_and_variant = clock_seq | 0xE000

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
        if( name == '_imitate_UUID4'
                and '_imitate_UUID4' not in dir(self)):
            object.__setattr__(self, name, value)
        else:
            super(OrderedUUID, self).__setattr__(self, name, value)

    @property
    def imitate_UUID4(self):
        return self._imitate_UUID4

    @property
    def time_low(self):
        if self._imitate_UUID4:
            time_low = NotImplemented
        else:
            time_low = (self.int >> 64) & 0xffffffff
        return time_low

    @property
    def time_mid(self):
        if self._imitate_UUID4:
            time_mid = NotImplemented
        else:
            time_mid = (self.int >> 80) & 0xffff
        return time_mid

    @property
    def time_hi_version(self):
        if self._imitate_UUID4:
            time_hi_version = NotImplemented
        else:
            time_hi_version = (self.int >> 96) & 0xfff
        return time_hi_version

    @property
    def version(self):
        if self._imitate_UUID4:
            version = NotImplemented
        else:
            version = (self.int >> 124)
        return version

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
        rounded_delta = timedelta(days=calculated_delta.days,
            seconds=round(calculated_delta.seconds, -2))
        datetime_local = datetime.fromtimestamp(
            self.time_seconds, timezone(rounded_delta)
        )
        return datetime_local

    @property
    def datetime_utc(self):
        """Return a timezone-aware datetime object in UTC."""
        return datetime.fromtimestamp(self.time_seconds, timezone.utc)

    @property
    def time(self):
        if self._imitate_UUID4:
            time = NotImplemented
        else:
            time = (self.int >> 64) & OrderedUUID._TIME_MASK
        return time

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

    def _get_timestamp(self):
        """Generate a timestamp for use with an OrderedUUID."""
        timestamp = (
            (time.time_ns() // 100) + OrderedUUID._TIME_OFFSET
        ) & OrderedUUID._TIME_MASK
        if timestamp <= OrderedUUID._last_timestamp:
            timestamp = timestamp + 1

        OrderedUUID._last_timestamp = timestamp
        return timestamp
