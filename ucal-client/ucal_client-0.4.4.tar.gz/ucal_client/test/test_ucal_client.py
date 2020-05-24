"""All ucal client tests."""
# pylint: disable=unused-variable

import json
import pytest

from ucal_client.base import UcalBlock, UcalState, \
    UcalConfig, UcalClientException


def test_state():
    """Test UcalState."""
    assert UcalState("Error") == UcalState.ERROR
    assert UcalState("NoPlan") == UcalState.NO_PLAN
    assert UcalState("HasPlan") == UcalState.HAS_PLAN
    assert UcalState("Executing") == UcalState.EXECUTING
    assert UcalState("Executing") != UcalState.HAS_PLAN


def test_valid_config():
    """Test UcalConfig."""
    config = UcalConfig(
        board_id="DaqBoard9000",
        time_unit_size=100,
        storage_frame_size=42
    )
    config2 = UcalConfig(
        "DaqBoard9000", 100, 42
    )

    config_repr = {
        "BoardId": "DaqBoard9000",
        "TimeUnitSize": 100.,
        "StorageFrameSize": 42
    }
    assert json.loads(config.to_message()) == config_repr
    assert json.loads(config2.to_message()) == config_repr

    config3 = UcalConfig.from_message(config2.to_message())
    assert config2 == config3


@pytest.mark.xfail(raises=UcalClientException)
def test_invalid_config():
    """Test exception raise from broken config."""
    config = UcalConfig(
        board_id=42,
        time_unit_size=100,
        storage_frame_size="DaqBoard9000"
    )
    msg = config.to_message()


def test_valid_block():
    """Test valid init for UcalBlock."""
    # Simplest block.
    block = UcalBlock(
        read_step_tu=1,
        write_step_tu=2,
        block_len_tu=10,
        voltage_0=[1, 2, 3],
        voltage_1=[4, 5, 6]
    )
    # Single channel block.
    block = UcalBlock(
        read_step_tu=1,
        write_step_tu=2,
        block_len_tu=10,
        voltage_0=[1, 2, 3],
        voltage_1=None
    )
    # Single channel block.
    block = UcalBlock(
        read_step_tu=1,
        write_step_tu=2,
        block_len_tu=0,
        voltage_0=None,
        voltage_1=[1, 2, 3]
    )
    # No-voltage block with write_step_tu > 0.
    block = UcalBlock(
        read_step_tu=1,
        write_step_tu=2,
        block_len_tu=0,
        voltage_0=None,
        voltage_1=None
    )
    # No-voltage block with write_step_tu == 0.
    # (Does not matter in this case)
    block = UcalBlock(
        read_step_tu=1,
        write_step_tu=0,
        block_len_tu=0,
        voltage_0=None,
        voltage_1=None
    )


def test_invalid_block():
    """Test invalid data for UcalBlock."""
    with pytest.raises(UcalClientException):
        # Different voltage length
        block = UcalBlock(
            read_step_tu=1,
            write_step_tu=2,
            block_len_tu=10,
            voltage_0=[1, 2, 3, 4],
            voltage_1=[1, 2, 3]
        )
    with pytest.raises(UcalClientException):
        # Negative read step
        block = UcalBlock(
            read_step_tu=-2,
            write_step_tu=2,
            block_len_tu=0,
            voltage_0=None,
            voltage_1=None
        )
    with pytest.raises(UcalClientException):
        # Zero write step with voltage
        block = UcalBlock(
            read_step_tu=1,
            write_step_tu=0,
            block_len_tu=0,
            voltage_0=[9000, 0],
            voltage_1=None
        )

    with pytest.raises(UcalClientException):
        # Empty list for voltage instead of None
        block = UcalBlock(
            read_step_tu=1,
            write_step_tu=0,
            block_len_tu=0,
            voltage_0=[9000, 0],
            voltage_1=[]
        )

