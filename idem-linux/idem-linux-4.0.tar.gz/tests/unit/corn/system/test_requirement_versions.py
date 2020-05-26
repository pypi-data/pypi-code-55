import idem_linux.corn.system.requirement_versions
import pytest
import sys


class TestRequirementVersions:
    @pytest.mark.asyncio
    async def test_load_pip_versions(self, c_hub):

        await idem_linux.corn.system.requirement_versions.load_pip_versions(c_hub)

        missing_reqs = {
            "aiofiles",
            "corn",
            "distro",
            "dnspython",
            "idem",
            "pop",
            "pop-config",
            "rend",
        } - c_hub.corn.CORN.requirement_versions._dict().keys()
        assert not missing_reqs

    @pytest.mark.asyncio
    async def test_load_python_version(self, c_hub):

        origin = sys.version_info
        sys.version_info = (1, 2, 3)
        await idem_linux.corn.system.requirement_versions.load_python_version(c_hub)
        sys.version_info = origin

        assert c_hub.corn.CORN.pythonversion == (1, 2, 3)
