# -*- coding: UTF-8 -*-
import time

import psycopg2
import pymysql
from pyhive import presto
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse

"""
将数据库的连接信息组装成一个connection对象
"""


class Connection(object):
    def __init__(self, conn_type, host, port, schema, username, password):
        self.host = host
        self.port = port
        self.conn_type = conn_type
        self.schema = schema
        self.username = username
        self.password = password

    # 从jdbc_url构造connection
    @classmethod
    def create(cls, jdbc_url, username, password):
        result = urlparse(jdbc_url[5:])
        conn_dict = {'host': result.hostname,
                     'port': result.port,
                     'conn_type': result.scheme,
                     'schema': result.path[1:],
                     'username': username,
                     'password': password}
        return cls(**conn_dict)

    def __str__(self):
        return self.__dict__

    def __repr__(self):
        return str(self.__str__())

    @property
    def jdbc_url(self):
        return "jdbc:{conn_type}://{host}:{port}/{schema}?useCompression=true&socketTimeout=1200000".format(
            **self.__dict__)


# 连接数据库和数仓
class DbConnCursor(object):

    def __init__(self, conn_type, host, port, schema, username, password):
        if conn_type.upper() == 'MYSQL':
            is_linked = False
            time_out = 720
            time_interval = 60
            while not is_linked and time_out > 0:
                try:
                    self.conn = pymysql.connect(host=host,
                                                port=port,
                                                user=username,
                                                password=password,
                                                database=schema,
                                                connect_timeout=31536000)
                    is_linked = True
                except Exception as e:
                    time.sleep(time_interval)
                    time_out = time_out - time_interval
                    print(e)
                    print('reconnect %d ......' % (720 / time_interval - int(time_out / time_interval)))
        elif conn_type.upper() == 'POSTGRESQL':
            self.conn = psycopg2.connect(host=host, port=port, user=username, password=password, database=schema)
        elif conn_type.upper() == 'REDSHIFT':
            self.conn = psycopg2.connect(host=host, port=port, user=username, password=password, database=schema)
        elif conn_type.upper() == 'PRESTO':
            self.conn = presto.connect(host='ec2-54-202-148-204.us-west-2.compute.amazonaws.com',
                                       port=8889,
                                       username='hadoop',
                                       source='airflow',
                                       protocol='http',
                                       catalog='hive',
                                       requests_kwargs={'auth': HTTPBasicAuth('hadoop', 'presto_admin2019')},
                                       schema='default')
        self.cur = self.conn.cursor()

    # 通过传入一个conn对象构造db_cursor
    @classmethod
    def create(cls, conn):
        return cls(**conn.__dict__)

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
