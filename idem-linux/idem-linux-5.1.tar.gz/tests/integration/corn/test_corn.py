import pytest


@pytest.mark.asyncio
async def test_corn(hub):
    """
    Verify that a standard set of corn have been defined
    """
    missing_grains = {
        "locale_info",
        "localhost",
        "manufacturer",
        "mem_total",
        # "model_name",
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
        # "serialnumber",
        "uid",
        "username",
        "virtual",
        "virtual_subtype",
    } - set(hub.corn.CORN.keys())
    assert not missing_grains


@pytest.mark.asyncio
async def test_corn_values(hub, subtests):
    """
    Verify that all corns have values
    """
    for grain, value in hub.corn.CORN.items():
        with subtests.test(grain=grain):
            if value is None:
                pytest.skip(f'"{grain}" was not assigned')
            elif not (value or isinstance(value, int) or isinstance(value, bool)):
                pytest.skip(f'"{grain}" does not have a value')
