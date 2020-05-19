import logging
import time

import pandas as pd
from h3 import h3

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class H3Parents:
    """
    Map hex IDs to their parents at lower resolution

    Conceptually, given hex IDs at high resolution like

    `hex_ids = ['bb', 'aa', 'ax', 'cc']`

    we want to get a dataframe that maps the child resolution to a lower parent
    resolution (i.e., its parent hexagons):

    ===================  ===================
    hex_id_resolution_9  hex_id_resolution_8
    ===================  ===================
    'bb'                 'bf'

    'aa'                 'af'

    'ax'                 'af'

    'cc'                 'cf'
    ===================  ===================

    Here, trailing 'f's indicate a lower resolution. Note that for actual hex
    IDs this is more complicated.

    :param list[str] hex_ids:
        Hex IDs at resolution higher than `parent_resolution`.
        Note: the resolution must not vary over the passed hex IDs.
    :param int parent_resolution:
        Resolution of the parent hexagons
    """

    def __init__(self, hex_ids, parent_resolution):
        self.hex_ids = hex_ids
        self.parent_resolution = parent_resolution
        self.child_resolution = h3.h3_get_resolution(self.hex_ids[0])
        self.column_name_child = f'hex_id_resolution_{self.child_resolution}'
        self.column_name_parent = f'hex_id_resolution_{self.parent_resolution}'

        self._raise_if_child_resolution_is_not_higher_than_parent_resolution()

    def get_mapping_dataframe(self):
        """
        Return mapping between hex IDs at different resolutions as dataframe.

        :return pandas.DataFrame: See class docstring.
        """
        logger.info('Get mapping dataframe.')

        hex_ids_parent_resolution = []
        n_hex_ids = len(self.hex_ids)
        for n, hex_id in enumerate(self.hex_ids):
            if n % 10000 == 0:
                logger.info(f'Hex ID {n} out of {n_hex_ids}')
            try:
                hex_ids_parent_resolution.append(
                    h3.h3_to_parent(str(hex_id), self.parent_resolution))
            except TypeError:
                logger.info(f'TypeError at hex ID {hex_id}')

        df = pd.DataFrame(data={
            self.column_name_child: self.hex_ids,
            self.column_name_parent: hex_ids_parent_resolution})
        return df

    def _raise_if_child_resolution_is_not_higher_than_parent_resolution(self):
        if not self.child_resolution > self.parent_resolution:
            raise ValueError(
                'Hex ID child resolution must be higher than parent resolution')


def create_h3_parents_table(db_backend,
                            name_prefix='hex_id_parents_of_resolution_',
                            parent_resolution=8,
                            table_with_child_hex_ids='probe_resolution_11',
                            child_hex_id_column='hex_id'):
    """
    Create table with mapping between high and low H3 resolutions.

    High resolutions are referred to as child resolutions.
    Low resolutions are referred to as parent resolutions.

    Given a table `table_with_child_hex_ids` that has a `hex_id` column at
    high resolutions (the children), e.g., resolution 9, this function
    creates a new table `hex_id_parents_of_resolution_9` that looks like this:

    ===================  ===================
    hex_id_resolution_9  hex_id_resolution_8
    ===================  ===================
    'bb'                 'bf'

    'aa'                 'af'
    ...                  ...
    ===================  ===================

    and creates a primary key on the child resolution (here
    `hex_id_resolution_9`). For details see docstring of `H3Parents`.

    :param geospin.utilities.backend.DatabaseBackend db_backend:
        Database backend with database that contains the
        `table_with_child_hex_ids` and to which the new table is added.
    :param str name_prefix: Prefix of new table name.
    :param int parent_resolution:
        Resolution to which the hex IDs of `table_with_child_hex_ids` are
        mapped.
    :param str table_with_child_hex_ids:
        Name of table with `hex_id` column.
    :param str child_hex_id_column:
        Name of hex_id column in table with child hex IDs.
    :return None:
    """
    with db_backend.engine.connect() as connection:
        t0 = time.time()
        logger.info('Start table creation.')
        hex_ids = _get_child_hex_ids_as_list(
            connection, table_with_child_hex_ids, child_hex_id_column)

        h3_parents = H3Parents(hex_ids, parent_resolution=parent_resolution)
        hex_id_mapping = h3_parents.get_mapping_dataframe()

        logger.info('Write dataframe to database.')
        h3_parents_table_name = f'{name_prefix}{h3_parents.child_resolution}'
        hex_id_mapping.to_sql(h3_parents_table_name, connection, index=False,
                              chunksize=10000, method='multi')
        logger.info('Add primary key.')
        _add_primary_key(connection, h3_parents_table_name,
                         column=h3_parents.column_name_child)
        logger.info(f'Done after {(time.time() - t0):.4} seconds.')


def _get_child_hex_ids_as_list(connection, table_name, hex_id_column='hex_id'):
    logger.info('Get child hex IDs as list.')
    sql = f"""
    SELECT {hex_id_column} FROM {table_name};
    """
    df = pd.read_sql_query(sql, connection)
    hex_ids = df.squeeze().to_list()
    return hex_ids


def _add_primary_key(connection, table, column):
    connection.execute(f'ALTER TABLE {table} ADD PRIMARY KEY ({column});')


def append_to_h3_parents_table(db_backend, existing_table,
                               child_resolution=9, parent_resolution=8):
    """
    Append parent resolution to existing H3 parents table

    See `create_h3_parents_table` for details
    :param geospin.utilities.backend.DatabaseBackend db_backend:
        Database backend with database that contains the
        `existing_table`.
    :param str existing_table:
        Name of existing H3 parents table.
    :param int child_resolution:
        Highest H3 resolution in `existing_table`.
    :param parent_resolution:
        Resolution of parent hex IDs that are to be added as new column.
    :return None:
    """
    logger.info(f'Append resolution {parent_resolution} to {existing_table}')

    child_hex_id_column = f'hex_id_resolution_{child_resolution}'
    parent_hex_id_column = f'hex_id_resolution_{parent_resolution}'
    tmp_table_name = f'tmp_h3_parents_of_resolution_{child_resolution}'

    with db_backend.engine.connect() as connection:
        t0 = time.time()

        # Create temporary H3 parents table
        create_h3_parents_table(db_backend,
                                name_prefix='tmp_h3_parents_of_resolution_',
                                parent_resolution=parent_resolution,
                                table_with_child_hex_ids=existing_table,
                                child_hex_id_column=child_hex_id_column)

        sql = f"""
        ALTER TABLE {existing_table} ADD COLUMN {parent_hex_id_column} text;

        UPDATE {existing_table} AS existing
        SET {parent_hex_id_column} = (
            SELECT tmp.{parent_hex_id_column}
            FROM {tmp_table_name} AS tmp
            WHERE tmp.{child_hex_id_column} = existing.{child_hex_id_column}
        );

        DROP TABLE {tmp_table_name};
        """
        connection.execute(sql)

        logger.info(f'Done appending after {(time.time() - t0):.4} seconds.')
