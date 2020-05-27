from itertools import combinations
import copy
import datetime

import numpy as np
import pytest

import astropy.units as u
import gwcs.coordinate_frames as cf
from astropy.table import Table

from dkist_inventory.inventory import (
    _get_unique,
    _inventory_from_headers,
    _inventory_from_wcs,
    extract_inventory,
    process_json_headers,
)


@pytest.fixture
def headers_inventory_214():
    """A minimal collection of headers to test inventory creation."""  # noqa
    return Table(
        {
            "LINEWAV": [550, 550, 550],
            "FPA_EXPO": [10, 20, 30],
            "INSTRUME": ["VBI", "VBI", "VBI"],
            "FRIEDVAL": [1, 2, 3],
            "POL_ACC": [500, 500, 500],
            "RECIPEID": [10, 10, 10],
            "RINSTID": [20, 20, 20],
            "RRUNID": [30, 30, 30],
            "OBJECT": ["A", "B", "C"],
            "FRAMEVOL": [100, 120, 130],
            "EXPERID": ["00", "00", "00"],
            "EXPERID01": ["10", "10", "10"],
            "EXPERID02": ["20", "20", "20"],
            "PROPID": ["001", "001", "001"],
            "PROPID01": ["30", "30", "30"],
            "DSETID": ["1234", "1234", "1234"],
        }
    )


def add_mongo_fields_to_header(fits_headers: list, pop_keys: tuple = None):
    for i, header in enumerate(fits_headers):
        header["createDate"] = datetime.datetime.utcnow().isoformat()
        header["updateDate"] = datetime.datetime.utcnow().isoformat()
        header["lostDate"] = datetime.datetime.utcnow().isoformat()
        header["objectKey"] = f"proposalid/datasetid/wibble_{i}.fits"
        header["bucket"] = "data"
        header["frameStatus"] = "it_is_a_frame"
        header["_id"] = 100 + i
        for key in pop_keys:
            header.pop(key)

    return fits_headers


def non_required_keys_combinations():
    keys = ["lostDate", "updateDate"]
    combo = []
    for i in range(len(keys) + 1):
        combo += list(combinations(keys, i))
    return combo


@pytest.fixture(scope="function", params=non_required_keys_combinations())
def json_headers(headers_inventory_214, request):
    fits_headers = copy.deepcopy(_inventory_from_headers(headers_inventory_214))
    return add_mongo_fields_to_header([fits_headers], request.param)


def test_process_json_headers(json_headers, headers_inventory_214):
    filenames, fits_headers, extra_inventory = process_json_headers(
        json_headers[0]["bucket"], json_headers
    )
    assert filenames == ["wibble_0.fits"]
    assert fits_headers == [_inventory_from_headers(headers_inventory_214)]
    assert extra_inventory["original_frame_count"] == 1
    assert extra_inventory["bucket"] == "data"
    assert extra_inventory["create_date"]


def test_valid_inventory(headers_inventory_214):
    inv = _inventory_from_headers(headers_inventory_214)
    assert isinstance(inv, dict)

    assert inv["wavelengthMin"] == inv["wavelengthMax"] == 550
    assert inv["filterWavelengths"] == [550]
    assert inv["instrumentName"] == "VBI"
    assert inv["qualityAverageFriedParameter"] == np.mean([1, 2, 3])
    assert inv["qualityAveragePolarimetricAccuracy"] == 500
    assert inv["recipeId"] == 10
    assert inv["recipeInstanceId"] == 20
    assert inv["recipeRunId"] == 30
    assert set(inv["targetTypes"]) == {"A", "B", "C"}
    assert inv["primaryProposalId"] == "001"
    assert inv["primaryExperimentId"] == "00"
    assert set(inv["contributingExperimentIds"]) == {"10", "20", "00"}
    assert set(inv["contributingProposalIds"]) == {"30", "001"}


def test_inventory_from_wcs(identity_gwcs_4d):
    inv = _inventory_from_wcs(identity_gwcs_4d)
    time_frame = list(
        filter(lambda x: isinstance(x, cf.TemporalFrame), identity_gwcs_4d.output_frame.frames)
    )[0]
    shape = identity_gwcs_4d.array_shape

    # This test transform is just 0 - n_pixel in all dimensions
    assert inv["wavelengthMin"] == 0
    assert inv["wavelengthMax"] == shape[2] - 1
    assert inv["boundingBox"] == ((0, 0), (shape[0] - 1, shape[1] - 1))
    assert inv["startTime"] == time_frame.reference_frame.datetime.isoformat('T')
    assert inv["endTime"] == (time_frame.reference_frame + (shape[3] - 1) * u.s).datetime.isoformat('T')
    assert inv["stokesParameters"] == ["I"]
    assert inv["hasAllStokes"] is False


def test_inventory_from_wcs_stokes(identity_gwcs_5d_stokes):
    inv = _inventory_from_wcs(identity_gwcs_5d_stokes)
    time_frame = list(
        filter(
            lambda x: isinstance(x, cf.TemporalFrame), identity_gwcs_5d_stokes.output_frame.frames
        )
    )[0]
    shape = identity_gwcs_5d_stokes.array_shape

    # This test transform is just 0 - n_pixel in all dimensions
    assert inv["wavelengthMin"] == 0
    assert inv["wavelengthMax"] == shape[2] - 1
    assert inv["boundingBox"] == ((0, 0), (shape[0] - 1, shape[1] - 1))
    assert inv["startTime"] == time_frame.reference_frame.datetime.isoformat('T')
    assert inv["endTime"] == (time_frame.reference_frame + (shape[3] - 1) * u.s).datetime.isoformat('T')
    assert inv["stokesParameters"] == ["I", "Q", "U", "V"]
    assert inv["hasAllStokes"] is True


def test_inventory_from_wcs_2d(identity_gwcs_3d_temporal):
    inv = _inventory_from_wcs(identity_gwcs_3d_temporal)
    time_frame = list(
        filter(
            lambda x: isinstance(x, cf.TemporalFrame), identity_gwcs_3d_temporal.output_frame.frames
        )
    )[0]
    shape = identity_gwcs_3d_temporal.array_shape

    # This test transform is just 0 - n_pixel in all dimensions
    assert "wavelengthMin" not in inv
    assert "wavelengthMax" not in inv
    assert inv["boundingBox"] == ((0, 0), (shape[0] - 1, shape[1] - 1))
    assert inv["startTime"] == time_frame.reference_frame.datetime.isoformat('T')
    assert inv["endTime"] == (time_frame.reference_frame + (shape[2] - 1) * u.s).datetime.isoformat('T')
    assert inv["stokesParameters"] == ["I"]
    assert inv["hasAllStokes"] is False


def test_unique_error():
    with pytest.raises(ValueError):
        _get_unique([1, 2, 3], singular=True)

    assert _get_unique([1, 2, 3], singular=False)


def test_extract_inventory(headers_inventory_214, identity_gwcs_4d):
    inv = extract_inventory(headers_inventory_214, identity_gwcs_4d)

    time_frame = list(
        filter(lambda x: isinstance(x, cf.TemporalFrame), identity_gwcs_4d.output_frame.frames)
    )[0]
    shape = identity_gwcs_4d.array_shape

    # This test transform is just 0 - n_pixel in all dimensions
    assert inv["wavelengthMin"] == 0
    assert inv["wavelengthMax"] == shape[2] - 1
    assert inv["boundingBox"] == ((0, 0), (shape[0] - 1, shape[1] - 1))
    assert inv["startTime"] == time_frame.reference_frame.datetime.isoformat('T')
    assert inv["endTime"] == (time_frame.reference_frame + (shape[3] - 1) * u.s).datetime.isoformat('T')
    assert inv["stokesParameters"] == ["I"]
    assert inv["hasAllStokes"] is False
    assert inv["filterWavelengths"] == [550]
    assert inv["instrumentName"] == "VBI"
    assert inv["qualityAverageFriedParameter"] == np.mean([1, 2, 3])
    assert inv["qualityAveragePolarimetricAccuracy"] == 500
    assert inv["recipeId"] == 10
    assert inv["recipeInstanceId"] == 20
    assert inv["recipeRunId"] == 30
    assert set(inv["targetTypes"]) == {"A", "B", "C"}
    assert inv["primaryProposalId"] == "001"
    assert inv["primaryExperimentId"] == "00"
    assert set(inv["contributingExperimentIds"]) == {"10", "20", "00"}
    assert set(inv["contributingProposalIds"]) == {"30", "001"}


def test_extract_inventory_no_wave(headers_inventory_214, identity_gwcs_3d_temporal):
    inv = extract_inventory(headers_inventory_214, identity_gwcs_3d_temporal)

    time_frame = list(
        filter(
            lambda x: isinstance(x, cf.TemporalFrame), identity_gwcs_3d_temporal.output_frame.frames
        )
    )[0]
    shape = identity_gwcs_3d_temporal.array_shape

    # This test transform is just 0 - n_pixel in all dimensions
    assert inv["boundingBox"] == ((0, 0), (shape[0] - 1, shape[1] - 1))
    assert inv["wavelengthMin"] == inv["wavelengthMax"] == 550
    assert inv["startTime"] == time_frame.reference_frame.datetime.isoformat('T')
    assert inv["endTime"] == (time_frame.reference_frame + (shape[2] - 1) * u.s).datetime.isoformat('T')
    assert inv["stokesParameters"] == ["I"]
    assert inv["hasAllStokes"] is False
    assert inv["filterWavelengths"] == [550]
    assert inv["instrumentName"] == "VBI"
    assert inv["qualityAverageFriedParameter"] == np.mean([1, 2, 3])
    assert inv["qualityAveragePolarimetricAccuracy"] == 500
    assert inv["recipeId"] == 10
    assert inv["recipeInstanceId"] == 20
    assert inv["recipeRunId"] == 30
    assert set(inv["targetTypes"]) == {"A", "B", "C"}
    assert inv["primaryProposalId"] == "001"
    assert inv["primaryExperimentId"] == "00"
    assert set(inv["contributingExperimentIds"]) == {"10", "20", "00"}
    assert set(inv["contributingProposalIds"]) == {"30", "001"}
