import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional
from .parameters.dates import DateFilter
from .api.base import DefaultAPI, APIInterface


class GSN:
    def __init__(self, api: APIInterface):
        self.api = api

    def get_sites(self) -> pd.DataFrame:
        return pd.read_json(
            self.api.sites(),
            dtype={
                "id": np.uint,
                "name": str,
                "description": str,
                "location": str,
                "insar_available": np.bool,
                "owner": str,
                "num_sensors": np.uint
            }
        )

    def get_site(self, site_id: str) -> pd.DataFrame:
        return pd.read_json(
            self.api.sites(site_id),
            dtype={
                "id": np.uint,
                "name": str,
                "description": str,
                "location": str,
                "insar_available": np.bool,
                "owner": str,
                "num_sensors": np.uint
            }
        )

    def get_raw_sp_for_site(self,
                            site_id: str,
                            start: Optional[datetime] = None,
                            end: Optional[datetime] = None) -> pd.DataFrame:
        return pd.read_json(
            self.api.sp(site_id, DateFilter(start, end)),
            dtype={
                "pot_number": np.uint,
                "time": np.datetime64,
                "potential": np.single,
                "units": str,
                "pot_notes": Optional[str],
                "site_id": np.uint
            },
            convert_dates=["time", ]
        )


def connect_to_gsn(url: str, code: str, api=DefaultAPI) -> GSN:
    return GSN(api(url, code))
