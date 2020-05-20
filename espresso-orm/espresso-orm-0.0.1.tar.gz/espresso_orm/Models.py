from flaskr.db import get_db
import psycopg2.extras as psycopg_extras


class Models:
    pass

    def browse(self, record_ids):
        db = get_db()
        cr = db.cursor(cursor_factory=psycopg_extras.DictCursor)
        query_string = "SELECT * FROM vl_user WHERE id in {}".format(record_ids)
        cr.execute(query_string)
        cr.fetchone()

    def create(self, value):
        pass

    def write(self, values):
        pass

    def delete(self):
        pass
