
from tornado.web import HTTPError

from anthill.common.handler import AuthenticatedHandler
from anthill.common.access import scoped, AccessToken
from anthill.common import to_int

from . model.blog import BlogNotFound, BlogError


class BlogsHandler(AuthenticatedHandler):
    @scoped(["blog"])
    async def get(self):

        blogs = self.application.blogs
        gamespace_id = self.token.get(AccessToken.GAMESPACE)

        try:
            blogs_list = await blogs.list_blogs(gamespace_id)
        except BlogError as e:
            raise HTTPError(e.code, e.args[0])

        self.dumps({
            "blogs": [
                blog.dump()
                for blog in blogs_list
            ]
        })


class BlogHandler(AuthenticatedHandler):
    @scoped(["blog"])
    async def get(self, blog_name):

        blogs = self.application.blogs
        gamespace_id = self.token.get(AccessToken.GAMESPACE)

        limit = to_int(self.get_argument("limit", 20))

        try:
            blog = await blogs.find_blog(gamespace_id, blog_name)
        except BlogNotFound:
            raise HTTPError(404, "No such blog")
        except BlogError as e:
            raise HTTPError(e.code, e.args[0])

        try:
            blog_entries = await blogs.list_enabled_blog_entries(gamespace_id, blog.blog_id, limit=limit)
        except BlogNotFound:
            raise HTTPError(404, "No such blog")
        except BlogError as e:
            raise HTTPError(e.code, e.args[0])

        self.dumps({
            "entries": [
                entry.dump()
                for entry in blog_entries
            ]
        })


class InternalHandler(object):
    def __init__(self, application):
        self.application = application
