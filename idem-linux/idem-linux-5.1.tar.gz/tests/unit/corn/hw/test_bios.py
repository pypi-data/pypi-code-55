import idem_linux.corn.hw.bios
import io
import pytest
import mock
from dict_tools import data


@pytest.mark.asyncio
async def test_load_arm_linux(mock_hub):
    mock_hub.exec.cmd.run.side_effect = [
        data.NamespaceDict({"retcode": 0, "stdout": "manufacturer=testman"}),
        data.NamespaceDict({"retcode": 0, "stdout": "DeviceDesc=testdesc"}),
        data.NamespaceDict({"retcode": 0, "stdout": "serial#=testnum"}),
    ]

    with mock.patch("shutil.which", return_value=True):
        await idem_linux.corn.hw.bios.load_arm_linux(mock_hub)

    assert mock_hub.corn.CORN.manufacturer == "testman"
    assert mock_hub.corn.CORN.serialnumber == "testnum"
    assert mock_hub.corn.CORN.productname == "testdesc"


@pytest.mark.asyncio
async def test_load_dmi(mock_hub):
    with mock.patch("os.path.exists", return_value=True):
        with mock.patch(
            "aiofiles.threadpool.sync_open",
            side_effect=[
                io.StringIO("01/01/0001"),
                io.StringIO("testversion"),
                io.StringIO("testman"),
                io.StringIO("testprod"),
                io.StringIO("testserial"),
                io.StringIO("00000000-0000-0000-0000-000000000000"),
            ],
        ):
            await idem_linux.corn.hw.bios.load_dmi(mock_hub)

    assert mock_hub.corn.CORN.biosreleasedate == "01/01/0001"
    assert mock_hub.corn.CORN.biosversion == "testversion"
    assert mock_hub.corn.CORN.manufacturer == "testman"
    assert mock_hub.corn.CORN.productname == "testprod"
    assert mock_hub.corn.CORN.serialnumber == "testserial"
    assert mock_hub.corn.CORN.uuid == "00000000-0000-0000-0000-000000000000"


@pytest.mark.asyncio
async def test_load_smbios(mock_hub):
    mock_hub.exec.smbios.get.side_effect = [
        "01/01/0001",
        "testversion",
        "testman",
        "testprod",
        "testserial",
        "00000000-0000-0000-0000-000000000000",
    ]
    with mock.patch("shutil.which", return_value=True):
        await idem_linux.corn.hw.bios.load_smbios(mock_hub)

    assert mock_hub.corn.CORN.biosreleasedate == "01/01/0001"
    assert mock_hub.corn.CORN.biosversion == "testversion"
    assert mock_hub.corn.CORN.manufacturer == "testman"
    assert mock_hub.corn.CORN.productname == "testprod"
    assert mock_hub.corn.CORN.serialnumber == "testserial"
    assert mock_hub.corn.CORN.uuid == "00000000-0000-0000-0000-000000000000"


@pytest.mark.asyncio
async def test_load_serialnumber(mock_hub):
    mock_hub.exec.smbios.get.return_value = "testserial"

    with mock.patch("shutil.which", return_value=True):
        await idem_linux.corn.hw.bios.load_serialnumber(mock_hub)

    assert mock_hub.corn.CORN.serialnumber == "testserial"
