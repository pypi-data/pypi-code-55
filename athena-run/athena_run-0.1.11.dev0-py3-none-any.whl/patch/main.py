import patch.pandas as patch_pandas
import patch.sklearn as patch_sklearn

import logging; log = logging.getLogger(__name__)


def patch_all():
    try:
        import patch.pandas as patch_pandas
        patch_pandas.patch()
    except ModuleNotFoundError:
        log.info("Couldn't patch module %s", module.__str__())

    try:
        import patch.sklearn as patch_sklearn
        patch_sklearn.patch()
    except ModuleNotFoundError:
        log.info("Couldn't patch module %s", module.__str__())
