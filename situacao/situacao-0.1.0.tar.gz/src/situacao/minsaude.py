import datetime

from bs4 import BeautifulSoup
import requests

from . import cache
from . import settings


def crawl():
    r = requests.get(settings.URL)
    s = BeautifulSoup(r.content, "html.parser")
    anchors = [
        a for a in s.find_all("a") if a.text.startswith(settings.LINK_TEXT_PREFIX)
    ]
    reports = {}
    for a in anchors:
        day, month, year = [int(t) for t in a.text.split(" | ")[-1].split("/")]
        if year == 2:
            year = 2020  # fixes 29th of April.
        url = a.get("href")
        date = datetime.date(year, month, day)
        if date < max(
            settings.FIRST_REPORT_WITH_MUNICIPAL_DATA, settings.FIRST_SUPPORTED_REPORT
        ):
            # there have been multiple versions prior to the 24th of March
            # but we really only care from that onwards as there is more data
            # granularity in those.
            continue
        reports[date] = url
    return reports


def maybe_fetch(reports):
    fetched = 0
    for d, url in reports.items():
        if cache.exists(d):
            continue
        r = requests.get(url)
        cache.store(d, r.content)
        fetched += 1
    return fetched
