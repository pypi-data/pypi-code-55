import idem_linux.corn.hw.storage.iscsi
import io
import os.path
import pytest
import unittest.mock as mock


ISCSI_DATA = """
InitiatorName=iqn.2005-03.org.open-iscsi:3f5058b1d0a0
InitiatorName=iqn.2006-04.com.example.node1
"""


class TestIscsi:
    @pytest.mark.asyncio
    async def test_load_iqn(self, c_hub):
        with mock.patch.object(os.path, "exists", return_value=True):
            with mock.patch(
                "aiofiles.threadpool.sync_open", return_value=io.StringIO(ISCSI_DATA)
            ):
                await idem_linux.corn.hw.storage.iscsi.load_iqn(c_hub)

        assert c_hub.corn.CORN.iscsi_iqn == (
            "iqn.2005-03.org.open-iscsi:3f5058b1d0a0",
            "iqn.2006-04.com.example.node1",
        )
