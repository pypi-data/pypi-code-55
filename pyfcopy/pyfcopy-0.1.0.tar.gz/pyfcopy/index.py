
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union


class Order(Enum):
    PRE = 1
    POST = 2


def index(
        path: Union[Path, str],
        *,
        absolute: Optional[bool] = None,
        order: Optional[Order] = None,
        include_root: Optional[bool] = None,
) -> List[Path]:

    path = Path(path) if not isinstance(path, Path) else path

    absolute = False if absolute is None else absolute
    order = Order.PRE if order is None else order
    include_root = True if include_root is None else include_root

    if order not in [Order.PRE, Order.POST]:
        raise ValueError(f"Invalid order.")

    if path.is_dir():

        paths = list(path.rglob("*"))

        if include_root:
            paths.append(path)

    elif path.is_file():

        paths = [path]

    else:
        raise ValueError(f"Given path does not exist: {path}")

    if order == Order.PRE:

        paths.sort(reverse=False)

    elif order == Order.POST:

        paths.sort(reverse=True)

    else:

        raise Exception()

    if not absolute:

        # trim absolute to relative paths
        paths = [
            absolute_path.relative_to(path)
            for absolute_path in paths
        ]

    return paths
