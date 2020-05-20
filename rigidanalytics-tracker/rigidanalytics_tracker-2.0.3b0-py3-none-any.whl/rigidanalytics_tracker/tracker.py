try:
    from time import time_ns
except ImportError:
    import time

    def time_ns():
        return time.time() * 10 ** 9
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
import uuid

from rigidanalytics_tracker import __version__
from rigidanalytics_tracker.transport import make_transport


DEFAULT_EVENT_TYPE = "page_view"
BACKEND_ENDPOINT_BASIS = 'https://rigidanalytics.com'


class Tracker(object):

    def set_intercepted_data(self, key, value):
        self.intercepted_data[key] = value

    def get_project_token(self):
        return self.settings.get('PROJECT_TOKEN')

    def app_settings(self):
        raise NotImplementedError()

    def get_full_url(self):
        raise NotImplementedError()

    def extract_request_headers(self):
        raise NotImplementedError()

    def get_response_data(self):
        raise NotImplementedError()

    def is_disabled(self):
        if self.settings.get("DEBUG_DISABLE_ANALYTICS") is not None:
            return self.settings["DEBUG_DISABLE_ANALYTICS"]
        else:
            return self.get_app_setting("DEBUG")

    @property
    def settings(self):
        return self.get_app_setting("RIGID_ANALYTICS", default={})

    def get_app_setting(self, setting, default=None):
        raise NotImplementedError()

    def get_session_id(self):
        return uuid.uuid4().hex

    def get_backend_endpoint(self):
        base_url = self.settings.get(
            'BACKEND_ENDPOINT', BACKEND_ENDPOINT_BASIS)
        return urljoin(base_url, self.settings.get('PROJECT_ID'))

    def init_tracking(self):
        self.transport = make_transport(self.get_backend_endpoint())
        self.intercepted_data = {
            "view_name": None,
        }
        self.start_time = None
        self.request = None
        self.response = None

    def start(self, request):
        self.init_tracking()
        self.request = request
        self.start_time = time_ns()

    def stop(self, response):
        self.response = response
        if self.start_time:
            end_time = time_ns()
            self.processing_time = end_time - self.start_time
            self.send_analytics_data()
            self.start_time = None

    def send_analytics_data(self):
        event_data = {
            "project_token": self.get_project_token(),
            "event_type": DEFAULT_EVENT_TYPE,
            "ra_tracker_version": __version__,
            "event_data": {
                "view_name": self.intercepted_data['view_name'],
                "header_data": self.extract_request_headers(),
                "full_url": self.get_full_url(),
                "ra_session_id": self.get_session_id(),
                "time_request_received_ns": self.start_time,
                "processing_time_ns": self.processing_time,
                "response_data": self.get_response_data(),
            }
        }
        self.transport.capture_event(event_data)
