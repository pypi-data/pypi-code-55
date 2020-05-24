from uuid import uuid4
from functools import wraps
import requests
from flask import request, g
import sentry_sdk


def flask_sentry_requests_distributed_tracing(app):
    with app.app_context():
        # NOTE: Setting here so it is present in crons/workers running in flask context
        g.x_request_id = str(uuid4())

        @app.before_request
        def _persist_request_id():
            request_id = str(request.headers.get("x-request-id") or uuid4())
            g.x_request_id = request_id

        @app.before_request
        def _setup_sentry_scope():
            with sentry_sdk.configure_scope() as scope:
                request_id = g.x_request_id
                scope.set_tag("request_id", request_id)

        def _header_wrapper(f):
            @wraps(f)
            def wrapper(*args, **kwgs):
                headers = kwgs.pop("headers", None) or {}
                headers["x-request-id"] = g.get("x_request_id", None) or str(uuid4())
                return f(*args, headers=headers, **kwgs)

            return wrapper

        requests.request = _header_wrapper(requests.request)
        requests.get = _header_wrapper(requests.get)
        requests.options = _header_wrapper(requests.options)
        requests.head = _header_wrapper(requests.head)
        requests.post = _header_wrapper(requests.post)
        requests.put = _header_wrapper(requests.put)
        requests.patch = _header_wrapper(requests.patch)
        requests.delete = _header_wrapper(requests.delete)
        requests.Session.request = _header_wrapper(requests.Session.request)
        requests.Session.get = _header_wrapper(requests.Session.get)
        requests.Session.options = _header_wrapper(requests.Session.options)
        requests.Session.head = _header_wrapper(requests.Session.head)
        requests.Session.post = _header_wrapper(requests.Session.post)
        requests.Session.put = _header_wrapper(requests.Session.put)
        requests.Session.patch = _header_wrapper(requests.Session.patch)
        requests.Session.delete = _header_wrapper(requests.Session.delete)
