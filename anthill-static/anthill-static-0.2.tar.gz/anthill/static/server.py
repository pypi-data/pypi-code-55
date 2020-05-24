
from tornado.web import StaticFileHandler
from anthill.common.options import options

from anthill.common import server, handler, database, access, ratelimit

from . model.deploy import DeploymentModel
from . model.settings import SettingsModel

from . import handler
from . import admin
from . import options as _opts


class StaticServer(server.Server):
    def __init__(self):
        super(StaticServer, self).__init__()

        self.db = database.Database(
            host=options.db_host,
            database=options.db_name,
            user=options.db_username,
            password=options.db_password)

        self.deployment_settings = SettingsModel(self.db)
        self.deployment = DeploymentModel(self.deployment_settings)

        self.ratelimit = ratelimit.RateLimit({
            "file_upload": options.rate_file_upload
        })

    def get_models(self):
        return [self.deployment_settings, self.deployment]

    def get_admin(self):
        return {
            "index": admin.RootAdminController,
            "settings": admin.SettingsController
        }

    def get_metadata(self):
        return {
            "title": "Static",
            "description": "Static file hosting service for players to upload",
            "icon": "file-text-o"
        }

    def get_handlers(self):

        h = [
            (r"/upload", handler.UploadFileHandler)
        ]

        if options.serve_static:
            # noinspection PyTypeChecker
            h.append((r'/download/(.*)', StaticFileHandler, {'path': options.data_runtime_location}))

        return h


if __name__ == "__main__":
    stt = server.init()
    access.AccessToken.init([access.public()])
    server.start(StaticServer)
