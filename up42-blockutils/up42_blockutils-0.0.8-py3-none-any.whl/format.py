"""
Utilities to handle exotic file formats (not GeoTiff), particularly DIMAP and NETCDF.
"""
# pylint: disable=C0411
from typing import Tuple
from pathlib import Path
import glob

import rasterio as rio
from rasterio.windows import Window
import numpy as np
from geojson import Feature

from blockutils.exceptions import UP42Error, SupportedErrors
from blockutils.datapath import set_data_path


def update_jsonfile(feature: Feature, output_name: str) -> Feature:
    """
    This method updates properties of a feature with a new file path.

    Arguments:
        feature: Input feature object.
        output_name: Output file path from main working folder (i.e. output.tif).

    Returns:
        Feature object with the updated data path to output_name.
    """
    new_feature = Feature(geometry=feature["geometry"], bbox=feature["bbox"])
    prop_dict = feature["properties"]
    meta_dict = {
        k: v
        for k, v in prop_dict.items()
        if not (k.startswith("up42.") or k.startswith("custom."))
    }
    new_feature["properties"] = meta_dict
    set_data_path(new_feature, output_name)
    return new_feature


class DimapFile:
    """
    Base class for handling DIMAP files.
    """

    def __init__(self, base_path: Path = Path("/tmp/input")):
        """
        Arguments:
            base_path: Main input working folder.
        """
        self.base_path = base_path

    def dimap_file_path(self, feature: Feature) -> Tuple[Path, Path]:
        """
        This methods returns the folder name of the MS and PAN files.
        (e.g. IMG_PHR1B_MS_001, IMG_PHR1B_PS_002)

        Arguments:
            feature: Input feature.

        Returns:
            Path to multispectral and panchromatic directory.
        """
        dimap_file_id = feature.properties.get("up42.data_path")
        dimap_path = self.base_path.joinpath(dimap_file_id)

        ms_files = glob.glob(str(dimap_path) + "/**/IMG_*_MS_*", recursive=True)
        ms_file = Path(ms_files[0]) or Path()
        pan_files = glob.glob(str(dimap_path) + "/**/IMG_*_P_*", recursive=True)
        pan_file = Path(pan_files[0]) or Path()

        return ms_file, pan_file

    def get_meta_input(self, feature: Feature, mode: str) -> Tuple[dict, dict]:
        """
        This method returns the profile of the input image.

        Arguments:
            feature: Input feature object.
            mode: `ms` or `pan` depending on the profile to be returned.

        Returns:
            Rasterio profile object.
        """
        ms_data_path, pan_data_path = self.dimap_file_path(feature)
        ms_data_name = Path(ms_data_path).joinpath(
            list(ms_data_path.glob("DIM_*"))[0].name
        )
        pan_data_name = Path(pan_data_path).joinpath(
            list(pan_data_path.glob("DIM_*"))[0].name
        )
        if mode == "ms":
            data_src = rio.open(ms_data_name)
        if mode == "pan":
            data_src = rio.open(pan_data_name)
        return data_src.profile

    def get_dim_xml_path(self, feature: Feature) -> Tuple:
        """
        This method returns the profile file of the input image.

        Arguments:
            feature: Input feature object.

        Returns:
            Paths to multispectral and panchromatic XML files.
        """
        ms_path, pan_path = self.dimap_file_path(feature)
        ms_name = Path(ms_path).joinpath(list(ms_path.glob("DIM_*"))[0].name)
        pan_name = Path(pan_path).joinpath(list(pan_path.glob("DIM_*"))[0].name)

        return ms_name, pan_name

    def read_image_as_raster(self, feature: Feature, mode: str) -> np.ndarray:
        """
        This method returns the input image in a numpy array format.

        Arguments:
            feature: Input feature object.
            mode: `ms` or `pan` depending on the array to be returned.

        Returns:
            Imagery in numpy array format.
        """
        ms_data_path, pan_data_path = self.dimap_file_path(feature)
        ms_data_name = Path(ms_data_path).joinpath(
            list(ms_data_path.glob("DIM_*"))[0].name
        )
        pan_data_name = Path(pan_data_path).joinpath(
            list(pan_data_path.glob("DIM_*"))[0].name
        )
        if mode == "ms":
            data_src = rio.open(ms_data_name)
            dtype = data_src.profile["dtype"]
            if dtype != "uint16":
                raise UP42Error(
                    SupportedErrors.WRONG_INPUT_ERROR, "Input dtype must be uint16."
                )
        if mode == "pan":
            data_src = rio.open(pan_data_name)
            dtype = data_src.profile["dtype"]
            if dtype != "uint16":
                raise UP42Error(
                    SupportedErrors.WRONG_INPUT_ERROR, "Input dtype must be uint16."
                )

        return data_src.read()

    # pylint: disable=too-many-locals
    def clip_and_read_image_as_raster(self, feature: Feature, mode: str, bounds):
        """
        This method returns the input image in a numpy array format.
        """
        ms_data_path, pan_data_path = self.dimap_file_path(feature)
        ms_data_name = Path(ms_data_path).joinpath(
            list(ms_data_path.glob("DIM_*"))[0].name
        )
        pan_data_name = Path(pan_data_path).joinpath(
            list(pan_data_path.glob("DIM_*"))[0].name
        )
        if mode == "ms":
            data_src = rio.open(ms_data_name)
            dtp = data_src.profile["dtype"]
            if dtp != "uint16":
                raise UP42Error(
                    SupportedErrors.WRONG_INPUT_ERROR, "Input dtype must be uint16."
                )
        if mode == "pan":
            data_src = rio.open(pan_data_name)
            dtp = data_src.profile["dtype"]
            if dtp != "uint16":
                raise UP42Error(
                    SupportedErrors.WRONG_INPUT_ERROR, "Input dtype must be uint16."
                )
        data_src_transform = data_src.transform
        lonmin, latmin, lonmax, latmax = bounds
        rows, cols = rio.transform.rowcol(
            data_src_transform, (lonmin, lonmax), (latmin, latmax)
        )
        clipped_data = data_src.read(
            window=Window(
                col_off=min(cols),
                row_off=min(rows),
                width=max(cols) - min(cols),
                height=max(rows) - min(rows),
            )
        )
        return (
            clipped_data,
            min(cols),
            min(rows),
            max(cols) - min(cols),
            max(rows) - min(rows),
        )


class NetCDFFile:
    """
    Base class for handling NETCDF files.
    """

    def __init__(self, base_path: Path = Path("/tmp/input")):
        """
        Arguments:
            base_path: Main input working folder.
        """
        self.base_path = base_path

    def path_to_nc_file(self, feature: Feature) -> Path:
        """
        This methods returns the file name based on the given params.

        Arguments:
            feature: Input feature object.

        Returns:
            Path to input NETCDF file.
        """
        nc_file_id = feature.properties.get("up42.data_path")
        nc_path = self.base_path.joinpath(nc_file_id)

        return nc_path
