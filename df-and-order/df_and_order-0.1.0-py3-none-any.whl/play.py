import importlib
from typing import Optional

from df_and_order.helpers import get_type_from_module_path, get_file_path_from_module_path


def build_class_instance(module_path: str, init_params: Optional[dict] = None):
    """
    Create an object instance from absolute module_path string.

    Parameters
    ----------
    module_path: str
        Full module_path that is valid for your project or some external package.
    init_params: optional dict
        These parameters will be used as init parameters for the given type.

    Returns
    -------
    Some object instance
    """
    class_ = get_type_from_module_path(module_path=module_path)
    result = class_(**(init_params or {}))
    return result


import os
import datetime
class External:
    @staticmethod
    def print_ts():
        file_path = get_file_path_from_module_path(module_path='df_and_order.steps.DfCache')
        print(datetime.datetime.fromtimestamp(os.path.getmtime(file_path)))

# External.print_ts()

import time
print(time.time())