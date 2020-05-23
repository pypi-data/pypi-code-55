import os
import shutil

from . import settings
from . import util


def ensure():
    if not os.path.exists(settings.CACHE_DIR):
        os.makedirs(settings.CACHE_DIR)


def exists(date):
    report_path = util.report_filename(date)
    return os.path.exists(report_path)


def store(date, content):
    ensure()
    report_path = util.report_filename(date)
    with open(report_path, "wb") as f:
        f.write(content)


def clear():
    shutil.rmtree(settings.CACHE_DIR, ignore_errors=True)
