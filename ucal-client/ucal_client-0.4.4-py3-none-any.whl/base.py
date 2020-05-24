"""IO elements for ucal_client."""
from enum import Enum
from collections import namedtuple
import json

import numpy as np


class UcalClientException(Exception):
    """Error raised during the client usage."""


class UcalBlock:
    """
    Device read/write configuration description for a specific time period.

    Plan or program in UcalClient(and Server) is stored as a
    sequence of independent blocks(UcalBlock), where each describes what
    voltage should be applied to the sample and how data should be measured.

    :param voltage_0: list of int values in millivolts, that should be applied
      sequentially to the first heater. Pattern repeats once it reaches end.
      If set to None, no voltage is applied.
    :param voltage_1: list of int values in millivolts, that should be applied
      sequentially to the second heater. Pattern repeats once it reached end.
      If set to None, no voltage is applied.
    :param read_step_tu: read step in TimeUnit (ms by default, see UcalConfig);
      Specifies how frequently should signal be measured and saved. Must be nonzero.
    :param write_step_tu: write step in TimeUnit (ms by defaul, see UcalConfig);
      Specifies how frequently voltage from voltage_0 and voltage_1
    :param block_len_tu: duration of the UcalBlock. If set to zero, user command
      is awaited to end the block (runs infinitely).
    """

    __slots__ = [
        "read_step_tu",
        "write_step_tu",
        "block_len_tu",
        "voltage_0",
        "voltage_1"
    ]
    _VOLTAGE_MAX = 10000
    _VOLTAGE_MIN = -10000

    def __init__(self, read_step_tu, write_step_tu, block_len_tu,
                 voltage_0, voltage_1):
        """
        :param read_step_tu: int, time between adc signal measurements
            in time units.
        :param write_step_tu: int, time between dac control update in
            time units.
        :param block_len_tu: int, total duration of block in time
            units. Zero means infinite block.
        :param voltage_0: None or Iterable[int], millivolts array pattern that
            would be repeated at channel 0.
        :param voltage_1: None or Iterable[int], millivolts array pattern that
            would be repeated at channel 1.
        """
        self.read_step_tu = int(read_step_tu)
        self.write_step_tu = int(write_step_tu)
        self.block_len_tu = int(block_len_tu)
        self.voltage_0 = voltage_0
        self.voltage_1 = voltage_1
        if self.voltage_0 is not None:
            self.voltage_0 = np.array(voltage_0).astype(np.int32)
        if self.voltage_1 is not None:
            self.voltage_1 = np.array(voltage_1).astype(np.int32)
        self._validate()

    def _validate(self):
        """Validate UcalBlock attributes."""
        try:
            # all time_step params must be given and must be non-negative int
            for attr in ["read_step_tu", "write_step_tu", "block_len_tu"]:
                val = getattr(self, attr)
                assert isinstance(val, int), "'{}' must be int".format(attr)
                assert val >= 0, "'{}' must be non-negative".format(attr)
            for attr in ["voltage_0", "voltage_1"]:
                val = getattr(self, attr)
                if val is not None:
                    msg = "Use None to turn off '{}' instead of {}".format(attr, val)
                    assert len(val) != 0, msg
                    val = np.array(val)
                    setattr(self, attr, val)
                    assert np.max(val) <= self._VOLTAGE_MAX, \
                        "Voltages must be less than {}".format(self._VOLTAGE_MAX)
                    assert np.min(val) >= self._VOLTAGE_MIN, \
                        "Voltages must be higher than {}".format(self._VOLTAGE_MIN)
            if (self.voltage_0 is not None) and (self.voltage_1 is not None):
                msg = "voltage_0 and voltage_1 arrays must have same len if given"
                assert isinstance(self.voltage_0, np.ndarray), msg
                assert isinstance(self.voltage_1, np.ndarray), msg
                assert len(self.voltage_0) == len(self.voltage_1), msg
            if (self.voltage_0 is not None) or (self.voltage_0 is not None):
                msg = "write_step_tu must be non-zero when voltage is given"
                assert self.write_step_tu > 0
        except (AssertionError, TypeError) as exc:
            msg = "Invalid block configuration: {}".format(str(exc))
            raise UcalClientException(msg) from None

    def __repr__(self):
        cnum = 10
        dump = lambda x: x if len(x) < cnum else x[:cnum] + '...'
        volts_repr = "[{}; {}]".format(
            dump(str(self.voltage_0)),
            dump(str(self.voltage_1))
        )
        return "<UcalBlock:read={};write={};len={};volts={}>".format(
            self.read_step_tu, self.write_step_tu, self.block_len_tu,
            volts_repr
        )


class UcalState(Enum):
    """
    State of the Server.

    :param EXECUTING: Server is executing Block.
    :param HAVE_PLAN: Server is ready to execute Blocks
    :param NO_PLAN: Server is waiting for Blocks, user can configure device.
    :param ERROR: Server is in emergency state which needs manual fix.
    """

    EXECUTING = 'Executing'
    HAS_PLAN = 'HasPlan'
    NO_PLAN = 'NoPlan'
    ERROR = 'Error'


_UcalConfig = namedtuple(
    "UcalConfig_", [
        "board_id",
        "time_unit_size",
        "storage_frame_size"
    ]
)


class UcalConfig(_UcalConfig):
    """
    Configuration of the Server.

    :param board_id: str, name that used to init daqboard.
    :param time_unit_size: float, multiplier in relevance
        to millisecond, e.g. 10 or 0.01. All time-related values
        in block are multiplied respectively
    :param storage_frame_size: int, size of the frame in server.
        Zero means size may vary. Non-zero frame size may cause
        time measurement errors caused by resampling.
    """

    def to_message(self):
        """Serialize data in json string for server."""
        assert self.time_unit_size >= 0
        try:
            data = {
                "BoardId": str(self.board_id),
                "TimeUnitSize": float(self.time_unit_size),
                "StorageFrameSize": int(self.storage_frame_size)
            }
        except ValueError as exc:
            raise UcalClientException(str(exc))
        return json.dumps(data)

    @classmethod
    def from_message(cls, message):
        """
        Deserialize data from json string from server.

        :param message: str, serialized to json message.
        """
        data = json.loads(message)
        board_id = str(data["BoardId"])
        time_unit_size = float(data["TimeUnitSize"])
        storage_frame_size = int(data["StorageFrameSize"])
        return cls(board_id, time_unit_size, storage_frame_size)


_UcalTs = namedtuple("UcalTs", ["step", "count"])


class UcalTs(_UcalTs):
    """
    Timestamp of data from server.
    Described as the *step* (time between adjacent data points) and
    the *count* (number of steps from start time moment).
    """
