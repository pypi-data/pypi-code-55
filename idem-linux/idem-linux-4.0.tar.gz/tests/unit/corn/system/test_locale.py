import idem_linux.corn.system.locale
import pytest
import locale
import sys
import time
import unittest.mock as mock


class TestLocale:
    @pytest.mark.asyncio
    async def test_load_info(self, c_hub):
        with mock.patch.object(
            locale, "getdefaultlocale", return_value=("testlang", "testenc")
        ):
            with mock.patch.object(
                sys, "getdefaultencoding", return_value="testdetectenc"
            ):
                await idem_linux.corn.system.locale.load_info(c_hub)
        assert c_hub.corn.CORN.locale_info.defaultlanguage == "testlang"
        assert c_hub.corn.CORN.locale_info.defaultencoding == "testenc"
        assert c_hub.corn.CORN.locale_info.detectedencoding == "testdetectenc"

    @pytest.mark.asyncio
    async def test_load_timezone(self, c_hub):
        val = time.tzname
        time.tzname = ("ZZZ", "ZZZ")
        await idem_linux.corn.system.locale.load_timezone(c_hub)
        time.tzname = val

        assert c_hub.corn.CORN.locale_info.timezone == "ZZZ"
