import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}


class Request():
    def __init__(self):
        self.session = requests.session()

    def get(self, url):
        r = self.session.get(url, headers=headers, verify=False, allow_redirects=False)
        return r
