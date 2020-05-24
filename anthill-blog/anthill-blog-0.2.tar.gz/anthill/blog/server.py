
from anthill.common.options import options

from anthill.common.server import Server, init, start
from anthill.common.access import AccessToken, public
from anthill.common.keyvalue import KeyValueStorage
from anthill.common.database import Database

from . import handler as h
from . import admin
from . import options as _opts
from . model.blog import BlogsModel


class BlogServer(Server):
    # noinspection PyShadowingNames
    def __init__(self):
        super(BlogServer, self).__init__()

        self.db = Database(
            host=options.db_host,
            database=options.db_name,
            user=options.db_username,
            password=options.db_password)

        self.blogs = BlogsModel(self.db, self)

        self.cache = KeyValueStorage(
            host=options.cache_host,
            port=options.cache_port,
            db=options.cache_db,
            max_connections=options.cache_max_connections)

    def get_admin(self):
        return {
            "index": admin.RootAdminController,
            "new_blog": admin.NewBlogAdminController,
            "blog": admin.BlogAdminController,
            "blog_settings": admin.BlogSettingsAdminController,
            "new_blog_entry": admin.NewBlogEntryAdminController,
            "blog_entry": admin.BlogEntryAdminController
        }

    def get_models(self):
        return [self.blogs]

    def get_internal_handler(self):
        return h.InternalHandler(self)

    def get_metadata(self):
        return {
            "title": "Blogs",
            "description": "A service to deliver news and patch notes feed to the users inside the game",
            "icon": "rss"
        }

    def get_handlers(self):
        return [
            (r"/blogs", h.BlogsHandler),
            (r"/blog/(.*)", h.BlogHandler)
        ]


if __name__ == "__main__":
    stt = init()
    AccessToken.init([public()])
    start(BlogServer)
