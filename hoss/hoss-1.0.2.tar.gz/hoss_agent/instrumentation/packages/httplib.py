from hoss_agent.conf.constants import EVENT
from hoss_agent.instrumentation.packages.base import BaseInstrumentation, logger
from uuid import uuid4
import time
import base64
from hoss_agent.context import execution_context

try:
    from httplib import HTTPConnection, HTTPResponse  # type: ignore
except ImportError:
    from http.client import HTTPConnection, HTTPResponse


class HttpLibInstrumentation(BaseInstrumentation):
    name = "httplib"

    def instrument(self):
        _install_httplib()

def _install_httplib():
    real_request = HTTPConnection._send_request
    real_getresponse = HTTPConnection.getresponse
    real_readresponse = HTTPResponse.read

    # hook into sendrequest and set up a partial event object.
    # the event object is store in the HTTPConnection object itself so it can be referenced in getresponse below
    def _sendrequest(self, method, url, body=None, headers={},
                     encode_chunked=False):
        host = self.host
        client = execution_context.get_client()
        if client is None:
            return real_request(self, method, url, body, headers, encode_chunked)
        if 'hoss' in host:
            logger.debug('Skip host: ' + host)
            return real_request(self, method, url, body, headers, encode_chunked)

        port = self.port
        default_port = self.default_port
        real_url = url

        if not real_url.startswith(("http://", "https://")):
            real_url = "%s://%s%s%s" % (
                default_port == 443 and "https" or "http",
                host,
                port != default_port and ":%s" % port or "",
                url,
            )
        request_received_at = int(round(time.time() * 1000))

        headers = dict(headers)


        try:
            body = body.encode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            pass
        self._hoss_context = {
            "event": {
                "eventId": uuid4(),
                "request": {
                    "method": method,
                    "headers": headers,
                    "body": base64.b64encode(body) if body is not None else "",
                    "url": real_url,
                    "receivedAt": request_received_at
                }
            },
            "client": client
        }
        return real_request(self, method, url, body, headers, encode_chunked)

    # Hook into getresponse to further construct the event object that was started in _sendrequest.
    # We can't read response body here because it'll close the body. We need to hook into HTTPResponse.read for that.
    # So we have to save the event to the response object so when read is called, we can reference the event
    def getresponse(self, *args, **kwargs):
        hoss_context = getattr(self, "_hoss_context", None)

        if hoss_context is None:
            return real_getresponse(self, *args, **kwargs)
        rv = real_getresponse(self, *args, **kwargs)

        response_received_at = int(round(time.time() * 1000))
        hoss_context['event']['response'] = {
            "headers": dict(rv.headers),
            "statusCode": rv.status,
            "receivedAt": response_received_at,
            "body": ""
        }
        if ('Content-Length' in rv.headers and rv.headers['Content-Length'] == 0) or (rv.chunked and not rv.chunk_left):
            hoss_context['client'].queue(EVENT, hoss_context['event'])
            # mark the event as queued so multiple read don't result in multiple events
            hoss_context['queued'] = True
        else :
            rv._hoss_context = hoss_context
        return rv

    def readresponse(self, amt=None):
        rv = real_readresponse(self, amt)

        hoss_context = getattr(self, "_hoss_context", None)
        if hoss_context is None or 'queued' in hoss_context:
            return rv

        hoss_context['event']['response']['body'] = base64.b64encode(rv) if rv else ""
        hoss_context['client'].queue(EVENT, hoss_context['event'])
        # mark the event as queued so multiple read don't result in multiple events
        hoss_context['queued'] = True

        return rv

    HTTPConnection._send_request = _sendrequest
    HTTPConnection.getresponse = getresponse
    HTTPResponse.read = readresponse
