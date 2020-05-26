import idem_linux.corn.net.realm
import pytest
import shutil
import unittest.mock as mock


class TestRealm:
    @pytest.mark.asyncio
    async def test_load_windows_domain(self, c_hub):
        c_hub.exec.cmd.run.return_value = c_hub.pop.data.imap(
            {"stdout": "TESTDOMAIN\nOTHERDOMAIN"}
        )

        with mock.patch.object(shutil, "which", return_value=True):
            await idem_linux.corn.net.realm.load_windows_domain(c_hub)

        assert c_hub.corn.CORN.windowsdomain == "TESTDOMAIN"
        assert c_hub.corn.CORN.windowsdomaintype == "Domain"
