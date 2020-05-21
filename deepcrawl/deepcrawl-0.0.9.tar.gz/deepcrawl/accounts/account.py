import deepcrawl
from deepcrawl.utils import ImmutableAttributesMixin, safe_string_to_datetime

account_mutable_fields = (
    "id",
    "projects",
    'active',
    'address_city',
    'address_state',
    'address_street',
    'address_zip',
    'api_callback',
    'api_callback_headers',
    'country',
    'custom_color_header',
    'custom_color_menu',
    'custom_domain',
    'custom_email_footer',
    'custom_logo_file',
    'custom_support_email',
    'custom_support_phone',
    'custom_skin_name',
    'finance_vat',
    'has_annual_package',
    'static_location',
    'custom_proxy',
    'custom_proxy_read_only',
    'name',
    'phone',
    'pref_email_support',
    'credits_available',
    'projects_count',
    'active_projects_count',
    'active_projects_refresh_at',
    'credit_allocation_refresh_at',
    'limit_projects_max',
    'limit_levels_max',
    'limit_pages_max',
    'timezone',
    'chargebee',
    'chargebee_subscription',
    'is_annual',
    'additional_users_available',
    'number_of_users',
    'limit_users_max',
    'portal_disabled',
    'currency',
    'account_managers',
    'splunk_enabled',
    'crawl_rate_max',
    '_primary_account_package_href',
    '_subscription_href',
    '_href',
    '_projects_href',
    '_hosted_page_href',
    '_crawls_href',
    '_credit_allocations_href',
    '_credit_reports_href',
    '_locations_href',
)

account_immutable_fields = (

)

account_fields = account_mutable_fields + account_immutable_fields


class DeepCrawlAccount(ImmutableAttributesMixin):
    __slots__ = account_fields

    mutable_attributes = account_mutable_fields

    def __init__(self, account_data):
        self.id = account_data.get("id")
        self.projects = []

        self.active = account_data.get('active')
        self.address_city = account_data.get('address_city')
        self.address_state = account_data.get('address_state')
        self.address_street = account_data.get('address_street')
        self.address_zip = account_data.get('address_zip')
        self.api_callback = account_data.get('api_callback')
        self.api_callback_headers = account_data.get('api_callback_headers')
        self.country = account_data.get('country')
        self.custom_color_header = account_data.get('custom_color_header')
        self.custom_color_menu = account_data.get('custom_color_menu')
        self.custom_domain = account_data.get('custom_domain')
        self.custom_email_footer = account_data.get('custom_email_footer')
        self.custom_logo_file = account_data.get('custom_logo_file')
        self.custom_support_email = account_data.get('custom_support_email')
        self.custom_support_phone = account_data.get('custom_support_phone')
        self.custom_skin_name = account_data.get('custom_skin_name')
        self.finance_vat = account_data.get('finance_vat')
        self.has_annual_package = account_data.get('has_annual_package')
        self.static_location = account_data.get('static_location')
        self.custom_proxy = account_data.get('custom_proxy')
        self.custom_proxy_read_only = account_data.get('custom_proxy_read_only')
        self.name = account_data.get('name')
        self.phone = account_data.get('phone')
        self.pref_email_support = account_data.get('pref_email_support')
        self.credits_available = account_data.get('credits_available')
        self.projects_count = account_data.get('projects_count')
        self.active_projects_count = account_data.get('active_projects_count')
        self.active_projects_refresh_at = account_data.get('active_projects_refresh_at')
        self.credit_allocation_refresh_at = safe_string_to_datetime(
            account_data.get('credit_allocation_refresh_at')
        )
        self.limit_projects_max = account_data.get('limit_projects_max')
        self.limit_levels_max = account_data.get('limit_levels_max')
        self.limit_pages_max = account_data.get('limit_pages_max')
        self.timezone = account_data.get('timezone')
        self.chargebee = account_data.get('chargebee')
        self.chargebee_subscription = account_data.get('chargebee_subscription')
        self.is_annual = account_data.get('is_annual')
        self.additional_users_available = account_data.get('additional_users_available')
        self.number_of_users = account_data.get('number_of_users')
        self.limit_users_max = account_data.get('limit_users_max')
        self.portal_disabled = account_data.get('portal_disabled')
        self.currency = account_data.get('currency')
        self.account_managers = account_data.get('account_managers')
        self.splunk_enabled = account_data.get('splunk_enabled')
        self.crawl_rate_max = account_data.get('crawl_rate_max')
        self._primary_account_package_href = account_data.get('_primary_account_package_href')
        self._subscription_href = account_data.get('_subscription_href')
        self._href = account_data.get('_href')
        self._projects_href = account_data.get('_projects_href')
        self._hosted_page_href = account_data.get('_hosted_page_href')
        self._crawls_href = account_data.get('_crawls_href')
        self._credit_allocations_href = account_data.get('_credit_allocations_href')
        self._credit_reports_href = account_data.get('_credit_reports_href')
        self._locations_href = account_data.get('_locations_href')

        super(DeepCrawlAccount, self).__init__()

    def load_projects(self, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.projects = connection.get_projects(self.id, filters=filters)
        return self.projects

    """
    ACCOUNT
    """

    def save(self, connection=None):
        """Makes a call to DeepCrawl in order to create this project.
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        raise NotImplementedError

    def refresh(self, connection=None):
        """Makes a call to DeepCrawl in order to refresh the current instance.
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        account = connection.get_account(self.id)
        for key in self.to_dict.keys():
            setattr(self, key, getattr(account, key))
        return self

    def update(self, account_settings, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        account = connection.update_account(self.id, account_settings)
        for key in self.to_dict.keys():
            setattr(self, key, getattr(account, key))
        return self

    def delete(self, connection=None):
        response = connection.delete_account(self.id)
        return response

    """
    PROJECTS
    """

    def get_projects(self, use_cache=True, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if use_cache and self.projects:
            return self.projects
        return self.load_projects(connection=connection, filters=filters)
