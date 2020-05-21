import patch.pandas as patch_pandas
import patch.sklearn as patch_sklearn

import logging; log = logging.getLogger(__name__)

def _safe_patch(module):
    try:
        module.patch()
    except ModuleNotFoundError:
        log.info("Couldn't patch module %s", module.__str__())


def patch_all():
    _safe_patch(patch_pandas)
    _safe_patch(patch_sklearn)
