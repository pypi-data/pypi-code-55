#todo file should be renamed to project.py for consistency

from copy import copy

import deepcrawl
from deepcrawl.utils import safe_string_to_datetime
from .extractions import DeepCrawlExtraction
from .project_settings import ProjectSettings

project_extra_fields = (
    "project_settings",
    "majestic_settings",
    "crawls",
    "issues",
    "schedules",
)


class DeepCrawlProject:

    def __init__(self, project_data, account_id):
        # relations
        self.id = project_data.get('id')
        self.account_id = account_id
        self.crawls = []
        self.issues = []
        self.schedules = []

        # attributes
        self.crawls_count = project_data.get('crawls_count')
        self.issues_count = project_data.get('issues_count')
        self.next_run_time = safe_string_to_datetime(project_data.get('next_run_time'))

        self.crawls_finished_last_finished_at = safe_string_to_datetime(
            project_data.get('crawls_finished_last_finished_at')
        )
        self.crawls_finished_last_progress_crawled = project_data.get('crawls_finished_last_progress_crawled')

        # project settings
        self.project_settings = ProjectSettings(project_data)
        self.majestic_settings = None

        # Create a list of custom extractions objects
        self.custom_extractions = [
            DeepCrawlExtraction(extraction_data=extraction) for extraction in project_data['custom_extractions']
        ]

    def __repr__(self):
        return f"[{self.account_id} {self.id}] {self.project_settings.name}"

    def __str__(self):
        return f"[{self.account_id} {self.id}] {self.project_settings.name}"

    @property
    def to_dict(self):
        dict_ = copy(self.__dict__)  # Replace __dict__ if immutability is added.

        # Remove extra fields
        for attr in project_extra_fields:
            dict_.pop(attr)

        dict_.update(**self.project_settings.to_dict)
        dict_['custom_extractions'] = [x.to_dict for x in self.custom_extractions]

        return dict_

    def load_crawls(self, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.crawls = connection.get_crawls(self.account_id, self.id, filters=filters)
        return self.crawls

    def load_issues(self, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.issues = connection.get_issues(self.account_id, self.id, filters=filters)
        return self.issues

    def load_schedules(self, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.schedules = connection.get_schedules(self.account_id, self.id, filters=filters)
        return self.schedules

    """
    PROJECT
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
        project = connection.get_project(self.account_id, self.id)
        for key in self.__dict__.keys():
            setattr(self, key, getattr(project, key))
        return self

    def update_settings(self, project_settings, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        project = connection.update_project_settings(self.account_id, self.id, project_settings)
        self.project_settings = project.project_setting
        return self

    def delete(self, connection=None):
        response = connection.delete_project(self.account_id, self.id)
        return response

    def add_extractions(self, connection, extractions):
        self.custom_extractions.extend(extractions)

        custom_extractions_list = []
        for custom_extraction in self.custom_extractions:
            custom_extractions_list.append({
                'label': custom_extraction.label,
                'regex': custom_extraction.regex,
                'match_number_from': custom_extraction.match_number_from,
                'match_number_to': custom_extraction.match_number_to,
                'filter': custom_extraction.filter,
                'clean_html_tags': custom_extraction.clean_html_tags
            })
        new_settings = {'custom_extractions': custom_extractions_list}
        return connection.update_project_settings(self.account_id, self.id, new_settings)

    """
    MAJESTIC
    """

    def get_majestic_settings(self, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.get_majestic_settings(self.account_id, self.id)

    def refresh_majestic_settings(self, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.majestic_settings = self.get_majestic_settings(connection=connection)
        return self.majestic_settings

    def update_majestic_settings(self, majestic_settings, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.majestic_settings = connection.update_majestic_settings(self.account_id, self.id, majestic_settings)
        return self.majestic_settings

    """
    ISSUES
    """

    def create_issue(self, issue_data, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        issue = connection.create_issue(self.account_id, self.id, issue_data)
        return issue

    def get_issue(self, issue_id, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        issue = connection.get_issue(self.account_id, self.id, issue_id)
        return issue

    def update_issue(self, issue_id, issue_data, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        issue = connection.update_issue(self.account_id, self.id, issue_id, issue_data)
        return issue

    def delete_issue(self, issue_id, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        response = connection.delete_issue(self.account_id, self.id, issue_id)
        return response

    def get_issues(self, use_cache=True, connection=None, filters=None):
        """Get issues for current project
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if use_cache and self.issues:
            return self.issues
        return self.load_issues(connection=connection, filters=filters)

    """
    CRAWLS
    """

    def start_crawl(self, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.start_crawl(self.account_id, self.id)

    def create_crawl(self, crawl_data, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.create_crawl(self.account_id, self.id, crawl_data)

    def get_crawl(self, crawl_id, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.get_crawl(self.account_id, self.id, crawl_id)

    def update_crawl(self, crawl_id, crawl_data, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        crawl = connection.update_crawl(self.account_id, self.id, crawl_id, crawl_data)
        return crawl

    def delete_crawl(self, crawl_id, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.delete_crawl(self.account_id, self.id, crawl_id)

    def get_crawls(self, use_cache=True, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if use_cache and self.crawls:
            return self.crawls
        return self.load_crawls(connection=connection, filters=filters)

    """
    SCHEDULES
    """

    def create_schedule(self, schedule_data, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.create_schedule(self.account_id, self.id, schedule_data)

    def get_schedule(self, schedule_id, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.get_schedule(self.account_id, self.id, schedule_id)

    def update_schedule(self, schedule_id, schedule_data, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        schedule = connection.update_schedule(self.account_id, self.id, schedule_id, schedule_data)
        return schedule

    def delete_schedule(self, schedule_id, connection=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.delete_schedule(self.account_id, self.id, schedule_id)

    def get_schedules(self, use_cache=True, connection=None, filters=None):
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if use_cache and self.schedules:
            return self.schedules
        return self.load_schedules(connection=connection, filters=filters)
