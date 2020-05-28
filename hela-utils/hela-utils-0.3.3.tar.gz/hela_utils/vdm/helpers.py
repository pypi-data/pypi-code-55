import psycopg2


def make_connection(db, host, port, user, pw, cert):
    config = {
        'host': host,
        'port': port,
        'user': user,
        'password': pw,
        'database': db,
        'sslmode': 'verify-ca',
        'sslrootcert': cert
    }
    connection = psycopg2.connect(**config)
    return connection


def col_name_mapping(col_names, rows):
    """
    Loops through a list of nested lists; maps each one to a separate of column names. Order of lists must match col list.
    :param col_names: the names to match each item to.
    :param rows: the list of nested lists ("records")
    :return: a nested list of dictionaried versions of each record
    """
    return [dict(zip(col_names, row)) for row in rows]


def get_query_results(vdm_conn, sql_query, as_named_dict=False):
    """
    Runs a VDM query and returns the results.
    :param vdm_conn: JDB VDM instance.
    :type vdm_conn: dict
    :param sql_query: SQL query.
    :type sql_query: str
    :return get_query: list of records (dicts).
    :rtype: list
    """
    c = vdm_conn.cursor()
    c.execute(sql_query)
    get_query = c.fetchall()
    if as_named_dict:
        desc = c.description
        column_names = [col[0] for col in desc]
        get_query = col_name_mapping(column_names, get_query)
    c.close()
    vdm_conn.close()
    return get_query
