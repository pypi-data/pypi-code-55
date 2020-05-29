import requests


class ContentDB:
    def __init__(self):
        self.base_url = "https://content.minetest.net"

    def search(self, query, content_types=None):
        # Build the query string
        if content_types is None:
            content_types = []
        query = f"{self.base_url}/api/packages/?q={query}"
        for item in content_types:
            query = query + f"&type={item}"
        return requests.get(query).json()

    def get(self, author, package):
        return requests.get(f"{self.base_url}/api/packages/{author}/{package}/").json()

    def get_release(self, author, package):
        return requests.get(f"{self.base_url}/api/packages/{author}/{package}/release").json()
