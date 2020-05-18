from pyfileconfgui.dash_ext.query import get_triggering_id

REFRESH_INTERVAL_ID = 'navigator-refresh-interval'


def is_refresh_trigger():
    trigger_id = get_triggering_id()
    if trigger_id is None or trigger_id == REFRESH_INTERVAL_ID:
        return True
    return False
