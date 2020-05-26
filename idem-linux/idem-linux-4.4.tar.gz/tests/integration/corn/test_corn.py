import pytest


class TestCorn:
    @pytest.mark.asyncio
    async def test_corn(self, hub):
        """
        Verify that a standard set of corn have been defined
        """
        missing_grains = {
            "locale_info",
            "localhost",
            "manufacturer",
            "mem_total",
            "model_name",
            "nodename",
            "num_cpus",
            "num_gpus",
            "os",
            "os_family",
            "osarch",
            "osbuild",
            "oscodename",
            "osfinger",
            "osfullname",
            "osmajorrelease",
            "osrelease",
            "osrelease_info",
            "path",
            "pid",
            "productname",
            "ps",
            "pythonexecutable",
            "pythonpath",
            "pythonversion",
            "requirement_versions",
            "shell",
            "SSDs",
            "swap_total",
            "serialnumber",
            "uid",
            "username",
        } - set(hub.corn.CORN.keys())
        assert not missing_grains

    @pytest.mark.asyncio
    async def test_corn_values(self, hub, subtests):
        """
        Verify that all corns have values
        """
        for grain, value in hub.corn.CORN.items():
            with subtests.test(grain=grain):
                if value is None:
                    pytest.fail(f'"{grain}" was not assigned')
                elif not (value or isinstance(value, int) or isinstance(value, bool)):
                    pytest.skip(f'"{grain}" does not have a value')
