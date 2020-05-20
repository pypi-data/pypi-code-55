def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # Add another function to call from your run.py to start the app
    hub.acct.SUB_PROFILES = {}
    hub.acct.PROFILES = {}
    hub.acct.UNLOCKED = False
    hub.pop.sub.load_subdirs(hub.acct, recurse=True)


def cli(hub):
    hub.pop.config.load(["acct"], cli="acct")
    key = hub.OPT["acct"]["acct_key"]
    fn = hub.OPT["acct"]["acct_file"]
    ret = hub.acct.enc.encrypt(fn, key)
    print(ret["msg"])


def unlock(hub, fn, key):
    """
    Initialize the file read, then store the authentication data on the hub
    as hub.acct.PROFILES
    """
    hub.acct.SUB_PROFILES = {}
    hub.acct.PROFILES = hub.acct.enc.data_decrypt(fn, key)
    if "default" in hub.acct.PROFILES:
        hub.acct.DEFAULT = hub.acct.PROFILES
    else:
        hub.acct.DEFAULT = "default"
    hub.acct.UNLOCKED = True


async def gather(hub, subs, profile):
    """
    Given the named plugins and profile, execute the acct plugins to
    gather the needed profiles if data is not present for it.
    """
    ret = {}
    if not hub.acct.UNLOCKED:
        hub.log.error("Account is locked")
        return ret
    for sub in subs:
        sub_data = {}
        if sub in hub.acct.SUB_PROFILES:
            continue
        if not hasattr(hub, f'acct.{sub}'):
            hub.log.debug(f"'{sub}' does not extend acct")
            continue
        for plug in getattr(hub, f'acct.{sub}'):
            hub.log.debug(f"Gathering account information for '{sub}'")
            if "gather" in plug:
                pdata = await plug.gather()
            hub.pop.dicts.update(sub_data, pdata)
        hub.acct.SUB_PROFILES[sub] = sub_data

    for sub, sub_data in hub.acct.SUB_PROFILES.items():
        hub.log.debug(f"Reading sub profile: {sub}")
        if profile in sub_data:
            hub.log.debug("Found profile in sub_data: {profile}")
            hub.pop.dicts.update(ret, sub_data[profile])
    for sub in subs:
        hub.log.debug(f"Reading acct profile: {sub}")
        if sub in hub.acct.PROFILES:
            hub.log.debug(f"Found sub in acct.PROFILES: {profile}")
            if profile in hub.acct.PROFILES[sub]:
                hub.log.debug(f"Found account in acct.PROFILES.{sub}: {profile}")
                hub.pop.dicts.update(ret, hub.acct.PROFILES[sub][profile])
    return ret
