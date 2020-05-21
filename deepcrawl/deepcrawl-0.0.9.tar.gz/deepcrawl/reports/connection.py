from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint
from .report import DeepCrawlReport
from .report_row import DeepCrawlReportRow


class ReportConnection(ApiConnection):
    """
    REPORT
        endpoint: reports > accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports
        http methods: GET

        endpoint: report > accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}
        http methods: GET

    REPORT ROWS
        endpoint: report_rows > accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/
                                report_rows
        http methods: GET

        endpoint: report_row > accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/
                               report_rows/{report_row_id}
        http methods: GET

    """

    """
    REPORT
    """

    def get_report(self, account_id, project_id, crawl_id, report_id):
        request_url = get_api_endpoint(
            "report",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, report_id=report_id
        )
        response = self.dc_request(url=request_url, method='get')
        return DeepCrawlReport(
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_data=response.json()
        )

    def get_reports(self, account_id, project_id, crawl_id, filters=None):
        request_url = get_api_endpoint(
            "reports",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        reports_response = self.get_paginated_data(request_url, method='get', filters=filters)

        list_of_reports = []
        for report in reports_response:
            list_of_reports.append(DeepCrawlReport(
                project_id=project_id, account_id=account_id, crawl_id=crawl_id,
                report_data=report
            ))
        return list_of_reports

    def get_reports_changes(self, account_id, project_id, crawl_id, filters=None):
        request_url = get_api_endpoint(
            "reports_changes",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        reports_changes_response = self.get_paginated_data(request_url, method='get', filters=filters)
        list_of_reports_changes = []
        for report in reports_changes_response:
            list_of_reports_changes.append(DeepCrawlReport(
                project_id=project_id, account_id=account_id, crawl_id=crawl_id,
                report_data=report
            ))
        return list_of_reports_changes

    """
    REPORT ROW
    """

    def get_report_row(self, account_id, project_id, crawl_id, report_id, report_row_id):
        request_url = get_api_endpoint(
            "report_row",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_id=report_id, report_row_id=report_row_id
        )
        response = self.dc_request(url=request_url, method='get')
        return DeepCrawlReportRow(
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, report_id=report_id,
            row_data=response.json()
        )

    def get_report_rows(self, account_id, project_id, crawl_id, report_id, filters=None):
        request_url = get_api_endpoint(
            "report_rows",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_id=report_id
        )
        rows_response = self.get_paginated_data(request_url, method='get', filters=filters)

        list_of_rows = []
        for row in rows_response:
            list_of_rows.append(DeepCrawlReportRow(
                project_id=project_id, account_id=account_id, crawl_id=crawl_id,
                report_id=report_id, row_data=row
            ))
        return list_of_rows

    def get_report_row_count(self, account_id, project_id, crawl_id, report_id, filters=None):
        request_url = get_api_endpoint(
            "report_rows",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_id=report_id
        )
        response = self.dc_request(url=request_url, method='head', filters=filters)
        return response.headers.get('X-Records')
