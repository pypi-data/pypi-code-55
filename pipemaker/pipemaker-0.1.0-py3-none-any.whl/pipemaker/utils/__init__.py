""" generic utilities that may be used on other projects """
import unicodedata
import re
import pandas as pd
import os
import sys
import yaml
import site
from .dotdict import dotdict
import logging

log = logging.getLogger(__name__)

pd.set_option("io.excel.xlsx.reader", "openpyxl")
pd.set_option("io.excel.xlsx.writer", "openpyxl")


def load_config(path):
    """ load config file from current, home, sys.prefix/etc, sitepackages

    :return: contents as nested dict
    """
    for root in (
        [os.curdir, os.path.expanduser("~"), f"{sys.prefix}/etc",]
        + site.getsitepackages()
        + [os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))]
    ):
        try:
            filepath = f"{root}/{path}".replace("\\", "/")
            with open(filepath) as f:
                r = yaml.safe_load(f)
            log.info(f"loaded configuration {filepath}")
            return dotdict(r)
        except IOError:
            pass
    log.warning(f"unable to load {path}")
    return dotdict()


def get_name():
    """ return random name """
    # https://www.nrscotland.gov.uk/statistics-and-data/statistics/statistics-by-theme/vital-events/names
    here = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(
        f"{here}/babies-first-names-top-100-girls.csv"
    ).FirstForename.drop_duplicates()
    name = df.sample(1).iloc[0]
    return name


def slugify(value, unicode=False):
    """ convert string to standard format e.g. for use in filenames
    Convert spaces to hyphens; replace chars that are not alpha with _; lower; strip.
    
    :param value: string to be converted
    :param unicode: allow unicode chars. if False then convert to ascii.
    :return: cleaned string
    """
    value = str(value)
    if unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w]", "_", value).strip().lower()
    return value
