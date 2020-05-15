from typing import Optional
from datetime import datetime


class DateFilter:
    def __init__(self,
                 start: Optional[datetime] = None,
                 end: Optional[datetime] = None):
        self.start = start
        self.end = end

    def to_api_param(self):
        params = ""
        if self.start:
            params += f"&start_date={self.start.isoformat()}"
        if self.end:
            params += f"&end_date={self.end.isoformat()}"
        return params
