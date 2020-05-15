import sys

from .profiler import Profiler  # noqa:F401

from ddtrace.profiling import _build


def _not_compatible_abi():
    raise ImportError(
        "Python ABI is not compatible, you need to recompile this module.\n"
        "Reinstall it with the following command:\n"
        "  pip install --no-binary ddtrace ddtrace[profiling]"
    )


if (3, 7) < _build.compiled_with <= (3, 7, 3):
    if sys.version_info[:3] > (3, 7, 3):
        _not_compatible_abi()
elif (3, 7, 3) < _build.compiled_with < (3, 8):
    if (3, 7) < sys.version_info[:3] <= (3, 7, 3):
        _not_compatible_abi()
