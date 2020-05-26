import idem_linux.corn.hw.storage.nvme
import io
import os.path
import pytest
import unittest.mock as mock

NQN_DATA = """
nqn.testnqn:234236
nqn.testnqn.test:23958
"""


class TestNvme:
    @pytest.mark.asyncio
    async def test_load_nvme_nqn(self, c_hub):
        with mock.patch.object(os.path, "exists", return_value=True):
            with mock.patch(
                "aiofiles.threadpool.sync_open", return_value=io.StringIO(NQN_DATA)
            ):
                await idem_linux.corn.hw.storage.nvme.load_nvme_nqn(c_hub)

        assert c_hub.corn.CORN.nvme_nqn == (
            "nqn.testnqn:234236",
            "nqn.testnqn.test:23958",
        )
