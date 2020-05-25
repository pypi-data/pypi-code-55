# pylint: disable=C0111 # (no docstrings)
# pylint: disable=C0413 # (allow importing local modules below sys path config)

import sys
import shutil
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from terodata import TeroDataClient

TEST_USER = "__TEST_USER__"
FAST_QUERY = {
    "mission": "jason3",
    "productType": "IGDR-SSHA",
    "tStart": "2016-05-01",
    "tEnd": "2016-05-10",
    "aoi": "POLYGON((2 41,3 41,3 42,2 42,2 41))",
}
CLIENT_OPTIONS = {
    "username": TEST_USER,
    "log": False,
    "poll_interval": 100,
}


def test_unauthorized():
    cli = TeroDataClient(username=None, log=False)
    with pytest.raises(Exception) as err:
        cli.get_dataset("sentinel1")
    assert "UNAUTHORIZED" in str(err.value)


# ====================================
# Dataset metadata
# ====================================
def test_get_datasets():
    cli = TeroDataClient(**CLIENT_OPTIONS)
    results = cli.get_datasets()
    assert "sentinel1" in results["datasets"]


def test_get_dataset():
    cli = TeroDataClient(**CLIENT_OPTIONS)
    results = cli.get_dataset("sentinel1")
    assert results["id"] == "sentinel1"


def test_get_dataset_not_found():
    cli = TeroDataClient(**CLIENT_OPTIONS)
    with pytest.raises(Exception) as err:
        cli.get_dataset("INVALID_DATASET")
    assert "DATASET_NOT_FOUND" in str(err.value)


# ====================================
# Queries
# ====================================
def test_create_query_job():
    cli = TeroDataClient(**CLIENT_OPTIONS)
    job = None
    try:
        job = cli.create_query_job("jason23", FAST_QUERY)
        assert job["id"]
        assert job["attrs"]
        assert job["status"]
    finally:
        if (job is not None) and "id" in job:
            cli.cancel_job(job["id"])


def test_create_query_job_dataset_not_found():
    cli = TeroDataClient(**CLIENT_OPTIONS)
    with pytest.raises(Exception) as err:
        cli.create_query_job("INVALID_DATASET", FAST_QUERY)
    assert "DATASET_NOT_FOUND" in str(err.value)


def test_create_query_job_invalid_query_product_type():
    cli = TeroDataClient(**CLIENT_OPTIONS)
    attrs = {
        "mission": "jason3",
        "productType": "INVALID_PRODUCT_TYPE",
    }
    with pytest.raises(Exception) as err:
        cli.create_query_job("jason23", attrs)
    assert "INVALID_QUERY" in str(err.value)


def test_create_query_job_invalid_query_date():
    cli = TeroDataClient(**CLIENT_OPTIONS)
    attrs = {
        "mission": "jason3",
        "tStart": "INVALID_DATE",
    }
    with pytest.raises(Exception) as err:
        cli.create_query_job("jason23", attrs)
    assert "INVALID_QUERY" in str(err.value)


def test_create_query_job_invalid_query_date_range():
    cli = TeroDataClient(**CLIENT_OPTIONS)
    attrs = {"mission": "jason3", "tStart": "2018-10-05", "tEnd": "2018-10-01"}
    with pytest.raises(Exception) as err:
        cli.create_query_job("jason23", attrs)
    assert "INVALID_QUERY" in str(err.value)


# Launch a huge query job, then cancel it
def test_create_get_cancel_query_job():
    cli = TeroDataClient(**CLIENT_OPTIONS)
    attrs = {"aoi": "POINT(2 41)"}
    job = cli.create_query_job("sentinel1", attrs)
    assert job["status"] == "RUNNING"
    id = job["id"]
    job = cli.get_job(id)
    assert job["status"] == "RUNNING"
    job = cli.cancel_job(id)
    assert job is None
    job = cli.get_job(id)
    assert job["status"] == "CANCELED"


def test_query():
    cli = TeroDataClient(**CLIENT_OPTIONS)
    attrs = {
        "mission": "jason2",
        "productType": "IGDR-SSHA",
        "tStart": "2016-05-01",
        "tEnd": "2016-05-10",
        "aoi": "POLYGON((2 41,3 41,3 42,2 42,2 41))",
    }
    job = cli.query("jason23", attrs)
    assert job["id"]
    assert job["status"] == "FINISHED"
    assert job["progress"] == 100


# ====================================
# Downloads
# ====================================
def test_create_download_job():
    job = None
    try:
        cli = TeroDataClient(**CLIENT_OPTIONS)
        granule_ids = ["JA3_IPR_2PdP070_020_20180102_083513_20180102_093126.nc"]
        job = cli.create_download_job("jason23", granule_ids)
        assert job["id"]
        assert job["maxSize"]
        assert job["status"]
    finally:
        if job:
            cli.cancel_job(job["id"])
            if "granulePaths" in job:
                granule_paths = list(job["granulePaths"].values())
                if len(granule_paths) > 0:
                    shutil.rmtree(os.path.dirname(granule_paths[0]))


def test_create_download_job_too_large():
    job = None
    try:
        cli = TeroDataClient(**CLIENT_OPTIONS)
        granule_ids = ["JA3_IPR_2PdP070_020_20180102_083513_20180102_093126.nc"]
        with pytest.raises(Exception) as err:
            job = cli.download("jason23", granule_ids, max_size=0.1)
        assert "JOB_TOO_LARGE" in str(err.value)
    finally:
        if job:
            cli.cancel_job(job["id"])
            if "granulePaths" in job:
                granule_paths = list(job["granulePaths"].values())
                if len(granule_paths) > 0:
                    shutil.rmtree(os.path.dirname(granule_paths[0]))


# Launch a large download job, then cancel it
def test_create_get_cancel_download_job():
    job = None
    try:
        cli = TeroDataClient(**CLIENT_OPTIONS)
        granule_ids = [
            "eyJncmFudWxlTmFtZSI6IlMxQl9JV19HUkRIXzFTRFZfMjAxODA5MDRUMDYwMDQ0XzIwMTgwOTA0VDA2MDEwOV8wMTI1NjFfMDE3MkNGXzcyNDciLCJwcm9jZXNzaW5nTGV2ZWwiOiJHUkRfSEQiLCJkb3dubG9hZFVybCI6Imh0dHBzOi8vZGF0YXBvb2wuYXNmLmFsYXNrYS5lZHUvR1JEX0hEL1NCL1MxQl9JV19HUkRIXzFTRFZfMjAxODA5MDRUMDYwMDQ0XzIwMTgwOTA0VDA2MDEwOV8wMTI1NjFfMDE3MkNGXzcyNDcuemlwIn0="
        ]
        job = cli.create_download_job("sentinel1-asf", granule_ids)
        assert job["status"] == "RUNNING"
        id = job["id"]
        job = cli.get_job(id)
        assert job["status"] == "RUNNING"
        job = cli.cancel_job(id)
        assert job is None
        job = cli.get_job(id)
        assert job["status"] == "CANCELED"
    finally:
        if job:
            cli.cancel_job(job["id"])
            if "granulePaths" in job:
                granule_paths = list(job["granulePaths"].values())
                if len(granule_paths) > 0:
                    shutil.rmtree(os.path.dirname(granule_paths[0]))


def test_download():
    def on_progress(job):
        if job["status"] == "RUNNING":
            cli.cancel_job(job["id"])

    job = None
    try:
        cli = TeroDataClient(**CLIENT_OPTIONS)
        granule_ids = [
            "eyJncmFudWxlTmFtZSI6IlMxQl9JV19HUkRIXzFTRFZfMjAxODA5MDRUMDYwMDQ0XzIwMTgwOTA0VDA2MDEwOV8wMTI1NjFfMDE3MkNGXzcyNDciLCJwcm9jZXNzaW5nTGV2ZWwiOiJHUkRfSEQiLCJkb3dubG9hZFVybCI6Imh0dHBzOi8vZGF0YXBvb2wuYXNmLmFsYXNrYS5lZHUvR1JEX0hEL1NCL1MxQl9JV19HUkRIXzFTRFZfMjAxODA5MDRUMDYwMDQ0XzIwMTgwOTA0VDA2MDEwOV8wMTI1NjFfMDE3MkNGXzcyNDcuemlwIn0="
        ]
        job = cli.download("sentinel1-asf", granule_ids, on_progress=on_progress)
    finally:
        if job:
            cli.cancel_job(job["id"])
            if "granulePaths" in job:
                granule_paths = list(job["granulePaths"].values())
                if len(granule_paths) > 0:
                    shutil.rmtree(os.path.dirname(granule_paths[0]))
