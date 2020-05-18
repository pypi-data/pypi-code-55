import ast
import json
import os
import sys
from datetime import datetime, timedelta

from data_sync.utils.db_util import DbConnCursor
from data_sync.utils.hive_util import HiveUtil
from data_sync.utils.msg_util import group_robot
from data_sync.utils.spark_util import SparkUtil

DEFAULT_HDFS = 'hdfs://{host}:8020'
HADOOP_COMMAND_PATH = '/home/ubuntu/emr-hadoop-clis/hadoop/hadoop/bin/hadoop'
HIVE_COMMAND_PATH = '/home/ubuntu/emr-hadoop-clis/hive/hive/bin/hive'
PYTHON2_COMMAND_PATH = '/usr/bin/python'
DATAX_PATH = '/home/ubuntu/app/datax/bin/datax.py'
BEELINE_COMMAND = "beeline -u 'jdbc:hive2://{host}/default;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2;'  -n hive "
IM_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=aa5620cb-b3ef-4057-a954-d11e3027f2b6'
"""
db同步到数仓的公共父类
dataX支持多个相同结构分表同步为一张表，所以源表设为list类型，可以覆盖一到多各种情况
querySql需要字段列表做支持，难以在外部传入，有此需求最好还是重写init_json方法
数据同步完的表结构处理，建议与同步数据分开，以降低耦合
"""


class MysqlToS3(object):

    def __init__(self,
                 connection,
                 tb_name_list,
                 biz_date,
                 target_host,
                 target_db,
                 target_tb,
                 concurrency=6,
                 split_pk=' ',
                 file_format='ORC',
                 where=None,
                 replace_columns=None,
                 ignore_columns=None,
                 primary_key=None,
                 sort_key=None,
                 is_check=True):
        self.connection = connection
        self.tb_name_list = tb_name_list
        self.biz_date = biz_date
        self.target_host = target_host
        self.concurrency = concurrency
        self.split_pk = split_pk
        self.file_format = file_format
        self.where = where
        self.replace_columns = replace_columns
        self.ignore_columns = ignore_columns
        self.target_db = target_db
        self.target_tb = target_tb
        self.primary_key = primary_key
        self.sort_key = sort_key
        self.is_check = is_check

    # 本方法从源库中生成3个list:reader_columns, writer_columns, tbl_columns
    def init_columns(self):
        reader_columns = []
        writer_columns = []
        tbl_columns = []
        if self.connection.conn_type.upper() == 'MYSQL':
            sql = "select COLUMN_NAME,DATA_TYPE from information_schema.COLUMNS " \
                  "where table_name='{table}' and table_schema='{schema}'".format(schema=self.connection.schema,
                                                                                  table=self.tb_name_list[0])
        else:
            sql = '''select attname,typname FROM pg_namespace n,pg_class c,pg_attribute a,pg_type t
                WHERE nspname='{schema}' and n.oid=c.relnamespace and c.relname ='{table}' and a.attnum > 0
                and a.attrelid = c.oid and a.atttypid = t.oid '''.format(schema='public', table=self.tb_name_list[0])
        with DbConnCursor.create(self.connection) as cur:
            cur.execute(sql)
            columns = cur.fetchall()
        column_dict = {}
        if self.replace_columns:
            column_dict = ast.literal_eval(self.replace_columns)
        if self.ignore_columns:
            ignore_columns = self.ignore_columns.split(",")
            print("ignore columns:" + str(ignore_columns))
            columns = [column for column in columns if column[0] not in ignore_columns]
        for column in columns:
            column_name = column[0]
            if column_name in column_dict:
                column_name = column_dict[column_name]
            regular_name = ("`" + column_name + "`") if self.connection.conn_type.upper() == 'MYSQL' else (
                    '"' + column_name + '"')
            reader_columns.append(regular_name)
            column_type = MysqlToS3.type_map(column[1].upper())
            writer_columns.append({"name": column_name, "type": column_type})
            tbl_columns.append("`" + column_name + "` " + column_type)
        return reader_columns, writer_columns, tbl_columns

    # 本方法实现db表到数仓表的字段映射
    @staticmethod
    def type_map(mysql_type):
        d = {
            'INT': 'BIGINT',
            'INT2': 'BIGINT',
            'SMALLINT': 'BIGINT',
            'INT4': 'BIGINT',
            'INT8': 'BIGINT',
            'BIT': 'BIGINT',
            'INTEGER': 'BIGINT',
            'TINYINT': 'BIGINT',
            'MEDIUMINT': 'BIGINT',
            'BIGINT': 'BIGINT',
            'numeric': 'DOUBLE',
            'DECIMAL': 'DOUBLE',
            'NEWDECIMAL': 'DOUBLE',
            'DOUBLE': 'DOUBLE',
            'FLOAT': 'DOUBLE',
            'INT24': 'BIGINT',
            'LONG': 'BIGINT',
            'LONGLONG': 'DECIMAL(38,0)',
            'SHORT': 'BIGINT',
            'TINY': 'BIGINT',
            'VARCHAR': 'STRING',
            'YEAR': 'BIGINT',
            'DATETIME': 'TIMESTAMP',
            'TIMESTAMP': 'TIMESTAMP',
        }
        return d.get(mysql_type, 'STRING')

    # 本方法生成datax执行需要的json参数，个性化较强，一般需要在子类重写
    def init_json(self):
        reader_columns, writer_columns, tbl_columns_list = self.init_columns()
        self.__dict__.update(
            {'reader_columns': reader_columns,
             'writer_columns': writer_columns,
             'tbl_columns': ','.join(tbl_columns_list)})
        reader = "mysqlreader" if self.connection.conn_type.upper() == 'MYSQL' else 'postgresqlreader'
        temp_json = {
            "core": {
                "transport": {
                    "channel": {
                        "speed": {
                            "record": 500000
                        }
                    }
                }
            },
            "job": {
                "content": [
                    {"reader": {
                        "name": reader,
                        "parameter": {
                            "splitPk": self.split_pk,
                            "column": reader_columns,
                            "connection": [
                                {"jdbcUrl": [self.connection.jdbc_url],
                                 "table": self.tb_name_list
                                 }
                            ],
                            "username": self.connection.username,
                            "password": self.connection.password,
                            "where": self.where
                        }
                    },
                        "writer": {
                            "name": "s3writer",
                            "parameter": {
                                "key": "/mysql2s3/{target_db}/{target_tb}/dt={biz_date}".format(**self.__dict__),
                                "bucket": "cf-data-sync",
                                "writeMode": "truncate",
                                "fileType": "orc",
                                "tableName": self.tb_name_list[0],
                                "jdbcUrl": self.connection.jdbc_url,
                                "username": self.connection.username,
                                "password": self.connection.password,
                                "column": writer_columns,
                            }
                        }
                    }
                ],
                "setting": {
                    "speed": {
                        "channel": self.concurrency
                    }
                }
            }
        }
        return temp_json

    # datax的参数拼装，实际执行,一般无需改动
    def run_data_x(self):
        sync_json = self.init_json()
        mysql2s3_json = json.dumps(sync_json, ensure_ascii=False, indent=2)
        json_file_path = "/home/ubuntu/data-sync/json/mysql2hdfs_{target_db}.{target_tb}.json".format(**self.__dict__)
        with open(json_file_path, 'wt') as f:
            f.write(str(mysql2s3_json))
        cmd_param = "--jvm=\"-Xms3g -Xmx3g -Xmn1200m -XX:InitialCodeCacheSize=20m -XX:+UseCodeCacheFlushing  -XX:SurvivorRatio=8 -XX:-UseCompressedClassPointers -XX:MaxMetaspaceSize=256m -XX:InitialBootClassLoaderMetaspaceSize=64m \"  {json_file_path}".format(
            json_file_path=json_file_path)
        print("******************************执行dataX脚本******************************")
        print("/usr/bin/python {datax_path} ".format(datax_path=DATAX_PATH) + cmd_param)
        result = os.system("/usr/bin/python {datax_path} ".format(datax_path=DATAX_PATH) + cmd_param)
        if result != 0:
            raise Exception('dataX failed!!!')

    # 本方法处理dataX同步完数据的建表,同步更新表结果,建分区等工作,如果是增量表还需要进行merge
    def do_post_sql(self):
        reader_columns, writer_columns, tbl_columns = self.init_columns()
        if self.sort_key and self.primary_key:
            is_increment = True
        else:
            is_increment = False
        hive_util = HiveUtil(self.target_host,
                             self.target_db,
                             self.target_tb,
                             tbl_columns,
                             self.biz_date,
                             self.file_format,
                             is_increment)
        hive_util.execute()
        if self.sort_key and self.primary_key:
            self.spark_merge()
        # 数据校验
        if self.is_check and self.connection.conn_type.upper() == 'MYSQL':
            self.data_check()

    # 合并T-2和T-1分区
    def spark_merge(self):
        spark_util = SparkUtil(**self.__dict__)
        spark_util.execute()

    # 目前仅支持单表数据校验
    def data_check(self):
        datetime_dt = datetime.strptime(self.biz_date, '%Y-%m-%d')
        last_dt = (datetime_dt - timedelta(days=1)).strftime('%Y-%m-%d')

        with DbConnCursor('presto',
                          None,
                          None,
                          None,
                          None,
                          None) as cur:
            hql = '''select count(1) from "{}"."{}" where dt='{}' '''.format(self.target_db, self.target_tb, last_dt)
            cur.execute(hql)
            yesterday_result = cur.fetchone()
            hql = '''select count(1) from "{target_db}"."{target_tb}" where dt='{biz_date}' '''.format(**self.__dict__)
            cur.execute(hql)
            today_result = cur.fetchone()
        if yesterday_result[0] != 0:
            diff = (today_result[0] - yesterday_result[0]) / yesterday_result[0]
            print(yesterday_result[0], today_result[0])
            content = "%s.%s数据波动异常dt='%s':count=%d,dt='%s':count=%d" % (
                self.target_db, self.target_tb, last_dt, yesterday_result[0], self.biz_date, today_result[0])
        else:
            with DbConnCursor.create(self.connection) as cur:
                db_sql = "select count(1) from `{}`.`{}`".format(self.connection.schema, self.tb_name_list[0])
                cur.execute(db_sql)
                db_result = cur.fetchone()
            if db_result[0] == 0:
                diff = 0
            else:
                diff = (today_result[0] - db_result[0]) / db_result[0]
            print(db_result[0], today_result[0])
            content = "%s.%s数据波动异常dt='%s',db.count=%d,dw.count=%d" % (
                self.target_db, self.target_tb, self.biz_date, db_result[0], today_result[0])
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c3c307e7-82cc-4d80-aa11-2f12e2268d4f'
        if abs(diff) > 0.5:
            print(content)
            group_robot(url, content)
            print('数据校验异常!!!!')
            sys.exit(255)

    def print_obj(self):
        print(self.__dict__)
