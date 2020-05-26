# -*- coding: utf-8 -*-
"""Classes and functinos for finding and managing files."""
import h5py


class WellFile:
    """Wrapper around an H5 file for a single well of data.

    Args:
        file_name: The path of the H5 file to open.

    Attributes:
        _h5_file: The opened H5 file object.
    """

    def __init__(self, file_name: str) -> None:
        self._h5_file: h5py._hl.files.File = h5py.File(
            file_name, "r",
        )

    def get_well_name(self) -> str:
        return str(self._h5_file.attrs["Well Name"])

    def get_well_index(self) -> int:
        return int(self._h5_file.attrs["Well Index (zero-based)"])
