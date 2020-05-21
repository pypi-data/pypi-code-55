from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint
from deepcrawl.downloads.download import DeepCrawlReportDownload
from .download import DeepCrawlCrawlDownloads


class DownloadConnection(ApiConnection):
    """
    CRAWL DOWNLOADS
        endpoint: crawl_downloads > accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/downloads
        http methods: GET
        methods: get_downloads

    REPORT DOWNLOAD
        endpoint: report_generate > accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}
                                    downloads
        http method: GET, POST

        endpoint: report_download > accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/
                                    downloads/{report_download_id}
        http method: GET, DELETE
    """

    """
    CRAWL DOWNLOADS
    """

    def get_crawl_downloads(self, account_id, project_id, crawl_id, filters=None):
        endpoint_url = get_api_endpoint(
            endpoint='crawl_downloads',
            account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        downloads = self.get_paginated_data(url=endpoint_url, method='get', filters=filters)

        list_of_downloads = []

        for download in downloads:
            list_of_downloads.append(
                DeepCrawlCrawlDownloads(
                    download_data=download, account_id=account_id, project_id=project_id, crawl_id=crawl_id)
            )
        return list_of_downloads

    """
    REPORT DOWNLOAD
    """

    def create_report_download(self, account_id, project_id, crawl_id, report_id, download_data):
        url = get_api_endpoint(
            "report_downloads",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, report_id=report_id
        )
        response = self.dc_request(url=url, method='post', json=download_data)
        return DeepCrawlReportDownload(
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_id=report_id, download_data=response.json()
        )

    def get_report_download(self, account_id, project_id, crawl_id, report_id, report_download_id):
        request_url = get_api_endpoint(
            "report_download",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_id=report_id, report_download_id=report_download_id
        )
        response = self.dc_request(url=request_url, method='get')
        return DeepCrawlReportDownload(
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, report_id=report_id,
            download_data=response.json()
        )

    def delete_report_download(self, account_id, project_id, crawl_id, report_id, report_download_id):
        request_url = get_api_endpoint(
            "report_download",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_id=report_id, report_download_id=report_download_id
        )
        return self.dc_request(url=request_url, method='delete')

    def get_report_downloads(self, account_id, project_id, crawl_id, report_id, filters=None):
        request_url = get_api_endpoint(
            "report_downloads",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_id=report_id
        )
        downloads_response = self.get_paginated_data(request_url, method='get', filters=filters)

        list_of_downloads = []
        for download in downloads_response:
            list_of_downloads.append(DeepCrawlReportDownload(
                project_id=project_id, account_id=account_id, crawl_id=crawl_id,
                report_id=report_id, download_data=download
            ))
        return list_of_downloads
