from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint
from .account import DeepCrawlAccount


class AccountConnection(ApiConnection):
    """
    ACCOUNT

        endpoint: accounts > accounts
        http methods: GET, POST
        methods: get_accounts, create_account

        endpoint: account > accounts/{account_id}
        http methods: GET, PATCH, DELETE
        methods: get_account, update_account, delete_account
    """

    def create_account(self, account_data):
        endpoint_url = get_api_endpoint(endpoint='accounts')
        response = self.dc_request(url=endpoint_url, method='post', json=account_data)
        return DeepCrawlAccount(account_data=response.json())

    def get_account(self, account_id):
        endpoint_url = get_api_endpoint(endpoint='account', account_id=account_id)
        response = self.dc_request(url=endpoint_url, method='get')
        return DeepCrawlAccount(account_data=response.json())

    def update_account(self, account_id, account_data):
        endpoint_url = get_api_endpoint(endpoint='account', account_id=account_id)
        response = self.dc_request(url=endpoint_url, method='patch', json=account_data)
        return DeepCrawlAccount(account_data=response.json())

    def delete_account(self, account_id):
        raise NotImplementedError
        # endpoint_url = get_api_endpoint(endpoint='account', account_id=account_id)
        # return self.dc_request(url=endpoint_url, method='delete')

    def get_accounts(self, filters=None):
        endpoint_url = get_api_endpoint(endpoint='accounts')
        accounts = self.get_paginated_data(url=endpoint_url, method='get', filters=filters)

        list_of_accounts = []
        for account in accounts:
            list_of_accounts.append(
                DeepCrawlAccount(account_data=account)
            )
        return list_of_accounts

    # TODO Add methods for project interactions
