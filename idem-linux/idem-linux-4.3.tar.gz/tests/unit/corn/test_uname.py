import idem_linux.corn.uname
import os
import pytest
import unittest.mock as mock


class TestUname:
    @pytest.mark.asyncio
    async def test_load_uname(self, c_hub):
        with mock.patch.object(
            os,
            "uname",
            return_value=(
                "Linux",
                "testname",
                "testrelease",
                "testversion",
                "testarch",
            ),
        ):
            await idem_linux.corn.uname.load_uname(c_hub)

        assert c_hub.corn.CORN.kernel == "Linux"
        assert c_hub.corn.CORN.nodename == "testname"
        assert c_hub.corn.CORN.kernelrelease == "testrelease"
        assert c_hub.corn.CORN.kernelversion == "testversion"
        assert c_hub.corn.CORN.cpuarch == "testarch"
