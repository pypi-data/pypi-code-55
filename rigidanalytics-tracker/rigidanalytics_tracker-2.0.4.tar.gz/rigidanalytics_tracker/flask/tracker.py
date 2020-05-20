from rigidanalytics_tracker.tracker import Tracker


def start(sender, **extra):
    from flask import request

    tracker = sender.extensions["rigidanalytics_tracker"]
    tracker.start(request)
    tracker.set_intercepted_data("view_name", request.endpoint)


def stop(sender, **extra):
    sender.extensions["rigidanalytics_tracker"].stop(extra.get("response"))


class FlaskTracker(Tracker):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions = getattr(app, "extensions", {})
        app.extensions["rigidanalytics_tracker"] = self
        self.app = app
        self.app.before_request(self.before_request_func)
        self.init_signals()

    def before_request_func(self):
        from flask import session

        session.setdefault(
            "ra_session_id", super(FlaskTracker, self).get_session_id())

    def init_signals(self):
        from flask import signals

        if signals.signals_available and not self.is_disabled():
            self.init_request_started()
            self.init_request_finished()

    def init_request_started(self):
        from flask import request_started

        request_started.connect(start, sender=self.app)

    def init_request_finished(self):
        from flask import request_finished

        request_finished.connect(stop, sender=self.app)

    @property
    def app_settings(self):
        return self.app.config

    def get_app_setting(self, setting, default=None):
        return self.app_settings.get(setting, default)

    def get_headers(self):
        return self.request.headers

    def format_header(self, header):
        return "HTTP_{}".format(header).upper().replace("-", "_")

    def extract_request_headers(self):
        return {self.format_header(k): v for k, v in self.get_headers()}

    def get_full_url(self):
        return self.request.url

    def get_session_id(self):
        from flask import session

        return session["ra_session_id"]

    def get_response_data(self):
        return {
            "status_code": self.response.status_code,
            "cookies": self.request.cookies,
        }
