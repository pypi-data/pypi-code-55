class UsageAPI(object):
    """
    Usage API
    """
    def __init__(self, rest_client):
        self.rest_client = rest_client

    def get(self):
        return self.rest_client.get("/v1/usage")
