import idem_linux.corn.uname
import os
import pytest
import mock


@pytest.mark.asyncio
async def test_load_uname(mock_hub):
    with mock.patch.object(
        os,
        "uname",
        return_value=("Linux", "testname", "testrelease", "testversion", "testarch",),
    ):
        await idem_linux.corn.uname.load_uname(mock_hub)

    assert mock_hub.corn.CORN.kernel == "Linux"
    assert mock_hub.corn.CORN.nodename == "testname"
    assert mock_hub.corn.CORN.kernelrelease == "testrelease"
    assert mock_hub.corn.CORN.kernelversion == "testversion"
    assert mock_hub.corn.CORN.cpuarch == "testarch"
