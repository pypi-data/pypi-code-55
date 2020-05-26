import idem_linux.corn.proc.user
import pytest
import os
import pwd
import unittest.mock as mock


class TestUser:
    @pytest.mark.asyncio
    async def test_load_user(self, c_hub):
        ret = 1234
        lam = lambda: 0
        lam.pw_name = "test_user"
        with mock.patch.object(os, "geteuid", return_value=ret):
            with mock.patch.object(pwd, "getpwuid", return_value=lam):
                await idem_linux.corn.proc.user.load_user(c_hub)

        assert c_hub.corn.CORN.uid == ret
        assert c_hub.corn.CORN.username == "test_user"
