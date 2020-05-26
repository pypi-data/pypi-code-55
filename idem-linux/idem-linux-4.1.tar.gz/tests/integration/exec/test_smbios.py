import asyncio
import os
import pytest


class TestSmbios:
    @pytest.mark.skipif(os.getuid(), reason="Skip if not root")
    @pytest.mark.asyncio
    async def test_get(self, hub):
        await hub.exec.smbios.get("bios-version")

    @pytest.mark.skipif(os.getuid(), reason="Skip if not root")
    @pytest.mark.asyncio
    async def test_records(self, hub):
        await hub.exec.smbios.records(0)
