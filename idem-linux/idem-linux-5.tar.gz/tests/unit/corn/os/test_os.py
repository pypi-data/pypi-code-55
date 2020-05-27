import distro
import idem_linux.corn.os.os
import pytest
import mock


@pytest.mark.asyncio
async def test_load_majorrelease(mock_hub):
    pass


@pytest.mark.asyncio
async def test_load_manufacturer(mock_hub):
    pass


@pytest.mark.asyncio
async def test_load_linux_distribution(mock_hub):
    class Distribution:
        def build_number(self):
            return "testbuild"

        def codename(self):
            return "testcodename"

        def name(self):
            return "testname"

        def version(self):
            return "999.999.999"

        def major_version(self):
            return "10"

    with mock.patch.object(distro, "LinuxDistribution", return_value=Distribution()):
        await idem_linux.corn.os.os.load_linux_distribution(mock_hub)

    assert mock_hub.corn.CORN.osbuild == "testbuild"
    assert mock_hub.corn.CORN.oscodename == "testcodename"
    assert mock_hub.corn.CORN.osfullname == "testname"
    assert mock_hub.corn.CORN.osrelease == "999.999.999"
    assert mock_hub.corn.CORN.os == "testname"
    assert mock_hub.corn.CORN.osrelease_info == (999, 999, 999)
    assert mock_hub.corn.CORN.osmajorrelease == 10
    assert mock_hub.corn.CORN.osfinger == "testname-999"
