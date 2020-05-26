import idem_linux.corn.os.arch
import os
import pytest
import shutil
import unittest.mock as mock


class TestArch:
    @pytest.mark.asyncio
    async def test_get_osarch_uname(self, c_hub):
        c_hub.exec.cmd.run.return_value = c_hub.pop.data.imap({"stdout": "test_arch"})

        with mock.patch.object(shutil, "which", side_effect=[True]):
            await idem_linux.corn.os.arch.get_osarch(c_hub)

        assert c_hub.corn.CORN.osarch == "test_arch"

    @pytest.mark.asyncio
    async def test_get_osarch_rpm(self, c_hub):
        c_hub.exec.cmd.run.return_value = c_hub.pop.data.imap({"stdout": "test_arch"})

        with mock.patch.dict(os.environ, {"_host_cpu": "True"}):
            with mock.patch.object(shutil, "which", side_effect=[False, True]):
                await idem_linux.corn.os.arch.get_osarch(c_hub)

        assert c_hub.corn.CORN.osarch == "test_arch"

    @pytest.mark.asyncio
    async def test_get_osarch_opkg(self, c_hub):
        c_hub.exec.cmd.run.return_value = c_hub.pop.data.imap(
            {"stdout": "foo\narch test_arch 64"}
        )

        with mock.patch.object(shutil, "which", side_effect=[False, False, True]):
            await idem_linux.corn.os.arch.get_osarch(c_hub)

        assert c_hub.corn.CORN.osarch == "test_arch"

    @pytest.mark.asyncio
    async def test_get_osarch_dpkg(self, c_hub):
        c_hub.exec.cmd.run.return_value = c_hub.pop.data.imap({"stdout": "test_arch"})

        with mock.patch.object(
            shutil, "which", side_effect=[False, False, False, True]
        ):
            await idem_linux.corn.os.arch.get_osarch(c_hub)

        assert c_hub.corn.CORN.osarch == "test_arch"

    @pytest.mark.asyncio
    async def test_get_osarch_6432(self, c_hub):
        c_hub.exec.cmd.run.return_value = c_hub.pop.data.imap({"stdout": "test_arch"})

        with mock.patch.object(
            shutil, "which", side_effect=[False, False, False, False]
        ):
            with mock.patch.dict(os.environ, {"PROCESSOR_ARCHITEW6432": "test_arch"}):
                await idem_linux.corn.os.arch.get_osarch(c_hub)

        assert c_hub.corn.CORN.osarch == "test_arch"

    @pytest.mark.asyncio
    async def test_get_osarch(self, c_hub):
        c_hub.exec.cmd.run.return_value = c_hub.pop.data.imap({"stdout": "test_arch"})

        with mock.patch.object(
            shutil, "which", side_effect=[False, False, False, False]
        ):
            with mock.patch.dict(os.environ, {"PROCESSOR_ARCHITECTURE": "test_arch"}):
                await idem_linux.corn.os.arch.get_osarch(c_hub)

        assert c_hub.corn.CORN.osarch == "test_arch"
