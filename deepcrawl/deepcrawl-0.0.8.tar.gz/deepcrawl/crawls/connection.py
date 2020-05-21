from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint
from .crawl import DeepCrawlCrawl
from .schedule import DeepCrawlSchedule


class CrawlConnection(ApiConnection):
    """
    CRAWL

        endpoint: crawls > accounts/{account_id}/projects/{project_id}/crawls
        http methods: GET, POST
        methods: get_crawls, start_crawl

        endpoint: crawl > accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}
        http methods: GET, PATCH, DELETE
        methods: get_crawl, update_crawl, delete_crawl

    SCHEDULES
        endpoint: crawl_schedules > accounts/{account_id}/projects/{project_id}/schedules
        http methods: GET, POST
        methods: create_schedule, get_schedules

        endpoint: crawl_schedule > accounts/{account_id}/projects/{project_id}/schedules/{schedule_id}
        http methods: GET, PATCH, DELETE
        methods: get_schedule, update_schedule, delete_schedule
    """

    """
    CRAWL
    """

    def start_crawl(self, account_id, project_id):
        endpoint_url = get_api_endpoint(endpoint='crawls', account_id=account_id, project_id=project_id)
        crawl_start_data = {"status": "crawling"}
        return self.dc_request(url=endpoint_url, method='post', content_type='form', data=crawl_start_data)

    def create_crawl(self, account_id, project_id, crawl_data):
        endpoint_url = get_api_endpoint(endpoint='crawls', account_id=account_id, project_id=project_id)
        response = self.dc_request(url=endpoint_url, method='post', json=crawl_data)
        return DeepCrawlCrawl(crawl_data=response.json(), account_id=account_id, project_id=project_id)

    def get_crawl(self, account_id, project_id, crawl_id):
        endpoint_url = get_api_endpoint(
            endpoint='crawl',
            account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        response = self.dc_request(url=endpoint_url, method='get')
        return DeepCrawlCrawl(crawl_data=response.json(), account_id=account_id, project_id=project_id)

    def update_crawl(self, account_id, project_id, crawl_id, crawl_data):
        endpoint_url = get_api_endpoint(
            endpoint='crawl',
            account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        response = self.dc_request(url=endpoint_url, method='patch', json=crawl_data)
        return DeepCrawlCrawl(crawl_data=response.json(), account_id=account_id, project_id=project_id)

    def delete_crawl(self, account_id, project_id, crawl_id):
        endpoint_url = get_api_endpoint(
            endpoint='crawl',
            account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        return self.dc_request(url=endpoint_url, method='delete')

    def get_crawls(self, account_id, project_id, filters=None):
        endpoint_url = get_api_endpoint(endpoint='crawls', account_id=account_id, project_id=project_id)
        crawls = self.get_paginated_data(url=endpoint_url, method='get', filters=filters)

        list_of_crawls = []
        for project in crawls:
            list_of_crawls.append(
                DeepCrawlCrawl(crawl_data=project, account_id=account_id, project_id=project_id)
            )
        return list_of_crawls

    """
    SCHEDULES
    """

    def create_schedule(self, account_id, project_id, schedule_data):
        endpoint_url = get_api_endpoint(endpoint='crawl_schedules', account_id=account_id, project_id=project_id)
        response = self.dc_request(url=endpoint_url, method='post', json=schedule_data)
        return DeepCrawlSchedule(account_id=account_id, project_id=project_id, schedule_data=response.json())

    def get_schedule(self, account_id, project_id, schedule_id):
        endpoint_url = get_api_endpoint(
            endpoint='crawl_schedule',
            account_id=account_id, project_id=project_id, schedule_id=schedule_id
        )
        response = self.dc_request(url=endpoint_url, method='get')
        return DeepCrawlSchedule(account_id=account_id, project_id=project_id, schedule_data=response.json())

    def update_schedule(self, account_id, project_id, schedule_id, schedule_data):
        endpoint_url = get_api_endpoint(
            endpoint='crawl_schedule',
            account_id=account_id, project_id=project_id, schedule_id=schedule_id
        )
        response = self.dc_request(url=endpoint_url, method='patch', json=schedule_data)
        return DeepCrawlSchedule(account_id=account_id, project_id=project_id, schedule_data=response.json())

    def delete_schedule(self, account_id, project_id, schedule_id):
        endpoint_url = get_api_endpoint(
            endpoint='crawl_schedule',
            account_id=account_id, project_id=project_id, schedule_id=schedule_id
        )
        return self.dc_request(url=endpoint_url, method='delete')

    def get_schedules(self, account_id, project_id, filters=None):
        endpoint_url = get_api_endpoint(endpoint='crawl_schedules', account_id=account_id, project_id=project_id)
        schedules = self.get_paginated_data(url=endpoint_url, method='get', filters=filters)

        list_of_schedules = []
        for schedule in schedules:
            list_of_schedules.append(
                DeepCrawlSchedule(account_id=account_id, project_id=project_id, schedule_data=schedule)
            )
        return list_of_schedules
