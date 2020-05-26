import idem_linux.corn.proc.pid
import pytest
import os
import unittest.mock as mock


class TestPid:
    @pytest.mark.asyncio
    async def test_load_pid(self, c_hub):
        ret = 1234
        with mock.patch.object(os, "getpid", return_value=ret):
            await idem_linux.corn.proc.pid.load_pid(c_hub)

        assert c_hub.corn.CORN.pid == ret
