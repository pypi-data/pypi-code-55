from ._version import __rev__, __version__  # noqa: F401
from .api import (  # noqa: F401
    Asset,
    Blob,
    LocalReport,
    Markdown,
    Params,
    Plot,
    Report,
    Result,
    Script,
    Table,
    by_datapane,
    init,
    on_datapane,
)

# call init if in jupyter/interactive mode
# TODO - do we want to init only in jupyter / interactive / etc.
init()
