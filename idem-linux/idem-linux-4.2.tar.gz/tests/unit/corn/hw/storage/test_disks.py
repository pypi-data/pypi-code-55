import glob
import idem_linux.corn.hw.storage.disks
import io
import os.path
import pytest
import unittest.mock as mock

DISK_DATA = """
"""


class TestDisks:
    @pytest.mark.asyncio
    async def test_load_disks(self, c_hub):
        with mock.patch.object(os.path, "exists", return_value=True):
            with mock.patch.object(
                glob,
                "glob",
                return_value=[
                    f"/sys/blcok/test-disk{num}/queue/rotational" for num in range(6)
                ],
            ):
                with mock.patch(
                    "aiofiles.threadpool.sync_open",
                    side_effect=[
                        io.StringIO("0"),  # SSD
                        io.StringIO("0"),  # SSD
                        io.StringIO("0"),  # SSD
                        io.StringIO("1"),  # HDD
                        io.StringIO("1"),  # HDD
                        io.StringIO("1"),  # HDD
                    ],
                ):
                    await idem_linux.corn.hw.storage.disks.load_disks(c_hub)

        assert c_hub.corn.CORN.SSDs == ("test-disk0", "test-disk1", "test-disk2")
        assert c_hub.corn.CORN.disks == ("test-disk3", "test-disk4", "test-disk5")
