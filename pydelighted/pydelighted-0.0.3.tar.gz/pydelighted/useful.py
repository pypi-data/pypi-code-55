import collections
import time


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def process_data(raw_data, date_fields):
    object_row = []
    for r in (raw_data):
        _object = dict()
        r_flat=flatten(r, parent_key='', sep='_')
        for o in r_flat.keys():
            _object[o.lower().replace(' ','_')] = format(date_fields, r_flat,o)
        object_row.append(_object)
    return object_row


def get_column_names(data):
    column_list = []
    for d in data:
        for c in d.keys():
            if c not in column_list:
                column_list.append(c)
    return column_list

def send_temp_data(datamart, data, schema_prefix, table, column_names):
    data_to_send = {
        "columns_name": column_names,
        "rows": [[r.get(c) for c in column_names] for r in data],
        "table_name": schema_prefix + '.' + table + '_temp'}
    datamart.send_data(
        data=data_to_send,
        other_table_to_update=schema_prefix + '.' + table,
        replace=False)

def format(date_fields,r, o):
    if o in date_fields:
        date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r.get(o)))
        return date_str
    elif type(r.get(o)) == list or type(r.get(o)) == dict:
        return str(r.get(o))
    return r.get(o)


def _clean(datamart, schema_prefix, table):
    selecting_id = 'id'
    print('trying to clean')
    cleaning_query = """
            DELETE FROM %(schema_name)s.%(table_name)s WHERE %(id)s IN (SELECT distinct %(id)s FROM %(schema_name)s.%(table_name)s_temp);
            INSERT INTO %(schema_name)s.%(table_name)s 
            SELECT * FROM %(schema_name)s.%(table_name)s_temp;
            DELETE FROM %(schema_name)s.%(table_name)s_temp;
            """ % {"table_name": table,
                   "schema_name": schema_prefix,
                   "id": selecting_id}
    datamart.execute_query(cleaning_query)
    print('cleaned')