import deepcrawl
from deepcrawl.utils import ImmutableAttributesMixin
from deepcrawl.utils import safe_string_to_datetime

crawl_mutable_fields = (
    "id",
    'reports',
    'reports_changes',
    'downloads',
)

crawl_immutable_fields = (
    'account_id',
    'project_id',

    'crawling_at',
    'finished_at',
    'progress_crawled',
    'progress_enqueued',
    'progress_uncrawled',
    'progress_crawling',
    'progress_finalizing',
    'progress_overall',
    'stats_crawled',
    'crawl_types',
    'stats_crawl_levels',
    'status',
    'total_step_links',
    'total_steps',
    'v1_migration_status',
    'pause_reason',
    'crawl_rate_current_limit',
    'crawl_rate',
    'crawl_rate_advanced',
    'status_internal',
    'optimus_transformed',
    'unique_pages_total',
    'levels_total',
    'all_pages_total',
    'uncrawled_urls_total',
    'crawl_compare_to_finished_at',
    'crawl_compare_to_crawl_test_site',

    '_account_href',
    '_project_href',
    '_crawl_settings_last_href',
    '_href',
    '_reports_href',
    '_sitemaps_href',
    '_statistics_href',
    '_site_explorer_href',
    '_crawl_compare_to_href',
    '_changes_href',

    'crawled_s',
)

crawl_fields = crawl_mutable_fields + crawl_immutable_fields


class DeepCrawlCrawl(ImmutableAttributesMixin):
    __slots__ = crawl_fields

    mutable_attributes = crawl_mutable_fields

    def __init__(self, crawl_data, account_id, project_id):
        # relations
        self.id = crawl_data.get('id')
        self.account_id = account_id
        self.project_id = project_id
        self.reports = []
        self.reports_changes = []

        # attributes
        self.crawling_at = safe_string_to_datetime(crawl_data.get('crawling_at'))
        self.finished_at = safe_string_to_datetime(crawl_data.get('finished_at'))
        self.progress_crawled = crawl_data.get('progress_crawled')
        self.progress_enqueued = crawl_data.get('progress_enqueued')
        self.progress_uncrawled = crawl_data.get('progress_uncrawled')
        self.progress_crawling = crawl_data.get('progress_crawling')
        self.progress_finalizing = crawl_data.get('progress_finalizing')
        self.progress_overall = crawl_data.get('progress_overall')
        self.stats_crawled = crawl_data.get('stats_crawled')
        self.crawl_types = crawl_data.get('crawl_types')
        self.stats_crawl_levels = crawl_data.get('stats_crawl_levels')
        self.status = crawl_data.get('status')
        self.total_step_links = crawl_data.get('total_step_links')
        self.total_steps = crawl_data.get('total_steps')
        self.v1_migration_status = crawl_data.get('v1_migration_status')
        self.pause_reason = crawl_data.get('pause_reason')
        self.crawl_rate_current_limit = crawl_data.get('crawl_rate_current_limit')
        self.crawl_rate = crawl_data.get('crawl_rate')
        self.crawl_rate_advanced = crawl_data.get('crawl_rate_advanced')
        self.status_internal = crawl_data.get('status_internal')
        self.optimus_transformed = crawl_data.get('optimus_transformed')
        self.unique_pages_total = crawl_data.get('unique_pages_total')
        self.levels_total = crawl_data.get('levels_total')
        self.all_pages_total = crawl_data.get('all_pages_total')
        self.uncrawled_urls_total = crawl_data.get('uncrawled_urls_total')
        self.crawl_compare_to_finished_at = safe_string_to_datetime(crawl_data.get('crawl_compare_to_finished_at'))
        self.crawl_compare_to_crawl_test_site = crawl_data.get('crawl_compare_to_crawl_test_site')
        self.crawled_s = crawl_data.get('crawled_/_s')

        self._account_href = crawl_data.get('_account_href')
        self._project_href = crawl_data.get('_project_href')
        self._crawl_settings_last_href = crawl_data.get('_crawl_settings_last_href')
        self._href = crawl_data.get('_href')
        self._reports_href = crawl_data.get('_reports_href')
        self._sitemaps_href = crawl_data.get('_sitemaps_href')
        self._statistics_href = crawl_data.get('_statistics_href')
        self._site_explorer_href = crawl_data.get('_site_explorer_href')
        self._crawl_compare_to_href = crawl_data.get('_crawl_compare_to_href')
        self._changes_href = crawl_data.get('_changes_href')

        super(DeepCrawlCrawl, self).__init__()

    def load_reports(self, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.reports = connection.get_reports(self.account_id, self.project_id, self.id, filters=filters)
        return self.reports

    def load_reports_changes(self, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.reports = connection.get_reports_changes(self.account_id, self.project_id, self.id, filters=filters)
        return self.reports

    def load_downloads(self, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.downloads = connection.get_crawl_downloads(self.account_id, self.project_id, self.id, filters=filters)
        return self.downloads

    """
    CRAWL
    """

    def save(self, connection):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        raise NotImplementedError

    def refresh(self, connection=None):
        # TODO Decide which attributes can be changed/updated
        raise NotImplementedError
        # connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        # crawl = connection.get_project(self.account_id, self.id)
        # for key in self.__dict__.keys():
        #     setattr(self, key, getattr(crawl, key))
        # return self

    def update(self, crawl_data, connection=None):
        # TODO Decide which attributes can be changed/updated
        raise NotImplementedError
        # connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        # crawl = connection.update_crawl(self.account_id, self.project_id, self.id, crawl_data)
        # for key in self.__dict__.keys():
        #     setattr(self, key, getattr(crawl, key))
        # return self

    def delete(self, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        response = connection.delete_crawl(self.account_id, self.project_id, self.id)
        del self
        return response

    """
    REPORTS
    """

    def get_report(self, report_id, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.get_report(self.account_id, self.project_id, self.id, report_id)

    def get_reports(self, use_cache=True, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if self.reports and use_cache:
            return self.reports
        return self.load_reports(connection=connection, filters=filters)

    def get_reports_changes(self, use_cache=True, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if self.reports_changes and use_cache:
            return self.reports_changes
        return self.load_reports_changes(connection=connection, filters=filters)

    """
    DOWNLOADS
    """

    def get_downloads(self, use_cache=True, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if self.downloads and use_cache:
            return self.reports_changes
        return self.load_downloads(connection=connection, filters=filters)
