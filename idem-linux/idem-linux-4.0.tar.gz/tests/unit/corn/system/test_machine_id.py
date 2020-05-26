import idem_linux.corn.system.machine_id
import io
import pytest
import unittest.mock as mock


class TestMachineId:
    @pytest.mark.asyncio
    async def test_load_machine_id(self, c_hub):
        with mock.patch(
            "aiofiles.threadpool.sync_open",
            return_value=io.StringIO("999999999999999999ffffffffffffff"),
        ):
            await idem_linux.corn.system.machine_id.load_machine_id(c_hub)
        await idem_linux.corn.system.machine_id.load_machine_id(c_hub)
