import pytest
import numpy as np
from streaming_data_types.timestamps_tdct import serialise_tdct, deserialise_tdct


class TestSerialisationTdct:
    original_entry = {
        "name": "some_name",
        "timestamps": [0, 1, 2, 3, 4],
        "sequence_counter": 42,
    }

    def test_serialises_and_deserialises_tdct_message_with_list_of_timestamps(self):
        buf = serialise_tdct(**self.original_entry)
        deserialised_tuple = deserialise_tdct(buf)

        assert deserialised_tuple.name == self.original_entry["name"]
        assert np.allclose(
            deserialised_tuple.timestamps, np.array(self.original_entry["timestamps"])
        )
        assert (
            deserialised_tuple.sequence_counter
            == self.original_entry["sequence_counter"]
        )

    def test_serialises_and_deserialises_tdct_message_with_array_of_timestamps(self):
        original_entry = {
            "name": "some_name",
            "timestamps": np.array([0, 1, 2, 3, 4]),
        }

        buf = serialise_tdct(**self.original_entry)
        deserialised_tuple = deserialise_tdct(buf)

        assert deserialised_tuple.name == original_entry["name"]
        assert np.allclose(
            deserialised_tuple.timestamps, self.original_entry["timestamps"]
        )

    def test_if_buffer_has_wrong_id_then_throws(self):
        buf = serialise_tdct(**self.original_entry)

        # Manually hack the id
        buf = bytearray(buf)
        buf[4:8] = b"1234"

        with pytest.raises(RuntimeError):
            deserialise_tdct(buf)
