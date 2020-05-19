import csv
import logging

import pandas as pd

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class FileCopier:
    """
    Copy data from files to database.

    .. note::
        As of now, only CSV files are supported.
    """

    def __init__(self, db_backend, path, delimiter=',',
                 unique_column='hex_id'):
        """
        :param geospin.utilities.backend.DatabaseBackend db_backend:
            Database backend.
        :param str path:
            Path to csv file with data to add to database table. The file
            must have a header.
        :param str delimiter:
            String that separates column values in the file.
        :param unique_column:
            Name of column in `table` that must be unique. If the provided
            file has values in `unique_column` that are identical to the
            corresponding column value in `table`, the corresponding rows are
            not added.
        """
        self.db_backend = db_backend
        self.path = path
        self.delimiter = delimiter
        self.unique_column = unique_column

    def copy_file_into_new_table(self, table, columns=None):
        """
        Copy file content into new table.

        Note: Only works for files that fit into memory.

        :param str table: Name of new table.
        :param None or list of str columns:
            List of columns to add. Default None adds all columns.
        """
        df = pd.read_csv(self.path, usecols=columns)
        with self.db_backend.engine.connect() as conn:
            df.to_sql(name=table, con=conn, index=False, chunksize=1000,
                      method='multi')

    def append_rows_from_file_to_existing_table(self, table):
        """ Append data from csv file to table.

        The columns in the table and the file have to be the same, but the
        column order is not important.

        :param str table:
            Name of table to which data should be added.
        """
        self._raise_if_columns_in_file_differ_from_columns_in_table(table)
        columns_in_file = self._get_column_names_in_file()

        sql = f"""
        -- Define function that adds a constraint only if it doesn't exist yet
        create or replace function add_unique_constraint_if_not_yet_there(
                tablename text, columnname text)
        returns void AS
        $$
        begin
            -- Check if column has unique constraint already
            if not exists(
                    with unique_columns_in_this_table as (
                        select column_name
                        from information_schema.table_constraints tc
                                 inner join
                             information_schema.constraint_column_usage cu
                             on cu.constraint_name = tc.constraint_name
                        where tc.constraint_type = 'UNIQUE'
                          and tc.table_name = tablename
                          and cu.column_name = columnname)
                    -- Is `columnname` in the unique columns?
                    select *
                    from unique_columns_in_this_table
                    where unique_columns_in_this_table.column_name = columnname
                )
            then
                -- Add unique constraint to column `columname`
                execute 'ALTER TABLE ' || tablename ||
                        ' ADD CONSTRAINT ' || columnname || ' ' ||
                        'unique (' || columnname || ')';
            end if;
        end;
        $$ language 'plpgsql';
        -- Create empty temporary table to be filled with data from file
        CREATE TEMP TABLE tmp_table
            ON COMMIT DROP
        AS
        SELECT *
        FROM {table}
            WITH NO DATA;
        -- Fill temporary table with data from file, take care of column order
        COPY tmp_table ({", ".join(columns_in_file)})
            FROM STDIN
            WITH (FORMAT CSV, HEADER TRUE, DELIMITER '{self.delimiter}');
        -- Ensure that `unique_column` is unique
        SELECT add_unique_constraint_if_not_yet_there(
                    '{table}', '{self.unique_column}');
        -- Insert all NEW rows into table
        INSERT INTO {table}
        SELECT *
        FROM tmp_table ON CONFLICT DO NOTHING;
        """
        with open(self.path, 'r') as file:
            conn = self.db_backend.engine.raw_connection()
            cursor = conn.cursor()
            cursor.copy_expert(sql, file)
            conn.commit()
            conn.close()

    def _raise_if_columns_in_file_differ_from_columns_in_table(self, table):
        columns_in_table = self.db_backend.get_column_names_in_table(table)
        columns_in_file = self._get_column_names_in_file()

        columns_only_in_file = []
        for column in columns_in_file:
            if column not in columns_in_table:
                columns_only_in_file.append(column)
        if columns_only_in_file:
            raise ValueError(f'File contains columns that are not in table: '
                             f'{columns_only_in_file}')
        for column in columns_in_table:
            if column not in columns_in_file:
                raise ValueError('Table contains columns that are not in file!')

    def _get_column_names_in_file(self):
        with open(self.path) as file:
            reader = csv.reader(file, delimiter=self.delimiter)
            columns = next(reader)
        return columns


class ViewCreator:
    """
    Create views at high resolution from feature tables at lower resolution

    For example it addresses the following issue:
    * Say we have real estate prices aggregated at resolution 8 (and with
    gaps at hex IDs where there is no such data)
    * The Germany wide probe table is at resolution 9
    * We want to create a view that contains the `hex_id` column at
    resolution 9 and all feature values that correspond to each hex ID (
    obtained from the parent hexagon at resolution 8)
    * hex_ids at resolution 9 for which no data exists should be filled with
    NULL.
    """

    def __init__(self,
                 db_backend,
                 feature_table='imo0001_prices',
                 hex_id_parents_table='hex_id_parents_of_resolution_9',
                 high_resolution=9,
                 feature_resolution=8,
                 ):
        self.db_backend = db_backend
        self.feature_table = feature_table
        self.hex_id_parents_table = hex_id_parents_table
        self.high_resolution = high_resolution
        self.feature_resolution = feature_resolution
        self.name = self.feature_table + f'_resolution_{self.high_resolution}'
        self._raise_if_table_does_not_exist()

    def create(self):
        """
        Create the view at high resolution.

        :return None:
        """
        feature_columns = self._get_feature_column_names_with_alias_prefix()
        feature_columns_str = _list2string(feature_columns)
        sql = f"""
        DROP VIEW IF EXISTS {self.name};

        CREATE VIEW {self.name} AS
        SELECT  parents.hex_id_resolution_{self.high_resolution} AS hex_id,
                {feature_columns_str}
        FROM
            {self.hex_id_parents_table} AS parents
            LEFT JOIN {self.feature_table} AS features
            ON
            parents.hex_id_resolution_{self.feature_resolution} =
                features.hex_id;
        """
        with self.db_backend.engine.connect() as connection:
            logger.info('Create view with features table at high resolution')
            connection.execute(sql)

    def _get_feature_column_names_with_alias_prefix(self,
                                                    alias='features'):
        """
        Return all column names from feature table excluding hex ID column

        Querying only the columns that we need is more efficient than first
        querying all and then dropping the `hex_id` column.

        :param str alias: Alias to prefix the columns with.
        :return list[str]: feature_columns_with_alias_prefix
        """
        columns = self.db_backend.get_column_names_in_table(self.feature_table)
        columns.remove('hex_id')
        feature_columns_with_alias_prefix = [
            f'{alias}.{column}' for column in columns
        ]
        return feature_columns_with_alias_prefix

    def _raise_if_table_does_not_exist(self):
        tables = [self.feature_table, self.hex_id_parents_table]
        for table in tables:
            if not self.db_backend.engine.has_table(table):
                raise ValueError(f'Table {table} not found in database!')


def _list2string(l):
    return ', '.join(l)
