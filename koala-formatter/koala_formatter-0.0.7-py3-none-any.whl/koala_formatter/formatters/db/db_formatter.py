from collections.abc import Callable
from koala_formatter.formatters.formatter_base import FormatterBase
from urllib3.util import parse_url


class DBFormatter(FormatterBase):

    def __init__(self, db_url: str = None):
        super().__init__(__name__)
        self._host = self._get_host(db_url)

    def __enter__(self):
        return self

    @property
    def collection_node_type(self):
        return "db_table"

    @property
    def required_collection_node_fields(self):
        return tuple(('schema_name', 'table_name', 'table_description', 'team_name'))

    @property
    def resource_node_type(self):
        return "db_table_column"

    @property
    def required_resource_node_fields(self):
        return tuple(('schema_name', 'table_name', 'column_name',
                      'column_description', 'data_type'))

    @property
    def required_edge_fields(self):
        return tuple(('inV', 'outV', 'label'))

    @property
    def collection_id_creator(self) -> Callable:
        return lambda column_map: f"{column_map['schema_name']}.{column_map['table_name']}"

    @property
    def resource_id_creator(self) -> Callable:
        return lambda column_map: f"{column_map['schema_name']}.{column_map['table_name']}.{column_map['column_name']}"

    @property
    def origin_host(self):
        return self._host

    def create_nodes(self, tables, columns):
        return self._create_graph_objects(tables, columns)

    @staticmethod
    def _get_host(db_url: str) -> str:
        if db_url:
            return parse_url(db_url).host
        else:
            return db_url
