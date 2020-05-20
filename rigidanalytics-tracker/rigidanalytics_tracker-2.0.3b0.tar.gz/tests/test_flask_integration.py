import os

import requests
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


def test_integration(flask_app_server, event_handler):
    resp = requests.get(flask_app_server)

    url = urljoin(
        os.environ['RA_BACKEND_ENDPOINT'], os.environ['RA_PROJECT_ID'])
    resp = requests.get(url)

    assert resp.ok, resp.text
    assert resp.ok
    event = resp.json()
    assert event['project_token'] == os.environ['RA_PROJECT_TOKEN']
    assert flask_app_server in event['event_data']['full_url']
    assert event['event_data']['response_data']['status_code'] == 200
