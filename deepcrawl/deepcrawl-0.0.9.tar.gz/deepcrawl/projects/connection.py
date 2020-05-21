from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint
from .issues import DeepCrawlIssue
from .majestic_settings import MajesticSettings
from .projects import DeepCrawlProject


class ProjectConnection(ApiConnection):
    """
    PROJECT

        endpoint: projects > accounts/{account_id}/projects
        http methods: GET, POST
        methods: get_projects, create_project

        endpoint: project > accounts/{account_id}/projects/{project_id}
        http methods: GET, PATCH, DELETE
        methods: get_project, update_project_settings, delete_project

    MAJESTIC

        endpoint: majestic > accounts/{account_id}/projects/{project_id}/majestic_configuration
        http methods: GET, PATCH
        methods: get_majestic_settings, update_majestic_settings

    ISSUES

        endpoint: issues > accounts/{account_id}/projects/{project_id}/issues
        http methods: GET, POST
        methods: get_issues, create_issue

        endpoint: issue > accounts/{account_id}/projects/{project_id}/issues/{issue_id}
        http methods: GET, PATCH, DELETE
        methods: get_issue, update_issue, delete_issue
    """

    """
    PROJECT
    """

    def create_project(self, account_id, project_settings: dict):
        endpoint_url = get_api_endpoint(endpoint='projects', account_id=account_id)
        response = self.dc_request(url=endpoint_url, method='post', json=project_settings)
        return DeepCrawlProject(project_data=response.json(), account_id=account_id)

    def get_project(self, account_id, project_id):
        endpoint_url = get_api_endpoint(endpoint='project', account_id=account_id, project_id=project_id)
        response = self.dc_request(url=endpoint_url, method='get')
        return DeepCrawlProject(project_data=response.json(), account_id=account_id)

    def update_project_settings(self, account_id, project_id, settings):
        endpoint_url = get_api_endpoint(endpoint='project', account_id=account_id, project_id=project_id)
        response = self.dc_request(url=endpoint_url, method='patch', json=settings)
        return DeepCrawlProject(project_data=response.json(), account_id=account_id)

    def delete_project(self, account_id, project_id):
        endpoint_url = get_api_endpoint(endpoint='project', account_id=account_id, project_id=project_id)
        return self.dc_request(url=endpoint_url, method='delete')

    def get_projects(self, account_id, filters=None):
        endpoint_url = get_api_endpoint(endpoint='projects', account_id=account_id)
        projects = self.get_paginated_data(url=endpoint_url, method='get', filters=filters)

        list_of_projects = []
        for project in projects:
            list_of_projects.append(
                DeepCrawlProject(project_data=project, account_id=account_id)
            )
        return list_of_projects

    """
    MAJESTIC
    """

    def get_majestic_settings(self, account_id, project_id):
        endpoint_url = get_api_endpoint(endpoint='majestic', account_id=account_id, project_id=project_id)
        response = self.dc_request(url=endpoint_url, method='get')
        return MajesticSettings(majestic_settings=response.json())

    def update_majestic_settings(self, account_id, project_id, majestic_settings):
        endpoint_url = get_api_endpoint(endpoint='majestic', account_id=account_id, project_id=project_id)
        response = self.dc_request(url=endpoint_url, method='patch', json=majestic_settings)
        return MajesticSettings(majestic_settings=response.json())

    """
    ISSUES
    """

    def create_issue(self, account_id, project_id, issue_data):
        url = get_api_endpoint("issues", account_id=account_id, project_id=project_id)
        response = self.dc_request(url=url, method='post', json=issue_data)
        return DeepCrawlIssue(account_id=account_id, project_id=project_id, issue_data=response.json())

    def get_issue(self, account_id, project_id, issue_id):
        endpoint_url = get_api_endpoint(
            endpoint='issue',
            account_id=account_id, project_id=project_id, issue_id=issue_id
        )
        response = self.dc_request(url=endpoint_url, method='get')
        return DeepCrawlIssue(issue_data=response.json(), account_id=account_id, project_id=project_id)

    def update_issue(self, account_id, project_id, issue_id, issue_data):
        endpoint_url = get_api_endpoint(
            endpoint='issue',
            account_id=account_id, project_id=project_id, issue_id=issue_id
        )
        response = self.dc_request(url=endpoint_url, method='patch', json=issue_data)
        return DeepCrawlIssue(issue_data=response.json(), account_id=account_id, project_id=project_id)

    def delete_issue(self, account_id, project_id, issue_id):
        url = get_api_endpoint("issue", account_id=account_id, project_id=project_id, issue_id=issue_id)
        return self.dc_request(url=url, method='delete')

    def get_issues(self, account_id, project_id, filters=None):
        request_url = get_api_endpoint("issues", account_id=account_id, project_id=project_id)
        issues_response = self.get_paginated_data(request_url, method='get', filters=filters)

        list_of_issues = []
        for issue in issues_response:
            list_of_issues.append(DeepCrawlIssue(issue_data=issue, project_id=project_id, account_id=account_id))
        return list_of_issues
