from flaskr.db import get_db
import psycopg2.extras as psycopg_extras


class Records:

    def read(self, record_id):
        db = get_db()
        cr = db.cursor(cursor_factory=psycopg_extras.DictCursor)
        query_string = "SELECT id FROM vl_user WHERE id = {}".format(record_id)
        cr.execute(query_string)
        cr.fetchone()