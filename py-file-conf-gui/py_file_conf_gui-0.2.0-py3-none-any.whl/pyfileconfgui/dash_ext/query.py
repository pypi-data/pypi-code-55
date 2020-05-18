from typing import Optional

import dash


def get_triggering_id() -> Optional[str]:
    ctx = dash.callback_context

    if not ctx.triggered:
        trigger_id = None
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    return trigger_id
