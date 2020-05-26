import distro
import idem_linux.corn.os.os
import pytest
import unittest.mock as mock


class TestOs:
    @pytest.mark.asyncio
    async def test_load_majorrelease(self, c_hub):
        pass

    @pytest.mark.asyncio
    async def test_load_manufacturer(self, c_hub):
        pass

    @pytest.mark.asyncio
    async def test_load_linux_distribution(self, c_hub):
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

        with mock.patch.object(
            distro, "LinuxDistribution", return_value=Distribution()
        ):
            await idem_linux.corn.os.os.load_linux_distribution(c_hub)

        assert c_hub.corn.CORN.osbuild == "testbuild"
        assert c_hub.corn.CORN.oscodename == "testcodename"
        assert c_hub.corn.CORN.osfullname == "testname"
        assert c_hub.corn.CORN.osrelease == "999.999.999"
        assert c_hub.corn.CORN.os == "testname"
        assert c_hub.corn.CORN.osrelease_info == (999, 999, 999)
        assert c_hub.corn.CORN.osmajorrelease == 10
        assert c_hub.corn.CORN.osfinger == "testname-999"
