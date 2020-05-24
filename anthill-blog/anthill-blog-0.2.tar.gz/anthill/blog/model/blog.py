
from anthill.common.database import DuplicateError, DatabaseError
from anthill.common.internal import Internal, InternalError
from anthill.common.model import Model
from anthill.common.validate import validate
from anthill.common import clamp

import ujson


class BlogEntryAdapter(object):
    def __init__(self, data):
        self.entry_id = data.get("entry_id")
        self.blog_id = data.get("blog_id")
        self.data = data.get("entry_data")
        self.enabled = data.get("entry_enabled") == 1
        self.create_date = data.get("entry_create_dt")
        self.update_date = data.get("entry_update_dt")

    def dump(self):
        return {
            "id": self.entry_id,
            "data": self.data,
            "create_date": str(self.create_date),
            "update_date": str(self.update_date)
        }


class BlogAdapter(object):
    def __init__(self, data):
        self.blog_id = data.get("blog_id")
        self.name = data.get("blog_name")
        self.schema = data.get("blog_schema")
        self.enabled = data.get("blog_enabled") == 1

    def dump(self):
        return {
            "name": self.name,
            "enabled": self.enabled
        }


class BlogError(Exception):
    def __init__(self, code, reason):
        super(Exception, self).__init__(reason)
        self.code = code


class BlogNotFound(Exception):
    pass


class BlogEntryNotFound(Exception):
    pass


class BlogsModel(Model):
    def __init__(self, db, app):
        self.db = db
        self.app = app
        self.internal = Internal()

    def get_setup_tables(self):
        return ["blogs", "blog_entries"]

    def get_setup_db(self):
        return self.db

    def has_delete_account_event(self):
        return False

    @validate(gamespace_id="int", blog_name="str_name", blog_schema="json_dict", blog_enabled="bool")
    async def create_blog(self, gamespace_id, blog_name, blog_schema, blog_enabled):
        try:
            blog_id = await self.db.insert(
                """
                INSERT INTO `blogs`
                (`gamespace_id`, `blog_name`, `blog_schema`, `blog_enabled`) 
                VALUES (%s, %s, %s, %s);
                """, gamespace_id, blog_name, ujson.dumps(blog_schema), int(blog_enabled))
        except DuplicateError:
            raise BlogError(409, "Blog with name '{0}' already exists".format(blog_name))
        except DatabaseError as e:
            raise BlogError(500, "Failed to create blog: " + str(e.args[1]))

        return blog_id

    @validate(gamespace_id="int", blog_id="int")
    async def delete_blog(self, gamespace_id, blog_id):
        try:
            async with self.db.acquire() as db:
                await db.execute(
                    """
                    DELETE FROM `blog_entries`
                    WHERE `gamespace_id`=%s AND `blog_id`=%s;
                    """, gamespace_id, blog_id)
                await db.execute(
                    """
                    DELETE FROM `blogs`
                    WHERE `gamespace_id`=%s AND `blog_id`=%s;
                    """, gamespace_id, blog_id)
        except DatabaseError as e:
            raise BlogError(500, str(e.args[1]))

    @validate(gamespace_id="int", blog_id="int", blog_name="str_name", blog_schema="json_dict", blog_enabled="bool")
    async def update_blog(self, gamespace_id, blog_id, blog_name, blog_schema, blog_enabled):
        try:
            await self.db.execute(
                """
                UPDATE `blogs`
                SET `blog_name`=%s, `blog_schema`=%s, `blog_enabled`=%s
                WHERE `gamespace_id`=%s AND `blog_id`=%s;
                """,  blog_name, ujson.dumps(blog_schema), int(blog_enabled), gamespace_id, blog_id)
        except DuplicateError:
            raise BlogError(409, "Blog with name '{0}' already exists".format(blog_name))
        except DatabaseError as e:
            raise BlogError(500, "Failed to update blog: " + str(e.args[1]))

    @validate(gamespace_id="int", blog_name="str_name")
    async def find_blog(self, gamespace_id, blog_name, db=None):
        try:
            result = await (db or self.db).get("""
                SELECT *
                FROM `blogs`
                WHERE `blog_name`=%s AND `gamespace_id`=%s
                LIMIT 1;
            """, blog_name, gamespace_id)
        except DatabaseError as e:
            raise BlogError(500, "Failed to find blog: " + e.args[1])
        if result is None:
            raise BlogNotFound()
        return BlogAdapter(result)

    @validate(gamespace_id="int", blog_id="int")
    async def get_blog(self, gamespace_id, blog_id, db=None):
        try:
            result = await (db or self.db).get("""
                SELECT *
                FROM `blogs`
                WHERE `blog_id`=%s AND `gamespace_id`=%s
                LIMIT 1;
            """, blog_id, gamespace_id)
        except DatabaseError as e:
            raise BlogError(500, "Failed to get blog: " + e.args[1])
        if result is None:
            raise BlogNotFound()
        return BlogAdapter(result)

    @validate(gamespace_id="int")
    async def list_blogs(self, gamespace_id):
        result = await self.db.query("""
            SELECT `blog_name`, `blog_id`, `blog_enabled`
            FROM `blogs`
            WHERE `gamespace_id`=%s;
        """, gamespace_id)

        return list(map(BlogAdapter, result))

    @validate(gamespace_id="int", blog_id="int", entry_data="json_dict", entry_enabled="bool")
    async def create_blog_entry(self, gamespace_id, blog_id, entry_data, entry_enabled):
        try:
            entry_id = await self.db.insert(
                """
                INSERT INTO `blog_entries`
                (`gamespace_id`, `blog_id`, `entry_data`, `entry_enabled`) 
                VALUES (%s, %s, %s, %s);
                """, gamespace_id, blog_id, ujson.dumps(entry_data), int(entry_enabled))
        except DatabaseError as e:
            raise BlogError(500, "Failed to create blog entry: " + str(e.args[1]))

        return entry_id

    @validate(gamespace_id="int", blog_id="int", entry_id="int")
    async def delete_blog_entry(self, gamespace_id, blog_id, entry_id):
        try:
            await self.db.execute(
                """
                DELETE FROM `blog_entries`
                WHERE `gamespace_id`=%s AND `blog_id`=%s AND `entry_id`=%s;
                """, gamespace_id, blog_id, entry_id)
        except DatabaseError as e:
            raise BlogError(500, str(e.args[1]))

    @validate(gamespace_id="int", blog_id="int", entry_id="int", entry_data="json_dict", entry_enabled="bool")
    async def update_blog_entry(self, gamespace_id, blog_id, entry_id, entry_data, entry_enabled):
        try:
            await self.db.execute(
                """
                UPDATE `blog_entries`
                SET `entry_data`=%s, `entry_enabled`=%s, `entry_update_dt`=CURRENT_TIMESTAMP()
                WHERE `gamespace_id`=%s AND `blog_id`=%s AND `entry_id`=%s;
                """,ujson.dumps(entry_data), int(entry_enabled), gamespace_id, blog_id, entry_id)
        except DatabaseError as e:
            raise BlogError(500, "Failed to update blog entry: " + str(e.args[1]))

    @validate(gamespace_id="int", blog_id="int")
    async def get_blog_entry(self, gamespace_id, blog_id, entry_id, db=None):
        try:
            result = await (db or self.db).get("""
                SELECT *
                FROM `blog_entries`
                WHERE `blog_id`=%s AND `gamespace_id`=%s AND `entry_id`=%s
                LIMIT 1;
            """, blog_id, gamespace_id, entry_id)
        except DatabaseError as e:
            raise BlogError(500, "Failed to get blog entry: " + e.args[1])
        if result is None:
            raise BlogEntryNotFound()
        return BlogEntryAdapter(result)

    @validate(gamespace_id="int", blog_id="int")
    async def list_enabled_blog_entries(self, gamespace_id, blog_id, limit=20):

        if limit <= 0 or limit > 1000:
            raise BlogError(400, "Bad limit")

        async with self.db.acquire() as db:
            result = await db.query("""
                SELECT `entry_id`, `entry_data`, `entry_create_dt`, `entry_update_dt`
                FROM `blog_entries`
                WHERE `gamespace_id`=%s AND `blog_id`=%s AND `entry_enabled`=1
                ORDER BY `entry_id` DESC
                LIMIT %s;
            """, gamespace_id, blog_id, limit)

        return list(map(BlogEntryAdapter, result))

    @validate(gamespace_id="int", blog_id="int")
    async def list_blog_entries_pages(self, gamespace_id, blog_id, entries_in_page, page=1):

        async with self.db.acquire() as db:
            pages_count = await db.get(
                """
                    SELECT COUNT(*) as `count`
                    FROM `blog_entries`
                    WHERE gamespace_id=%s AND `blog_id`=%s;
                """, gamespace_id, blog_id)

            import math
            pages = int(math.ceil(float(pages_count["count"]) / float(entries_in_page)))

            page = clamp(page, 1, pages)

            limit_a = (page - 1) * entries_in_page
            limit_b = page * entries_in_page

            result = await db.query("""
                SELECT *
                FROM `blog_entries`
                WHERE `gamespace_id`=%s AND `blog_id`=%s
                ORDER BY `entry_id` DESC
                LIMIT %s, %s;
            """, gamespace_id, blog_id, limit_a, limit_b)

        return pages, list(map(BlogEntryAdapter, result))
