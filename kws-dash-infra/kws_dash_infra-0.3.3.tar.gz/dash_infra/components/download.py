import os
from collections import deque
from tempfile import TemporaryDirectory
from uuid import uuid4
from zipfile import ZipFile

from dash_html_components import A
from dash_infra.core import Component
from flask import send_from_directory


class DownloadZip(Component):
    def __init__(self, id, maxsize=10):
        self._upload_folder = TemporaryDirectory()
        self.upload_folder = self._upload_folder.name
        self.maxsize = maxsize
        self.tmpfiles = deque(maxlen=maxsize)
        super().__init__(id)

    def layout(self):
        return A(
            id=self.id,
            children=f"Download {self.id}",
            href="",
            className="btn-flat btn-small",
        )

    def _before_registry(self, app):
        @app.server.route(f"/download/{self.id}/<filename>")
        def send(filename):
            return send_from_directory(self.upload_folder, filename)

    def register_callback(self, callback, copy=False):
        def post_hook(state, callback_output):
            if len(self.tmpfiles) == self.maxsize:
                last_id = self.tmpfiles.popleft()
                os.remove(os.path.join(self.upload_folder, last_id))

            file_id = str(uuid4()) + ".zip"
            self.tmpfiles.append(file_id)

            with ZipFile(os.path.join(self.upload_folder, file_id), "w") as zipf:
                for fname, fcontent in callback_output.items():
                    with zipf.open(fname, "w") as fp:
                        fp.write(fcontent.encode("utf-8"))

            return f"/download/{self.id}/{file_id}"

        callback._post_function_hooks.append(post_hook)
        callback.set_outputs((self.id, "href"))
        self.callbacks.add(callback)
