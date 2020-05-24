from anthill.common.validate import validate
from anthill.common import admin as a, update

from .model.blog import BlogNotFound, BlogError

import ujson
import collections


class RootAdminController(a.AdminController):
    async def get(self):
        try:
            blogs = await self.application.blogs.list_blogs(self.gamespace)
        except BlogError as e:
            raise a.ActionError(e.args[0])

        return {
            "blogs": blogs
        }

    def render(self, data):
        tbl_rows = [{
            "edit": [a.link("blog", blog.name, icon="rss", blog_id=blog.blog_id)],
            "enabled": [a.status("Yes" if blog.enabled else "No", "success" if blog.enabled else "danger")],
        } for blog in data["blogs"]]

        return [
            a.content("Blogs", [
                {
                    "id": "edit",
                    "title": "Blog"
                }, {
                    "id": "enabled",
                    "title": "Enabled"
                }], tbl_rows, "default", empty="No blogs"),
            a.links("Actions", [
                a.link("new_blog", "New Blog", icon="plus")
            ])
        ]

    def access_scopes(self):
        return ["blog_admin"]


class NewBlogAdminController(a.AdminController):
    def render(self, data):

        return [
            a.breadcrumbs([], "Create New"),
            a.form("Create New Blog", fields={
                "name": a.field("Blog Name", "text", "primary", "non-empty", order=1),
                "schema": a.field("Blog Schema", "json", "primary", order=2,
                                  description="A JSON Scheme every blog entry will be matched on. "
                                              "See docs below for more information."),
                "enabled": a.field("Enabled", "switch", "primary", order=3)
            }, methods={
                "create": a.method("Create", "primary")
            }, data=data),
            a.links("Navigate", [
                a.link("index", "Go back", icon="chevron-left"),
                a.link("https://spacetelescope.github.io/understanding-json-schema/index.html", "See docs", icon="book")
            ])
        ]

    async def get(self):
        return {
            "schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "title": "Title",
                        "type": "object",
                        "properties": {
                            "en": {
                                "title": "English Title",
                                "type": "string"
                            }
                        }
                    }
                },
                "title": "Blog Entry"
            },
            "enabled": "true"
        }

    @validate(name="str_name", schema="load_json_dict", enabled="bool")
    async def create(self, name, schema, enabled):
        try:
            blog_id = await self.application.blogs.create_blog(self.gamespace, name, schema, enabled)
        except BlogError as e:
            raise a.ActionError(e.args[0])

        raise a.Redirect("blog", message="New blog has been created", blog_id=blog_id)

    def access_scopes(self):
        return ["blog_admin"]


class BlogAdminController(a.AdminController):
    ENTRIES_PER_PAGE = 20

    def render(self, data):

        tbl_rows = [{
            "edit": [a.link(
                "blog_entry",
                entry.data["title"]["en"]
                if entry.data.get("title", {}).get("en", None) is not None
                else entry.entry_id, icon="rss",
                blog_id=self.context.get("blog_id"),
                entry_id=entry.entry_id)],
            "enabled": [a.status("Yes" if entry.enabled else "No", "success" if entry.enabled else "danger")],
            "created": str(entry.create_date),
            "updated": str(entry.update_date)
        } for entry in data["entries"]]

        return [
            a.breadcrumbs([], data["blog_name"]),
            a.content("Entries", [
                {
                    "id": "edit",
                    "title": "Edit"
                }, {
                    "id": "enabled",
                    "title": "Enabled"
                }, {
                    "id": "created",
                    "title": "Created"
                }, {
                    "id": "updated",
                    "title": "Updated"
                }], tbl_rows, "default", empty="No blog entries"),
            a.pages(data["pages"]),
            a.links("Navigate", [
                a.link("index", "Go back", icon="chevron-left"),
                a.link("new_blog_entry", "New Blog Entry", icon="plus", blog_id=self.context.get("blog_id")),
                a.link("blog_settings", "Settings", icon="cogs", blog_id=self.context.get("blog_id"))
            ])
        ]

    @validate(blog_id="int", page="int")
    async def get(self, blog_id, page=1):
        try:
            blog = await self.application.blogs.get_blog(self.gamespace, blog_id)
        except BlogNotFound:
            raise a.ActionError("No such blog")

        try:
            pages, entries = await self.application.blogs.list_blog_entries_pages(
                self.gamespace, blog_id, BlogAdminController.ENTRIES_PER_PAGE, page)
        except BlogError as e:
            raise a.ActionError(e.args[0])

        return {
            "blog_name": blog.name,
            "pages": pages,
            "entries": entries
        }

    def access_scopes(self):
        return ["blog_admin"]


class BlogSettingsAdminController(a.AdminController):
    def render(self, data):

        return [
            a.breadcrumbs([
                a.link("blog", data["name"], blog_id=self.context.get("blog_id"))
            ], "Settings"),
            a.form("Blog Settings", fields={
                "name": a.field("Blog Name", "text", "primary", "non-empty", order=1),
                "schema": a.field("Blog Schema", "json", "primary", order=2,
                                  description="A JSON Scheme every blog entry will be matched on. "
                                              "See docs below for more information."),
                "enabled": a.field("Enabled", "switch", "primary", order=3)
            }, methods={
                "update": a.method("Update", "primary")
            }, data=data),
            a.form("Danger", fields={}, methods={
                "delete": a.method("Delete This Blog Forever", "danger")
            }, data=data, icon="warning"),
            a.links("Navigate", [
                a.link("index", "Go back", icon="chevron-left"),
                a.link("https://spacetelescope.github.io/understanding-json-schema/index.html", "See docs", icon="book")
            ])
        ]

    @validate(name="str_name", schema="load_json_dict", enabled="bool")
    async def update(self, name, schema, enabled=False, **ignored):
        blog_id = self.context.get("blog_id")

        try:
            await self.application.blogs.update_blog(self.gamespace, blog_id, name, schema, enabled)
        except BlogError:
            raise a.ActionError("Failed to update blog")

        raise a.Redirect("blog_settings", message="Blog has been updated", blog_id=blog_id)

    async def delete(self):
        blog_id = self.context.get("blog_id")

        try:
            await self.application.blogs.delete_blog(self.gamespace, blog_id)
        except BlogError:
            raise a.ActionError("Failed to delete blog")

        raise a.Redirect("index", message="Blog has been deleted")

    async def get(self, blog_id):
        try:
            blog = await self.application.blogs.get_blog(self.gamespace, blog_id)
        except BlogNotFound:
            raise a.ActionError("No such blog")

        return {
            "name": blog.name,
            "schema": blog.schema,
            "enabled": "true" if blog.enabled else "false"
        }

    @validate(name="str_name", schema="load_json_dict", enabled="bool")
    async def create(self, name, schema, enabled):
        try:
            blog_id = await self.application.blogs.create_blog(self.gamespace, name, schema, enabled)
        except BlogError as e:
            raise a.ActionError(e.args[0])

        raise a.Redirect("blog", message="New blog has been created", blog_id=blog_id)

    def access_scopes(self):
        return ["blog_admin"]


class NewBlogEntryAdminController(a.AdminController):
    def render(self, data):
        new_entry = self.context.get("clone", None) is None
        return [
            a.breadcrumbs([
                a.link("blog", data["blog_name"], blog_id=self.context.get("blog_id"))
            ], "New Blog Entry" if new_entry else "Clone Blog Entry"),
            a.form("Blog Entry", fields={
                "data": a.field("Entry", "dorn", "primary", schema=data["blog_schema"], order=1),
                "enabled": a.field("Enabled", "switch", "primary", order=2)
            }, methods={
                "create": a.method("Create" if new_entry else "Clone", "primary")
            }, data=data),
            a.links("Navigate", [
                a.link("blog", "Go back", icon="chevron-left", blog_id=self.context.get("blog_id")),
                a.link("blog_settings", "Edit Blog Settings", icon="cogs", blog_id=self.context.get("blog_id"))
            ])
        ]

    async def get(self, blog_id, clone=None):
        try:
            blog = await self.application.blogs.get_blog(self.gamespace, blog_id)
        except BlogNotFound:
            raise a.ActionError("No such blog")

        if clone is None:
            enabled = "true"
            data = {}
        else:
            try:
                entry = await self.application.blogs.get_blog_entry(self.gamespace, blog_id, clone)
            except BlogNotFound:
                raise a.ActionError("No such blog")
            else:
                enabled = "true" if entry.enabled else "false"
                data = entry.data

        return {
            "blog_name": blog.name,
            "blog_schema": blog.schema,
            "enabled": enabled,
            "data": data
        }

    @validate(data="load_json_dict", enabled="bool")
    async def create(self, data, enabled=False, **ignored):
        blog_id = self.context.get("blog_id")
        try:
            entry_id = await self.application.blogs.create_blog_entry(self.gamespace, blog_id, data, enabled)
        except BlogError as e:
            raise a.ActionError(e.args[0])

        raise a.Redirect("blog", message="New blog entry has been created", blog_id=blog_id)

    def access_scopes(self):
        return ["blog_admin"]


class BlogEntryAdminController(a.AdminController):
    def render(self, data):
        return [
            a.breadcrumbs([
                a.link("blog", data["blog_name"], blog_id=self.context.get("blog_id"))
            ], "Blog Entry #{0}".format(self.context.get("entry_id"))),
            a.form("Blog Entry", fields={
                "data": a.field("Entry", "dorn", "primary", schema=data["blog_schema"], order=1),
                "enabled": a.field("Enabled", "switch", "primary", order=2)
            }, methods={
                "update": a.method("Update", "primary"),
                "delete": a.method("Delete", "danger")
            }, data=data),
            a.links("Navigate", [
                a.link("blog", "Go back", icon="chevron-left", blog_id=self.context.get("blog_id")),
                a.link("new_blog_entry", "Clone This Entry", icon="clone", blog_id=self.context.get("blog_id"),
                       clone=self.context.get("entry_id")),
                a.link("blog_settings", "Edit Blog Settings", icon="cogs", blog_id=self.context.get("blog_id"))
            ])
        ]

    async def get(self, blog_id, entry_id):
        try:
            blog = await self.application.blogs.get_blog(self.gamespace, blog_id)
        except BlogNotFound:
            raise a.ActionError("No such blog")

        try:
            entry = await self.application.blogs.get_blog_entry(self.gamespace, blog_id, entry_id)
        except BlogNotFound:
            raise a.ActionError("No such blog")

        return {
            "blog_name": blog.name,
            "blog_schema": blog.schema,
            "data": entry.data,
            "enabled": "true" if entry.enabled else "false",
        }

    @validate()
    async def delete(self, **ignored):
        blog_id = self.context.get("blog_id")
        entry_id = self.context.get("entry_id")

        try:
            await self.application.blogs.get_blog(self.gamespace, blog_id)
        except BlogNotFound:
            raise a.ActionError("No such blog")

        try:
            await self.application.blogs.delete_blog_entry(self.gamespace, blog_id, entry_id)
        except BlogError as e:
            raise a.ActionError(e.args[0])

        raise a.Redirect("blog", message="Blog entry has been deleted", blog_id=blog_id)

    @validate(data="load_json_dict", enabled="bool")
    async def update(self, data, enabled=False, **ignored):
        blog_id = self.context.get("blog_id")
        entry_id = self.context.get("entry_id")

        try:
            await self.application.blogs.get_blog(self.gamespace, blog_id)
        except BlogNotFound:
            raise a.ActionError("No such blog")

        try:
            await self.application.blogs.update_blog_entry(self.gamespace, blog_id, entry_id, data, enabled)
        except BlogError as e:
            raise a.ActionError(e.args[0])

        raise a.Redirect("blog", message="Blog entry has been updated", blog_id=blog_id)

    def access_scopes(self):
        return ["blog_admin"]
