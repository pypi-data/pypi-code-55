"""
registration_params
===================

Module to calculate volume of brain regions
"""

import numpy as np
import logging

from brainio import brainio
from imlib.pandas.misc import initialise_df

from neuro.atlas_tools.array import lateralise_atlas
from neuro.structures.IO import load_structures_as_df
from neuro.atlas_tools.misc import get_voxel_volume
from neuro.structures.structures_tree import (
    atlas_value_to_name,
    UnknownAtlasValue,
)


def get_lateralised_atlas(
    atlas_path,
    hemispheres_path,
    left_hemisphere_value=2,
    right_hemisphere_value=1,
):
    atlas = brainio.load_any(atlas_path)
    hemispheres = brainio.load_any(hemispheres_path)

    atlas_left, atlas_right = lateralise_atlas(
        atlas,
        hemispheres,
        left_hemisphere_value=left_hemisphere_value,
        right_hemisphere_value=right_hemisphere_value,
    )

    unique_vals_left, counts_left = np.unique(atlas_left, return_counts=True)
    unique_vals_right, counts_right = np.unique(
        atlas_right, return_counts=True
    )
    return unique_vals_left, unique_vals_right, counts_left, counts_right


def add_structure_volume_to_df(
    df,
    atlas_value,
    structures_reference_df,
    unique_vals_left,
    unique_vals_right,
    counts_left,
    counts_right,
    voxel_volume,
):

    name = atlas_value_to_name(atlas_value, structures_reference_df)

    try:
        left_index = np.where(unique_vals_left == atlas_value)[0][0]
        left_volume = counts_left[left_index] * voxel_volume
    except IndexError:
        logging.warning(
            "Atlas value: {} not found in registered atlas. "
            "Setting registered volume to 0.".format(atlas_value)
        )
        left_volume = 0

    try:
        right_index = np.where(unique_vals_right == atlas_value)[0][0]
        right_volume = counts_right[right_index] * voxel_volume
    except IndexError:
        logging.warning(
            "Atlas value: {} not found in registered atlas. "
            "Setting registered volume to 0.".format(atlas_value)
        )
        right_volume = 0

    df = df.append(
        {
            "structure_name": name,
            "left_volume_mm3": left_volume,
            "right_volume_mm3": right_volume,
            "total_volume_mm3": left_volume + right_volume,
        },
        ignore_index=True,
    )
    return df


def calculate_volumes(
    atlas_path,
    hemispheres_path,
    atlas_structures_path,
    registration_config,
    output_file,
    left_hemisphere_value=2,
    right_hemisphere_value=1,
):
    (
        unique_vals_left,
        unique_vals_right,
        counts_left,
        counts_right,
    ) = get_lateralised_atlas(
        atlas_path,
        hemispheres_path,
        left_hemisphere_value=left_hemisphere_value,
        right_hemisphere_value=right_hemisphere_value,
    )

    structures_reference_df = load_structures_as_df(atlas_structures_path)
    voxel_volume = get_voxel_volume(registration_config)
    voxel_volume_in_mm = voxel_volume / (1000 ** 3)
    df = initialise_df(
        "structure_name",
        "left_volume_mm3",
        "right_volume_mm3",
        "total_volume_mm3",
    )
    for atlas_value in unique_vals_left:
        if atlas_value is not 0:  # outside brain
            try:
                df = add_structure_volume_to_df(
                    df,
                    atlas_value,
                    structures_reference_df,
                    unique_vals_left,
                    unique_vals_right,
                    counts_left,
                    counts_right,
                    voxel_volume_in_mm,
                )
            except UnknownAtlasValue:
                print(
                    "Value: {} is not in the atlas structure reference file. "
                    "Not calculating the volume".format(atlas_value)
                )

    df.to_csv(output_file, index=False)
