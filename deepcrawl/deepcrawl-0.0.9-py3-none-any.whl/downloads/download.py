from deepcrawl.utils import ImmutableAttributesMixin
from deepcrawl.utils import safe_string_to_datetime

download_init_required_fields = (
    'account_id',
    'project_id',
    'crawl_id',
    'report_id',
    'report_type',
)

download_init_optional_fields = (
    'filter',
    'output_type',  # Has a finite list of accepted values (csv_zip, compact_csv_zip, xml_zip)
)

download_mutable_fields = ()
# download object has no settings which can be defined after creation.
# Maybe these fields are settings, which should be a separate class.

# todo many fields are immutable for users, and may be blank when the object is created but could be updated by DeepCrawl after a refresh
download_immutable_fields = (
    'id',
    'status',
    'date_requested',
    'total_rows',
    'report_file',

    'report_name',  # Custom field to store the report name

    '_account_href',
    '_project_href',
    '_crawl_href',
    '_report_href',
    '_report_href_alt',
    '_report_template_href',
    '_report_type_href',
    '_href'

)

download_fields = download_init_required_fields + download_init_optional_fields + download_mutable_fields + \
                  download_immutable_fields


class DeepCrawlCrawlDownloads(ImmutableAttributesMixin):
    __slots__ = download_fields

    mutable_attributes = download_init_required_fields + download_init_optional_fields + download_mutable_fields

    def __init__(self, download_data, account_id, project_id, crawl_id):
        # relations
        self.account_id = account_id
        self.project_id = project_id
        self.crawl_id = crawl_id

        # attributes
        self.id = download_data.get('id')
        self.report_type = download_data.get('report_type')
        self.status = download_data.get('status')
        self.filter = download_data.get('filter')
        self.output_type = download_data.get('output_type')
        self.date_requested = safe_string_to_datetime(
            download_data.get('date_requested')
        )
        self.total_rows = download_data.get('total_rows')
        self.report_file = download_data.get('report_file')
        self._account_href = download_data.get('_account_href')
        self._project_href = download_data.get('_project_href')
        self._crawl_href = download_data.get('_crawl_href')
        self._report_href = download_data.get('_report_href')
        self._report_href_alt = download_data.get('_report_href_alt')
        self._report_template_href = download_data.get('_report_template_href')
        self._report_type_href = download_data.get('_report_type_href')
        self._href = download_data.get('_href')

        self.report_name = self._report_href_alt.split('/')[-1]

        super(DeepCrawlCrawlDownloads, self).__init__()  # todo Check if this is needed?

    def __repr__(self):
        return f"[{self.id}] {self.report_name.title()} {self.report_type} - {self.output_type} ({self.status})"

    def __str__(self):
        return f"[{self.id}] {self.report_name.title()} {self.report_type} - {self.output_type} ({self.status})"

    def refresh(self, connection=None):
        raise NotImplementedError

    def delete(self, connection=None):
        raise NotImplementedError


class DeepCrawlReportDownload:
    def __init__(self, account_id, project_id, crawl_id, report_id, download_data: dict):
        # relations
        self.id = download_data.get("id")
        self.account_id = account_id
        self.project_id = project_id
        self.crawl_id = crawl_id
        self.report_id = report_id

        # attributes
        self.report_type = download_data.get('report_type')
        self.status = download_data.get('status')
        self.filter = download_data.get('filter')
        self.output_type = download_data.get('output_type')
        self.date_requested = safe_string_to_datetime(download_data.get('date_requested'))
        self.total_rows = download_data.get('total_rows')

        # only in create (I think.)
        self.output_requested = download_data.get('output_requested')
