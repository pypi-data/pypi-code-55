class DeepCrawlReportRow:
    def __init__(self, account_id, project_id, crawl_id, report_id, row_data: dict):

        # relations
        self.id = row_data.get("_href", "").split("/")[-1]
        self.account_id = account_id
        self.project_id = project_id
        self.crawl_id = crawl_id
        self.report_id = report_id

        # attributes
        self.data = row_data.get('data')
