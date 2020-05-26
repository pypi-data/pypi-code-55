import idem_linux.corn.system.path
import os
import pytest
import unittest.mock as mock


class TestPath:
    @pytest.mark.asyncio
    async def test_load_cwd(self, c_hub):
        with mock.patch.object(os, "getcwd", return_value="/path"):
            await idem_linux.corn.system.path.load_cwd(c_hub)
        assert c_hub.corn.CORN.cwd == "/path"

    @pytest.mark.asyncio
    async def test_load_executable(self, c_hub):
        await idem_linux.corn.system.path.load_executable(c_hub)
        assert "python" in c_hub.corn.CORN.pythonexecutable

    @pytest.mark.asyncio
    async def test_load_path(self, c_hub):
        with mock.patch.dict(os.environ, {"PATH": "/path:/other/path"}):
            await idem_linux.corn.system.path.load_path(c_hub)
        assert c_hub.corn.CORN.path == "/path:/other/path"

    @pytest.mark.asyncio
    async def test_load_pythonpath(self, c_hub):
        await idem_linux.corn.system.path.load_pythonpath(c_hub)

    @pytest.mark.asyncio
    async def test_load_shell(self, c_hub):
        with mock.patch.dict(os.environ, {"SHELL": "/bin/test_sh"}):
            await idem_linux.corn.system.path.load_shell(c_hub)
        assert c_hub.corn.CORN.shell == "/bin/test_sh"
