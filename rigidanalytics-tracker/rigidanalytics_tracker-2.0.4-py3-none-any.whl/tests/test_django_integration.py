from __future__ import print_function

from datetime import datetime
import os

import django
from django.conf import settings
from django.test import LiveServerTestCase
import pytest
import requests
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


@pytest.mark.usefixtures("event_handler")
class DjangoIntegrationTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_django_app.settings'
        settings.MIDDLEWARE.append(
            'rigidanalytics_tracker.middleware.Analytics')
        settings.RIGID_ANALYTICS = {
            'PROJECT_ID': os.environ['RA_PROJECT_ID'],
            'PROJECT_TOKEN': os.environ['RA_PROJECT_TOKEN'],
            'DEBUG_DISABLE_ANALYTICS': False,
            'BACKEND_ENDPOINT': os.environ['RA_BACKEND_ENDPOINT'],
        }
        django.setup()
        super(DjangoIntegrationTests, cls).setUpClass()

    def assert_time_request_received(self, time_request_received_ns):
        """
        Assert that the time difference between `time_request_received_ns`
        and `datetime.now()` is pretty small (less than 5
        seconds). The small time difference should mean that the time
        manipulations are performed in the right way. The greater
        values should mean that something is wrong with the
        conversions from seconds to nanoseconds (or vise versa).
        """
        time_received_s = int(time_request_received_ns) / 1000000000
        received_datetime = datetime.fromtimestamp(time_received_s)
        time_diff = abs((received_datetime - datetime.now()).total_seconds())
        msg = "Time difference is greater than 5 seconds: {}".format(time_diff)
        assert time_diff < 5, msg

    def test_integration(self):
        resp = requests.get(self.live_server_url)

        url = urljoin(
            os.environ['RA_BACKEND_ENDPOINT'], os.environ['RA_PROJECT_ID'])
        resp = requests.get(url)

        assert resp.ok, resp.text
        assert resp.ok
        event = resp.json()
        event_data = event['event_data']

        assert event['project_token'] == os.environ['RA_PROJECT_TOKEN'], event
        assert self.live_server_url in event_data['full_url']
        assert event_data['response_data']['status_code'] == 200
        assert event_data['ra_session_id']

        self.assert_time_request_received(
            event_data['time_request_received_ns'])
