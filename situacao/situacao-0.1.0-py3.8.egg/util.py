import sys
import os

from . import settings


def abort(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def report_filename(date):
    return os.path.join(settings.CACHE_DIR, date.isoformat() + ".pdf")
