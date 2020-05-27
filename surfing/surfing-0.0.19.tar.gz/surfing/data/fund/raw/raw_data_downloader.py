from .rq_raw_data_downloader import RqRawDataDownloader
from .em_raw_data_downloader import EmRawDataDownloader
from .web_raw_data_downloader import WebRawDataDownloader

class RawDataDownloader(object):
    def __init__(self, rq_license):
        self.rq_downloader = RqRawDataDownloader(rq_license)
        self.web_downloader = WebRawDataDownloader()
        self.em_downloader = EmRawDataDownloader()
        self.updated_count = {}

    def download(self, start_date, end_date):
        failed_tasks = []

        failed_tasks.extend(self.em_downloader.download_all(start_date, end_date))
        # If 'em_tradedates' in failed_tasks, there is no trading day between start_date and end_date
        # Stop and return
        if 'em_tradedates' in failed_tasks:
            return failed_tasks

        failed_tasks.extend(self.rq_downloader.download_all(start_date, end_date))
        failed_tasks.extend(self.web_downloader.download_all(start_date, end_date))
        
        for key, value in self.rq_downloader.updated_count.items():
            if key not in self.updated_count:
                self.updated_count[key] = value
            else:
                self.updated_count[key] += value

        for key, value in self.web_downloader.updated_count.items():
            if key not in self.updated_count:
                self.updated_count[key] = value
            else:
                self.updated_count[key] += value

        for key, value in self.em_downloader.updated_count.items():
            if key not in self.updated_count:
                self.updated_count[key] = value
            else:
                self.updated_count[key] += value

        return failed_tasks
