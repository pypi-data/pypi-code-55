import os

from data_sync.utils.glue_util import GlueUtil

BEELINE_COMMAND = "beeline -u 'jdbc:hive2://{host}/default;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2;'  -n hive "


class HiveUtil(object):
    def __init__(self, target_host, target_db, target_tb, tbl_columns, biz_date, last_date, file_format, is_increment):
        self.target_host = target_host
        self.target_db = target_db
        self.target_tb = target_tb
        self.tb_columns = tbl_columns
        self.biz_date = biz_date
        self.file_format = file_format
        self.is_increment = is_increment
        self.last_date = last_date
        self.dw_columns = None

    def execute(self):
        # 建库建表，执行hive-SQL,不执行则无法判断是否需要更新表结构
        self.do_hive_cmd("CREATE_TABLE")
        # 同步更新表结构,执行hive-SQL，不执行则后面无法获取最新字段列表
        self.do_hive_cmd("UPDATE_TABLE_STRUCTURE")
        # 创建新分区
        self.do_hive_cmd("ADD_PARTITION")

    def do_hive_cmd(self, cmd_type):
        hive_sql = execute_sql.get(cmd_type)()
        print(hive_sql)
        if hive_sql and "" != hive_sql.strip():
            print(
                "******[{cmd_type}] start, table:`{target_db}`.`{target_tb}`*******".format(cmd_type=cmd_type,
                                                                                            **self.__dict__))
            hql_file_path = "/home/ubuntu/data-sync/hql/{target_db}.{target_tb}.hql".format(**self.__dict__)
            with open(hql_file_path, 'wt') as f:
                f.write(hive_sql)
            beeline_command_path = BEELINE_COMMAND.format(host=self.target_host)
            hive_cmd = "{} -f {}".format(beeline_command_path, hql_file_path)
            result = os.system(hive_cmd)
            if result != 0:
                raise Exception('[{cmd_type}] hive sql failed!!!'.format(cmd_type=cmd_type))
            print(
                "******[{cmd_type}] end, table:`{target_db}`.`{target_tb}`*******".format(cmd_type=cmd_type,
                                                                                          **self.__dict__))

    def create_table(self):
        create_sql = """
                   CREATE DATABASE IF NOT EXISTS `{target_db}` LOCATION 's3://cf-data-sync/mysql2s3/{target_db}/';
                   USE `{target_db}`;
                   CREATE external TABLE IF NOT EXISTS `{target_tb}`({tbl_columns})
                   partitioned by (dt string)
                   ROW FORMAT DELIMITED
                   FIELDS TERMINATED BY '\\u0001'
                   STORED AS {file_format}
                   LOCATION 's3://cf-data-sync/mysql2s3/{target_db}/{target_tb}/';
                   """.format(**self.__dict__)
        return create_sql

    def add_partition(self):
        hive_sql = """
                               USE `{target_db}`;
                               ALTER TABLE `{target_tb}` DROP IF EXISTS PARTITION (dt='{biz_date}');
                               ALTER TABLE `{target_tb}` ADD IF NOT EXISTS PARTITION (dt='{biz_date}') location 's3://cf-data-sync/mysql2s3/{target_db}/{target_tb}/dt={biz_date}';
                               """.format(**self.__dict__)
        # 是否增量merge,决定是否更新旧分区
        if self.is_increment and dw_column_num != db_column_num:
            print('db columns num not equal dw columns num, so need update last partition schema')
            alter_last_partition_sql = self.alter_last_partition()
            hive_sql = hive_sql + alter_last_partition_sql
        return hive_sql

    # 修改hive表前一分区的orc-schema
    def alter_last_partition(self):
        glue_util = GlueUtil(self.target_db, self.target_tb)
        self.dw_columns = glue_util.get_columns()
        alter_sql = """
                   USE `{target_db}`;
                   INSERT OVERWRITE TABLE  `{target_tb}` partition(dt='{last_date}') 
                   select {dw_columns} from `{target_tb}`
                   where dt='{last_date}';
                   """.format(**self.__dict__)
        return alter_sql

    def update_table_structure(self):
        # 同步更新表结构,执行hive-SQL，不执行则后面无法获取最新字段列表
        db_column_num = len(self.tbl_columns)
        glue_util = GlueUtil(self.target_db, self.target_tb)
        dw_column_num = glue_util.get_columns_num()
        print('db_column_num:' + str(db_column_num) + ',dw_column_num:' + str(dw_column_num))
        alter_sql = ''
        # 业务库新增字段
        if dw_column_num < db_column_num:
            print('add columns......')
            alter_sql = """
                               USE `{target_db}`;
                               ALTER TABLE  `{target_tb}` replace columns({tbl_columns});
                               """.format(**self.__dict__)
        # 业务库删除字段，hive表不能删字段，不支持rename，此为临时方案
        if dw_column_num > db_column_num:
            print('delete columns......')
            alter_sql = """
                       USE `{target_db}`;
                       DROP  TABLE IF  EXISTS `{target_tb}`;
                       CREATE external TABLE IF NOT EXISTS `{target_tb}`({tbl_columns})
                       partitioned by (dt string)
                       ROW FORMAT DELIMITED
                       FIELDS TERMINATED BY '\\u0001'
                       STORED AS {file_format}
                       LOCATION 's3://cf-data-sync/mysql2s3/{target_db}/{target_tb}/';
                       ALTER TABLE `{target_tb}` DROP IF EXISTS PARTITION (dt='{last_date}');
                       ALTER TABLE `{target_tb}` ADD IF NOT EXISTS PARTITION (dt='{last_date}') location 's3://cf-data-sync/mysql2s3/{target_db}/{target_tb}/dt={last_date}';
                       """.format(**self.__dict__)
        return alter_sql

    execute_sql = {"CREATE_TABLE": create_table, "UPDATE_TABLE_STRUCTURE": update_table_structure,
                   "ADD_PARTITION": add_partition}
    
    def print_obj(self):
        print(self.__dict__)
