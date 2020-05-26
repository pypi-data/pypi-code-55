import idem_linux.corn.proc.group
import pytest
import grp
import unittest.mock as mock


class TestGroup:
    @pytest.mark.asyncio
    async def test_load_group(self, c_hub):
        ret = lambda: 0
        ret.gr_name = "test_groupname"
        with mock.patch.object(grp, "getgrgid", return_value=ret):
            await idem_linux.corn.proc.group.load_group(c_hub)

        assert c_hub.corn.CORN.groupname == "test_groupname"
