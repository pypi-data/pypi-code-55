# Standard library imports.
from typing import List, Dict, Tuple, Union, Optional, Any, Pattern
from functools import reduce
import re
import inspect
from time import sleep
import dateutil
import datetime
import sys

# Math and data analysis imports
import pandas as pd
from pathlib import Path
from getpass import getpass as gp

# Third-party library imports
import psycopg2
from psycopg2 import extensions as _ext
import pyodbc
import dill as pickle
import keyring
from keyrings.alt import Windows
import logging
from sqlalchemy import create_engine, MetaData, Table
import sqlalchemy
from pprint import pprint
from joblib import Memory
from meta import app_name
from colorama import Fore

# Local imports.
# from config_ import get_config_from
from test_db_utils_ge_packaging.db_utils_ge import config

# Cache.
location = 'cachedir'
memory = Memory(location, verbose=0)

# Set keyring.
keyring.set_keyring(Windows.RegistryKeyring())

# Global paths.
INPUT_CONF_FOLDER = Path(app_name) / 'input_conf'
PICKLES_FOLDER = Path(app_name) / 'pickles'

# psycopg2 types to use in driver acknowledgement.
PsyConn = psycopg2.extensions.connection
PsyCur = psycopg2.extensions.cursor

COLOR_INFO = Fore.GREEN
COLOR_WARN = Fore.LIGHTBLUE_EX
COLOR_ERROR = Fore.RED
COLOR_NONE = Fore.RESET
COLOR_META = Fore.MAGENTA


def time_range_splitter(query: str, split_by_nmonths: Union[int, float], is_overlap: bool = False) -> str:
    """Gets query string and returns generator of queries with.

    Parameters
    ----------
    query
        Strings that contains time range in the order Tsmaller Tbigger.
    split_by_nmonths
        Split using interval in months.
    is_overlap
        If in the internal splitting points the periods overlap, default False.
    Returns
    -------
    str
        The same string with time ranges replaced by fractionated time string.

    """
    # Look for time in format "YYYY-mm-DD HH:MM:SS"
    patt: Pattern[str] = re.compile('\d+-\d+-\d+(\s+\d+:\d+:\d+)?')
    dates_tuple = [m.group(0) for m in re.finditer(patt, query)]
    try:
        mp = list(map(dateutil.parser.parse, dates_tuple))
    except Exception as e:
        print(f'Exception in time parsing in time_range_splitter, aborting. Code: {repr(e)}')
        sys.exit(1)

    # [:2] and n_pairs>1 for the cases where more than 1 time column affected in SQL query.
    date_start, date_end = mp[:2]
    n_pairs = len(mp) // 2

    # Short-circuit back the same query, if split is not needed.
    if date_end - date_start <= datetime.timedelta(days=30 * split_by_nmonths):
        yield query

    # For letter aliases see
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
    freq_alias = 'D'  # M for months
    spl_list = pd.date_range(date_start, date_end, freq=f'{int(30 * split_by_nmonths)}{freq_alias}')

    # Add boundaries to the list, if not present.
    if date_start not in spl_list:
        spl_list = spl_list.insert(0, pd.date_range(date_start, periods=1)[0])
    if date_end not in spl_list:
        spl_list = spl_list.append(pd.date_range(date_end, periods=1))

    for idx, t_a in enumerate(spl_list[:-1]):
        t_b = spl_list[idx + 1]
        # Add 1 hour for internal timestamps to make the intersection.
        # This is needed to ensure the delta are computed correctly, e.g.
        # the FIRST variant is to be used when duplicates are removed.
        t_b = t_b + pd.Timedelta('1hour') if is_overlap and t_b != date_end else t_b

        rep = (str(x) for x in [t_a, t_b] * n_pairs)
        new_query = re.sub(patt, lambda match: next(rep), query)
        if t_b != date_end:
            # PostgreSQL syntax (e.g. for GR)
            new_query = new_query.replace('::timestamp + INTERVAL \'1 day\'', '')
            # MS SQL syntax (e.g. for SCADA)
            new_query = new_query.replace('DATEADD(day, 1', 'DATEADD(day, 0')
        yield new_query


def query_inserter(schema: str,
                   dct: Union[dict, pd.DataFrame],
                   verbose: bool = True,
                   created_by: bool = False) -> Optional[bool]:
    """Insert data as dict into DB with given table_name

    Parameters
    ----------
    schema
    dct
        Keys are column names, values are data.
    verbose
        Flush commentaries if True.
    created_by
        add DB username to 'created_by' field
    Returns
    -------
    None
        Adds data to DB.

    """
    params = config.get_config_from(filename='database_default.ini', section='postgresql')
    if created_by:
        dct['created_by'] = params['user']
    try:
        connect_url = sqlalchemy.engine.url.URL(
            drivername='postgresql+psycopg2',
            username=params['user'],
            password=params['password'],
            host=params['host'],
            port=params['port'],
            database=params['database'],
            query={'sslmode': params['sslmode'], 'connect_timeout': params['connect_timeout']}
        )
        schema_name, table_name = schema.split('.')

        engine = create_engine(connect_url, echo=False)
        with engine.connect() as conn_alch:
            if isinstance(dct, dict):
                conn_alch.execute(f'SET search_path TO {schema_name}')
                meta = MetaData()
                table_data = Table(table_name,
                                   meta,
                                   autoload=True,
                                   autoload_with=conn_alch,
                                   postgresql_ignore_search_path=True)
                conn_alch.execute(table_data.insert().values(dct))
                print("Record inserted successfully into mobile table")
            elif isinstance(dct, pd.DataFrame):
                dct.to_sql(name=table_name, con=conn_alch, schema=schema_name, if_exists='append', index=False)
                print("DataFrame inserted successfully into mobile table")
        status_ok = True
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table, psycopg2 error:", repr(error))
        pprint(dct)
        logging.critical(f'Failed to insert record into mobile table, psycopg2 error:: {repr(error)}')
        status_ok = False
    except Exception as e:
        logging.critical(f'Failed to insert record into mobile table, unknown error: {repr(e)}')
        status_ok = None
    return status_ok


@memory.cache
def query_puller(output_type: str = 'list',
                 schema: Optional[str] = None,
                 fields: Optional[List[str]] = None,
                 limit: int = 10000,
                 query_add: str = '',
                 verbose: bool = True,
                 query_override: Optional[str] = None,
                 formatter: bool = True,
                 split_by_nmonths: Optional[Union[int, float]] = None,
                 misc: Union[list, dict, None] = None,
                 credentials: Optional[Tuple[int, str]] = None,
                 is_force_input_password: bool = False,
                 db_config: str = 'postgresql',
                 park_dim_key_single: Optional[int] = None,
                 log_obj: Optional[logging.Logger] = None) -> Union[List, pd.DataFrame, None]:
    """Query part and vendor data from multiple tables

    Parameters
    ----------
    log_obj
        logging.Logger object. If not given, replaced by simple stdio print for text output.
    park_dim_key_single
        park_dim_key to identify the connection parameters.
    is_force_input_password
        Force the application ask for credentials even when keyring is available.
    credentials
        (SSO, password) tuple
    misc
        Reserved for additional parameters.
    output_type
        'list' or 'df'.
    schema
        SQL table_name string.
    fields
        Fields to include in the query.
    limit
        Limit of rows in output.
    query_add
        Additional parameters for query (e.g. " WHERE a='b' ")
    verbose
        Invoke comments of execution,
    query_override
        Inject a whole query to override the other parameters.
    formatter
        Invoke visual reformat of the input query string.
    split_by_nmonths
        Maximum number of month for single query period, or None.
    db_config
        'postgresql' (PostgreSQL) or 'pyodbc' (MS SQL Server)

    Returns
    -------
    Union[List, pd.DataFrame]
        Output of query in given format.

    """
    # Override reading from SCADA if input is a forced query, and db_config is not correct.
    info_flush = log_obj.info if log_obj is not None else print
    error_flush = log_obj.error if log_obj is not None else print
    warning_flush = log_obj.warning if log_obj is not None else print
    if query_override is not None:
        db_config = 'pyodbc' if 'scadahistorical' in query_override.lower() else 'postgresql'
    if db_config == 'pyodbc':
        df_conn_creds = pd.read_csv(INPUT_CONF_FOLDER / 'table_scada__park_dim_key__site_ip__sql_login__sql_pwd__sql_db.csv')
        try:
            db_connect_config_by_park = df_conn_creds[df_conn_creds['park_dim_key'] == park_dim_key_single].iloc[0, :].to_dict()
        except (KeyError, IndexError) as ki_err:
            # Not found park_dim_key, aborting.
            error_flush(f'Could not find SCADA connection config_ by park_dim_key: {park_dim_key_single}, error code: {repr(ki_err)}')
            sys.exit(1)
            # print('----\nTrying default SCADA credentials\n----')

        keep_keywords = ['server', 'user', 'password', 'database', 'login_timeout']
        db_connect_config_by_park = {k: v for k, v in db_connect_config_by_park.items() if k in keep_keywords}
        info_flush(f'Getting connect config_ for SCADA: {db_connect_config_by_park}')

    conn = None
    try:
        db_connect_config = config.get_config_from(filename='database_default.ini', section=db_config)
        if not db_connect_config['user'].strip() or not db_connect_config['password'].strip() or is_force_input_password:
            try:
                if keyring.get_password('fetcher', 'username') is None:
                    # Get username (SSO) from command line.
                    while True:
                        try:
                            # sso should be integer. If not, try the input again.
                            sso = int(input('Enter SSO:'))
                        except ValueError:
                            print('Incorrect input, try again...')
                            continue

                        is_correct = input('Is the input correct? [y/n]')
                        if is_correct.strip().lower() == 'y':
                            db_connect_config['user'] = sso
                            try:
                                keyring.set_password('fetcher', 'username', str(sso))
                            except Exception as e:
                                error_flush('Fatal identification error on keyring.set_password:')
                                input_str = input(repr(e))
                                raise e
                            info_flush(f'Username {sso} saved to keyring.' )
                            break

                    # Get password from command line.
                    while True:
                        passw = gp('Enter password:')
                        is_correct = input('Is the input correct? [y/n]')
                        if is_correct.strip().lower() == 'y':
                            db_connect_config['password'] = passw
                            keyring.set_password('fetcher', 'password', passw)
                            info_flush(f'Password for username {sso} saved to keyring.')
                            break
                elif keyring.get_password('fetcher', 'username') is not None:
                    db_connect_config['user'] = int(keyring.get_password('fetcher', 'username'))
                    db_connect_config['password'] = keyring.get_password('fetcher', 'password')
            except KeyError:
                # Not found user or password field, proceeding
                info_flush('user/password not found in config_, proceeding...')
        if db_config == 'postgresql':
            conn = psycopg2.connect(**db_connect_config)
        elif db_config == 'pyodbc':
            conn = pyodbc.connect(connect_string_reformatter(**db_connect_config_by_park))
        else:
            error_flush('DB driver not found, aborting')
            sys.exit(1)

        cur = conn.cursor()

        if query_override is not None:
            query = query_override
        else:
            query = f"""
                SET application_name='query_puller'; 
                SELECT {','.join(fields)}
                FROM {schema}
                {query_add}
                LIMIT {limit};
            """
            if formatter:
                query = query_formatter(query)
        if split_by_nmonths is not None:
            if output_type == 'list':
                frame = []
                frame.extend(fetch_one(conn, cur, q, output_type, verbose, db_connect_config, misc=misc) for
                             q in time_range_splitter(query=query, split_by_nmonths=split_by_nmonths))
            else:
                frame = pd.concat(fetch_one(conn, cur, q, output_type, verbose, db_connect_config, misc=misc) for
                             q in time_range_splitter(query=query, split_by_nmonths=split_by_nmonths, is_overlap=True))

                cols_defining = next(([x] for x in ['system_number', 'turbine_id'] if x in frame.columns), [])
                cols_defining.extend(next(([x] for x in ['utc_dttm', 'local_dttm', 'timeline', 'dttm'] if x in frame.columns), []))
                frame = frame.drop_duplicates(cols_defining, 'first').sort_values(cols_defining).reset_index(drop=True)
        else:
            frame = fetch_one(conn, cur, query, output_type, verbose, db_connect_config, misc=misc)

        try:
            misc_str = 'None' if misc is None else misc[0]
            with open(PICKLES_FOLDER / f'whole_{misc_str}.pickle', 'wb') as f:
                pickle.dump(frame, f)
        except Exception as epi:
            error_flush(f'Error upon pickling final DataFrame or List..., code: {repr(epi)}')

        cur.close()
        if verbose:
            info_flush('Cursor of DB connection closed.')
    except psycopg2.OperationalError as operror:  # If keyring saved wrong password
        keyring.delete_password('fetcher', 'username')
        keyring.delete_password('fetcher', 'password')
        print('Login/Password pair incorrect, try again.')
        return query_puller(output_type,
                            schema,
                            fields,
                            limit,
                            query_add,
                            verbose,
                            query_override,
                            formatter,
                            split_by_nmonths,
                            misc,
                            credentials,
                            is_force_input_password=True)
    except (Exception, psycopg2.DatabaseError) as error:
        error_flush(f'Fatal error, execution aborted {repr(error)}')
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()
            if verbose:
                info_flush('DB connection closed.\n-------')

    return frame


def check_and_resume_conn(conn: PsyConn,
                          cur: PsyCur,
                          params: Dict) -> Tuple[PsyConn, PsyCur]:
    """Checking the correctness of Postgres connection, and resuming if needed.

    Parameters
    ----------
    conn
    cur
    params

    Returns
    -------
    Tuple[PsyConn, PsyCur]
        New working connection, cursor tuple.
    """
    try:
        iso_lvl = conn.isolation_level
        if conn is not None and not conn.closed:
            print('Connection exists, returning the same connection:cursor pointer.')
            return conn, cur
        else:
            status = conn.get_transaction_status()
            if status == _ext.TRANSACTION_STATUS_UNKNOWN:
                # server connection lost
                try:
                    conn.close()
                except:
                    print('Did not manage to close the connection, proceeding...')
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                print('Connection reestablished.')
            elif status != _ext.TRANSACTION_STATUS_IDLE:
                conn.rollback()
        print('Isolation_level:', iso_lvl)

    except psycopg2.OperationalError as oe:
        print(repr(oe))
        e_info = inspect.getmro(type(oe))
        print(e_info)
        print('Lost connection to DB is being reestablished...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
    except psycopg2.Error as pe:
        print(repr(pe))
        e_info = inspect.getmro(type(pe))
        print(e_info)
        print('Unexpected DB error, connection being reestablished...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
    except Exception as e:
        print(repr(e))
        e_info = inspect.getmro(type(e))
        print(e_info)
        print('Unknown error:')
        raise
    return conn, cur


def connect_string_reformatter(server: Optional[str] = None,
                               database: Optional[str] = None,
                               user: Optional[str] = None,
                               password: Optional[str] = None,
                               driver: str = 'pyodbc',
                               login_timeout: Optional[int] = None) -> Optional[str]:
    """Generates the string for MS SQL Server connection using pyodbc.
    How to make connect string:
    http://archives.visokio.com/kb/kb.visokio.com/kb/db/dsn-less-odbc.html

    Parameters
    ----------
    login_timeout
        Timeout in seconds, currently not used.
    server
    database
    user
    password

    Returns
    -------
    str
        Connection string formatted for pyodbc SQL connection input.
    """
    if any(x is None for x in [server, database, user, password]):
        print('Did not receive correct config_ input in correct_string_generator, returning None.')
        return None
    # reverse=True to get the latest version of ODBC

    def sort_by_number(drname: str) -> int:
        """Get the first decimal number from string, for sorting."""
        num = re.search(r'\d+', drname)
        return int(num.group(0)) if num is not None else 0

    try:
        odbc_driver = next(x for x in sorted(list(pyodbc.drivers()), key=sort_by_number, reverse=True)
                           if 'odbc driver' in x.lower())
    except StopIteration:
        print('Could not find ODBC driver for SCADA connection, aborting.')
        logging.error('Could not find ODBC driver for SCADA connection, aborting.')
        sys.exit(1)

    raw_config_pyodbc = f"""DRIVER={odbc_driver}
    UID={user}
    AutoTranslate=No
    Network=DBMSSOCN
    WSID=GHDD8TT2E
    APP=Microsoft® Windows® Operating System
    Trusted_Connection=No
    SERVER={server}
    DATABASE={database}
    PWD={password}"""

    # raw_config_adodbapi = f"PROVIDER=SQLOLEDB.1;Data Source={server};Database={database};trusted_connection=no;UID={user};PWD={password};"
    raw_config_adodbapi = f"PROVIDER=SQLOLEDB.1;Data Source={server};Initial Catalog={database};trusted_connection=no;User ID={user};Password={password};"

    config_str_split = raw_config_pyodbc.split('\n')
    config_str_list_of_tup = [(x.split('=')[0].strip(), x.split('=')[1].strip()) for x in config_str_split]
    config_str_ready = ';'.join(x[0] + '={' + x[1] + '}' for x in config_str_list_of_tup)
    config_str_ready = config_str_ready if driver == 'pyodbc' else raw_config_adodbapi
    return config_str_ready


def fetch_one(conn: PsyConn,
              cur: PsyCur,
              query: str,
              output_type: str,
              verbose: bool = False,
              params: Optional[Dict[str, Any]] = None,
              misc: Optional[List] = None) -> Union[List, pd.DataFrame, None]:
    """Return the result of single query, output_type can be list or pd.DataFrame.

    Parameters
    ----------
    misc
    params
    verbose
    cur
        Cursor object.
    conn
        Connection object.
    query
        Query string.
    output_type
        'list' or 'df'

    Returns
    -------
    List[Dict[str_key, data]]
        Query output as List of Dict, pd.DataFrame, or None if no data.

    """

    retry_times = 10
    for i in range(retry_times):
        try:
            if output_type == 'list':  # make a list
                if verbose:
                    print(f'-------\nExecuting query to get {output_type}:', flush=True)
                    print(query, flush=True)

                cur.execute(query)
                desc = cur.description
                column_names = [col[0] for col in desc]
                frame = [dict(zip(column_names, row)) for row in cur.fetchall()]
            elif output_type == 'df':  # make pd.DataFrame
                if verbose:
                    print(f'-------\nExecuting query to get {output_type}:', flush=True)
                    print(query, flush=True)

                frame = pd.read_sql_query(query, conn)
                misc_0 = 'None' if misc is None else misc[0]
                filename_partial = 'partial_' + str(misc_0) + '_' + re.sub(r'[: .]', '_', str(datetime.datetime.now())) + '.pickle'
                try:
                    frame.to_pickle(PICKLES_FOLDER / filename_partial)
                except FileNotFoundError:
                    print(f'Could not save file to {(PICKLES_FOLDER / filename_partial).resolve()}')
                except Exception as e_pick:
                    print(f'Unknown error while pickling, code: {repr(e_pick)}')
            else:
                print('Warning: unknown output format in fetch_one, return pd.DataFrame')
                frame = pd.read_sql_query(query, conn)
            return frame
        except (psycopg2.Error, pd.io.sql.DatabaseError, TypeError) as de:
            print('DatabaseError: ', str(de))
            print(f'Query failed, resuming connection, iteration {i} after 1 min delay...')
            sleep(60)
            conn, cur = check_and_resume_conn(conn, cur, params)
        except Exception as e:
            # Trying to inspect the cause of the error.
            cls1 = e.__class__
            print(cls1.__name__)

            try:
                print(inspect.getmro(type(e)))
                print(inspect.getmro(cls1))
                print(inspect.getclasstree(inspect.getmro(type(e))))
                print(inspect.getclasstree(inspect.getmro(cls1)))

            except Exception as eee:
                print(eee)
                print('could not inspect, proceeding...')

            print('Unknown database connection error:', repr(e), 'in fetching\n', query, '\nReturning no data.')
            return None
    else:
        print("Didn't manage to df data after", retry_times, "times")
        return None


def query_formatter(query: str, toggle_comments: bool = True) -> str:
    """Formats query string to better format: UPPERCASE for SQL keywords, lowercase for the rest,
    newline before primary SQL keywords, newline+4' ' for secondary sentences.

    Parameters
    ----------
    query
        Input query string.
    toggle_comments
        Testing feature with SQL comments. Do not change it.
    Returns
    -------
    str
        Formatted string.

    """

    keywords_all = ['PRECISION',
                    'INTERVAL',
                    'DISTINCT',
                    'BETWEEN',
                    'WINDOW',
                    'DOUBLE',
                    'SELECT',
                    'DELETE',
                    'CREATE',
                    'HAVING',
                    'VALUES',
                    'UPDATE',
                    'INSERT',
                    'ROUND',
                    'LIMIT',
                    'ORDER',
                    'INNER',
                    'OUTER',
                    'ALTER',
                    'WHERE',
                    'TABLE',
                    'COUNT',
                    'GROUP',
                    'LIKE',
                    'JOIN',
                    'NULL',
                    'LEFT',
                    'WHEN',
                    'THEN',
                    'WITH',
                    'DESC',
                    'ELSE',
                    'INTO',
                    'CASE',
                    'CAST',
                    'FROM',
                    'LEAD',
                    'END',
                    'AND',
                    'SET',
                    'AVG',
                    'MIN',
                    'MAX',
                    'SUM',
                    'SQL',
                    'ASC',
                    'ADD',
                    'NOT',
                    'LAG',
                    'AS',
                    'BY',
                    'ON',
                    'OR',
                    'IS']

    keywords_newline_before = ['SELECT',
                               'FROM',
                               'JOIN',
                               'WHERE',
                               'UPDATE',
                               'CREATE',
                               'WITH',
                               'ALTER',
                               'ORDER',
                               'GROUP',
                               'INSERT',
                               'LIMIT',]

    keywords_newline_after = ['SELECT',
                              'FROM',
                              'WHERE',
                              'UPDATE',
                              'CREATE',
                              'WITH',
                              'AND',
                              'BY']

    keywords_newline_before_comma = ['SUM', 'MIN', 'MAX']

    keywords_secondary = sorted(list(set(keywords_all) - set(keywords_newline_before) - set(keywords_newline_after)),
                                reverse=True, key=lambda x: len(x))
    query_original = query

    comm_placeholder_1 = '&&1' if toggle_comments else ''
    query_comments = ['--' + '--'.join(x.split('--')[1:]) for x in query.splitlines() if '--' in x]  # -- comments
    query = reduce(lambda x, y: x.replace(y, comm_placeholder_1), [query] + query_comments)

    comm_placeholder_2 = '&&2' if toggle_comments else ''
    query_comments_star = re.findall(re.escape('/*') + r'.*?' + re.escape('*/'), query, flags=re.DOTALL)
    query = reduce(lambda x, y: x.replace(y, comm_placeholder_2), [query] + query_comments_star)

    new_query = query.lower()
    new_query = re.sub(r'[ ]+', ' ', new_query)  # turn all long spaces ' '
    new_query = re.sub(r'\n+', ' ', new_query)    # delete newlines

    for word in keywords_newline_before:
        new_query = re.sub(fr'\b{word}\b', r'\n' + fr'{word.upper()}', new_query, flags=re.IGNORECASE)

    for word in keywords_newline_after:
        new_query = re.sub(fr'\b{word}\b', fr'{word.upper()}' + r'\n    ', new_query, flags=re.IGNORECASE)

    # words to uppercase only
    for word in keywords_secondary:
        new_query = re.sub(fr'\b{word}\b', fr'{word.upper()}', new_query, flags=re.IGNORECASE)

    # SPECIAL CASES
    # add newline + 4" " before ", sum" or similar
    for word in keywords_newline_before_comma:
        new_query = re.sub(fr'(?P<prefix>,[^\n]*?)\b{word}\b', fr'\g<prefix>\n    {word.upper()}', new_query,
                           flags=re.IGNORECASE)

    # remove newline in BETWEEN ... AND\n
    new_query = re.sub(r'\bbetween\b([\s\S]*?)and\n\s*', r'BETWEEN\1AND ', new_query, flags=re.IGNORECASE)

    # remove unnecessary spaces
    new_query = re.sub(r'\s+\n', r'\n', new_query)
    new_query = re.sub(r'[ ]{4,}', '    ', new_query)
    new_query = re.sub(r'([^ ])[ ]{2,3}([^ ])', r'\1 \2', new_query)

    # remove newlines in compound keywords
    new_query = re.sub(r'([A-Z])\s*\n\s*([A-Z])', r'\1 \2', new_query)

    # adjust BETWEEN / AND statement to  (T >= lower AND T < upper::timestamp + INTERVAL '1 day')
    new_query = new_query.replace("'''", "'")
    patt = re.compile(r"(?P<varname>[\w_]*)\s*BETWEEN\s+'(?P<lower>[^']*?)'\s+AND\s+'(?P<upper>[^']*?)'", flags=re.I)
    betw_elems = re.finditer(patt, new_query)
    for m in betw_elems:
        var = m.group('varname')
        low = m.group('lower')
        upp = m.group('upper')
        new_comparison = f"({var} >= '{low}' AND '{var}' < '{upp}'::timestamp + INTERVAL '1 day')"
        new_query = new_query.replace(m.group(0), new_comparison)

    if toggle_comments:
        # add --comments
        new_query = reduce(lambda x, y: x.replace(comm_placeholder_1, y + '\n', 1), [new_query] + query_comments)
        # add /* comments */
        new_query = reduce(lambda x, y: x.replace(comm_placeholder_2, y, 1), [new_query] + query_comments_star)

        # add leading and trailing newlines as in the original query
        for comm in query_comments + query_comments_star:
            if re.search(r'\n\s*' + re.escape(comm), query_original) and not re.search(r'\n\s*' + re.escape(comm), new_query):
                new_query = new_query.replace(comm, '\n' + comm)
            if re.search(re.escape(comm) + r'\s*\n', query_original) and not re.search(re.escape(comm) + r'\s*\n', new_query):
                new_query = new_query.replace(comm, comm + '\n')

    return new_query


def insert_list_of_dict(input_values: Union[List[Dict], pd.DataFrame],
                        table_name: str,
                        log_object: Optional[logging.Logger] = None) -> bool:
    """Insert list of dict to the given table in schema line by line.

    Parameters
    ----------
    input_values
        List of Dict (list of single rows) or pd.DataFrame (each row = row in a table).
    table_name
        Table address like 'someschema.sometable'.
    log_object
        Logger object.

    Returns
    -------
    bool
        Insert status.

    """
    log_func_info = log_object.info if log_object is not None else print
    log_func_warn = log_object.warning if log_object is not None else print
    is_all_inserted = True
    if isinstance(input_values, list):
        for record in input_values:
            log_func_info(
                COLOR_META + f'Uploading record with tid={record["turbine_id"]}, start={record["mcr_start"]} to {table_name}...')
            # pprint.pprint(record)
            is_status_ok = query_inserter(table_name, record)
            is_all_inserted = is_all_inserted and is_status_ok
    elif isinstance(input_values, pd.DataFrame):
        is_status_ok = query_inserter(table_name, input_values)
    else:
        log_func_warn(f'Unable to inset to table_name {table_name}, unknown input format of {input_values}')
        return False
    status_ok_str = COLOR_INFO + 'OK' + COLOR_NONE if is_status_ok else COLOR_ERROR + 'FAIL' + COLOR_NONE
    status_to_print = f'Record uploaded:'.ljust(60) + status_ok_str
    log_func = log_func_info if is_status_ok else log_func_warn
    log_func(status_to_print)

    return is_all_inserted


if __name__ == '__main__':
    query_str = """SELECT
    system_number,channel_id,utc_dttm,local_dttm,value_avg
FROM
    ge_opd.channel_data_f
WHERE
    system_number in ( 32162028,32162501 ) AND
    channel_id in ( 870,871,872,631,25 ) AND
    ( local_dttm >= '2017-07-24 00:00:00' AND
    local_dttm < ('2019-03-26 00:00:00'::timestamp + INTERVAL '1 day'))
LIMIT 100000000;
"""
    date_a = datetime.datetime(2017, 3, 31, 0, 0)
    date_b = datetime.datetime(2019, 2, 20, 0, 0)
    interval = 2
    rng = pd.date_range(date_a, date_b, freq=f'{interval}M')
    print(rng)
    if date_b not in rng:
        rng = rng.append(pd.date_range(date_b, periods=1))
    print(rng)
    print(pd.date_range(date_a, date_b, freq=f'{interval}M'))