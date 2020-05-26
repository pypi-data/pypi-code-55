import idem_linux.corn.system.selinux
import pytest
import shutil
import unittest.mock as mock


class TestSelinux:
    @pytest.mark.asyncio
    async def test_load_selinux(self, c_hub):
        c_hub.exec.cmd.run.side_effect = [
            c_hub.pop.data.imap({"retcode": 0}),
            c_hub.pop.data.imap({"stdout": "Enabled"}),
        ]
        with mock.patch.object(shutil, "which", return_value=True):
            await idem_linux.corn.system.selinux.load_selinux(c_hub)
        assert c_hub.corn.CORN.selinux.enabled is True
        assert c_hub.corn.CORN.selinux.enforced == "Enabled"
