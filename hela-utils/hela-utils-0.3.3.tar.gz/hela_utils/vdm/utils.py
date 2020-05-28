from .helpers import get_query_results


def get_table_names(vdm_connection):
    """
    returns all table names from the vdm connection source
    """
    query = """SELECT DISTINCT TableName FROM SYS.Columns;"""
    data = get_query_results(vdm_connection, query)
    return sorted([row[0] for row in data])


def get_field_names_from_table(vdm_connection, table_name):
    """
    returns the field names for a given table name
    """
    query = """SELECT mysub.Name FROM
              (SELECT Name, TableName
              FROM SYS.Columns
              WHERE TableName='{table}') mysub;""".format(table=table_name)
    data = get_query_results(vdm_connection, query)
    return sorted([row[0] for row in data])


def get_tables_from_field_name(vdm_connection, field_name):
    """
    returns the names of the tables that have the given field name
    """
    query = """SELECT DISTINCT mysub.TableName FROM
              (SELECT Name, TableName
              FROM SYS.Columns
              WHERE Name='{field}') mysub;""".format(field=field_name)
    data = get_query_results(vdm_connection, query)
    return sorted([row[0] for row in data])
