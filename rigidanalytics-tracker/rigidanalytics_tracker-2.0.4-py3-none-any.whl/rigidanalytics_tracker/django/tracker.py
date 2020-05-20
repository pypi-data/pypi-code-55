import re

from rigidanalytics_tracker.tracker import Tracker


class DjangoTracker(Tracker):

    @property
    def app_settings(self):
        from django.conf import settings

        return settings

    def get_app_setting(self, setting, default=None):
        if hasattr(self.app_settings, setting):
            return getattr(self.app_settings, setting)
        return default

    def extract_request_headers(self):
        regex_http_ = re.compile(r'^HTTP_.+$')
        regex_content_type = re.compile(r'^CONTENT_TYPE$')
        regex_content_length = re.compile(r'^CONTENT_LENGTH$')

        request_headers = {}
        for header in self.request.META:
            if (
                regex_http_.match(header)
                or regex_content_type.match(header)
                or regex_content_length.match(header)
            ):
                request_headers[header] = self.request.META[header]

        return request_headers

    def get_full_url(self):
        return self.request.build_absolute_uri()

    def get_session_id(self):
        return self.request.session.setdefault(
            "ra_session_id", super(DjangoTracker, self).get_session_id())

    def get_response_data(self):
        return {
            "status_code": self.response.status_code,
            "cookies": self.response.cookies,
        }
