
from tornado.web import HTTPError, stream_request_body

from anthill.common.handler import JsonHandler, AuthenticatedHandler
from anthill.common.access import scoped, AccessToken

from anthill.common import to_int
from anthill.common.options import options
from anthill.common.ratelimit import RateLimitExceeded

from . model.deploy import DeploymentError

import ujson
import tempfile
import os


@stream_request_body
class UploadFileHandler(AuthenticatedHandler):
    def __init__(self, application, request, **kwargs):
        super(UploadFileHandler, self).__init__(application, request, **kwargs)
        self.filename = None
        self.file = None
        self.tmp_name = None
        self.tmp_descriptor = None

    @scoped(scopes=["static_upload"])
    async def put(self):
        deployment = self.application.deployment

        self.file.close()

        gamespace_id = self.token.get(AccessToken.GAMESPACE)
        account_id = self.token.account

        try:
            url = await deployment.deploy(
                gamespace_id, account_id, self.tmp_name, self.filename)
        except DeploymentError as e:
            raise HTTPError(500, e.message)

        os.close(self.tmp_descriptor)

        self.dumps({
            "url": url
        })

    @scoped(scopes=["static_upload"])
    async def prepared(self, *args, **kwargs):

        account_id = self.token.account

        try:
            await self.application.ratelimit.limit("file_upload", account_id)
        except RateLimitExceeded:
            raise HTTPError(429, "Too many file uploads")

        self.filename = self.get_argument("filename")

        try:
            self.tmp_descriptor, self.tmp_name = tempfile.mkstemp()
            self.file = open(self.tmp_name, 'wb')
        except Exception as e:
            raise HTTPError(500, str(e))

    async def prepare(self):
        self.request.connection.set_max_body_size(to_int(options.max_file_size))
        await super(UploadFileHandler, self).prepare()

    def data_received(self, chunk):
        self.file.write(chunk)
