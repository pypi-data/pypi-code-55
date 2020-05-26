import idem_linux.corn.os.lsb_release
import pytest


class TestLsbRelease:
    @pytest.mark.asyncio
    async def test_load_lsb_release(self, c_hub):
        # TODO LSB_RELEASE needs a refactor, test it more thoroloughly when it's refactored
        await idem_linux.corn.os.lsb_release.load_lsb_release(c_hub)
