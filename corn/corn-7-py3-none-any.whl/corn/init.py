# Import python libs
import asyncio
import logging
import re

log = logging.getLogger(__name__)


def __init__(hub):
    # Set up the central location to collect all of the grain data points
    hub.corn.CORN = hub.pop.data.omap()
    hub.pop.sub.add(dyne_name="output")
    hub.pop.sub.load_subdirs(hub.corn, recurse=True)


def cli(hub):
    hub.pop.config.load(["corn", "rend"], "corn")
    hub.corn.init.standalone()

    outputter = getattr(hub, f"output.{hub.OPT.rend.output}.display")
    if hub.OPT.corn.get("grains"):
        print(
            outputter({item: hub.corn.CORN.get(item) for item in hub.OPT.corn.grains})
        )
    else:
        # Print all the corn sorted by dict key
        sorted_keys = sorted(hub.corn.CORN.keys(), key=lambda x: x.lower())
        sorted_corn = {key: hub.corn.CORN[key] for key in sorted_keys}

        print(outputter(sorted_corn))


def standalone(hub):
    """
    Run the corn sequence in a standalone fashion, useful for projects without
    a loop that want to make a temporary loop or from cli execution
    """
    hub.pop.loop.start(hub.corn.init.collect())


async def collect(hub):
    """
    Collect the corn that are presented by all of the app-merge projects that
    present corn.
    """
    await hub.corn.init.run_sub(hub.corn)
    # Load up the subs with specific corn
    await hub.corn.init.process_subs()


async def run_sub(hub, sub):
    """
    Execute the contents of a specific sub, all modules in a sub are executed
    in parallel if they are coroutines
    """
    coros = []
    for mod in sub:
        if mod.__name__ == "init":
            continue
        log.debug(f"Loading corn module {mod.__file__}")
        for func in mod:
            log.debug(f"Loading corn in {func.__name__}()")
            ret = func()
            if asyncio.iscoroutine(ret):
                coros.append(ret)
            else:
                log.warning(f"Corn collection function is not asynchronous: {func}")
    for fut in asyncio.as_completed(coros):
        await fut


async def process_subs(hub):
    """
    Process all of the nested subs found in hub.corn
    Each discovered sub is hit in lexicographical order and all plugins and functions
    exposed therein are executed in parallel if they are coroutines or as they
    are found if they are natural functions
    """
    coros = [
        hub.corn.init.run_sub(sub)
        for sub in hub.pop.sub.iter_subs(hub.corn, recurse=True)
    ]
    for fut in asyncio.as_completed(coros):
        await fut


async def clean_value(hub, key: str, val: str) -> str or None:
    """
    Clean out well-known bogus values.
    If it isn't clean (for example has value 'None'), return None.
    Otherwise, return the original value.
    """
    if val is None or not val or re.match("none", val, flags=re.IGNORECASE):
        return None
    elif re.search("serial|part|version", key):
        # 'To be filled by O.E.M.
        # 'Not applicable' etc.
        # 'Not specified' etc.
        # 0000000, 1234567 etc.
        # begone!
        if (
            re.match(r"^[0]+$", val)
            or re.match(r"[0]?1234567[8]?[9]?[0]?", val)
            or re.search(
                r"sernum|part[_-]?number|specified|filled|applicable",
                val,
                flags=re.IGNORECASE,
            )
        ):
            return None
    elif re.search("asset|manufacturer", key):
        # AssetTag0. Manufacturer04. Begone.
        if re.search(
            r"manufacturer|to be filled|available|asset|^no(ne|t)",
            val,
            flags=re.IGNORECASE,
        ):
            return None
    else:
        # map unspecified, undefined, unknown & whatever to None
        if re.search(r"to be filled", val, flags=re.IGNORECASE) or re.search(
            r"un(known|specified)|no(t|ne)? (asset|provided|defined|available|present|specified)",
            val,
            flags=re.IGNORECASE,
        ):
            return None
    return val
