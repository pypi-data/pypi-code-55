import os
import sys
import pytest
import pandas as pd
from pipemaker.filesystem import Filepath
from pipemaker.filesystem.creds import gdrive
from pipemaker.utils.defaultlog import log


def test_local_exists():
    # drive
    if sys.platform.startswith("win"):
        assert Filepath("d:").exists()
        assert not Filepath("xx:").exists()

    # folder
    folder = "temp_8387746"
    os.makedirs(folder, exist_ok=True)
    assert Filepath(folder).exists()
    if sys.platform.startswith("win"):
        assert not Filepath("d:/xxxxxxx").exists()

    # file
    assert Filepath("test_filepath.py").exists()
    assert not Filepath("xxxxxxxxx").exists()


def test_s3_exists():
    # bucket
    assert Filepath("s3://simonm3").exists()
    assert not Filepath("s3://xxxxxxxx").exists()

    # folder
    assert Filepath("s3://simonm3/donotdelete").exists()
    assert not Filepath("s3://simonm3/xxxxxxx").exists()

    # file
    assert Filepath("s3://simonm3/donotdelete/test1.txt").exists()
    assert not Filepath("s3://simonm3/donotdelete/xxxxxxxx").exists()


def test_google_exists():
    # root
    assert Filepath(f"googledrive://{gdrive()}").exists()

    # folder
    assert Filepath(f"googledrive://donotdelete{gdrive()}").exists()
    assert not Filepath(f"googledrive://xxxxxxx{gdrive()}").exists()

    # file
    assert Filepath(f"googledrive://donotdelete/test1.txt{gdrive()}").exists()
    assert not Filepath(f"googledrive://simon/xxxxxxxx.py{gdrive()}").exists()


@pytest.mark.parametrize("fs1", ["", "s3://simonm3", "googledrive:"])
@pytest.mark.parametrize("ext", [".pkl", ".csv", ".xlsx"])
def test_saveload(fs1, ext, tmp_path):

    # allows str to be passed as parameter for manual testing
    if not isinstance(tmp_path, str):
        tmp_path = tmp_path.name
    fp = Filepath(f"{fs1}/_testdata/{tmp_path}/file1{ext}")
    try:
        fp.remove()
    except:
        pass

    # define data. note explicitly set cols else in memory is range and fails assertion
    data = pd.DataFrame([dict(a=6, b=3), dict(a=7, b=9, c="hello")])

    # save
    fp.save(data)
    assert fp.exists()

    # load
    loaded = fp.load()
    assert loaded.equals(data)
