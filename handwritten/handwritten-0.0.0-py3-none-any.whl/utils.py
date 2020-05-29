import os
from typing import Optional, Tuple


DEFAULT_ROOTS = (".git", "setup.py")


def project_root(path: Optional[str] = None, root_signals: Tuple[str] = DEFAULT_ROOTS) -> str:
    path = '.' if path is None else path
    path = os.path.realpath(path)
    prev_path = None
    in_dir = set(os.listdir(path))
    while path != prev_path and not any(root in in_dir for root in root_signals):
        prev_path = path
        path = os.path.dirname(path)
        in_dir = set(os.listdir(path))
    return path
