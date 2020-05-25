import os
from collections import deque
from tempfile import TemporaryDirectory
from uuid import uuid4
from zipfile import ZipFile

from dash_html_components import A, Div
from dash_core_components import Loading
from dash_infra.core import Component, as_callback

from flask import send_from_directory


class DownloadZip(Component):
    def __init__(self, id, maxsize=10):
        self._upload_folder = TemporaryDirectory()
        self.upload_folder = self._upload_folder.name
        self.maxsize = maxsize
        self.tmpfiles = deque(maxlen=maxsize)
        super().__init__(id)

    def layout(self):
        return Div(
            id=f"{self.id}-container",
            children=[
                A(
                    id=self.id,
                    children=f"Download {self.id}",
                    href="",
                    className="btn-flat btn-small disabled",
                ),
                Loading(id=f"{self.id}-loading", fullscreen=True),
            ],
        )

    def _before_registry(self, app):
        def send(filename):
            return send_from_directory(self.upload_folder, filename)

        send.__name__ = f"send-{self.id}"
        app.server.route(f"/download/{self.id}/<filename>")(send)

    def _enable_link(self, href):
        if href:
            return "btn-flat btn-small"
        else:
            return "btn-flat btn-small disabled"

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

            return f"/download/{self.id}/{file_id}", True

        callback._post_function_hooks.append(post_hook)
        callback.set_outputs([(self.id, "href"), (f"{self.id}-loading", "children")])

        enable_link = as_callback(
            inputs=[(f"{self.id}-loading", "children")], outputs=(self.id, "className"),
        )(self._enable_link)

        self.callbacks.add(callback)
        self.callbacks.add(enable_link)
