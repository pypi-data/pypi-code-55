# -*- coding: UTF-8 -*-
import boto3


class GlueUtil(object):
    def __init__(self, db_name, table_name):
        self.client = boto3.client('glue', region_name='us-west-2')
        self.db_name = db_name
        self.table_name = table_name

    # 获取hive表（分区字段除外）字段数
    def get_columns_num(self):
        columns_list = self.get_columns_list()
        return len(columns_list)

    # 获取一个表除分区外的所有字段,并用逗号连接成字符串
    def get_columns(self):
        column_list = self.get_columns_list()
        return ','.join(column_list)

    # 获取表（分区字段除外）所有字段名称的list
    def get_columns_list(self):
        response = self.client.get_table(
            DatabaseName=self.db_name,
            Name=self.table_name
        )
        columns = response['Table']['StorageDescriptor']['Columns']
        column_list = []
        for col in columns:
            column_list.append(col['Name'])

        return column_list

    # 获取表的分区s3路径
    def get_partition_loc(self, partition_str):
        response = self.client.batch_get_partition(
            DatabaseName=self.db_name,
            TableName=self.table_name,
            PartitionsToGet=[
                {
                    'Values': [
                        partition_str,
                    ]
                },
            ]
        )

        return response['Partitions'][0]['StorageDescriptor']['Location']

    # 获取表数据大小，如果是分区表则获取指定分区的大小
    def get_table_size(self, partition_str=None):
        table_desc = self.client.get_table(DatabaseName=self.db_name,
                                           Name=self.table_name)
        if not table_desc['Table']['PartitionKeys']:
            data_size = table_desc['Table']['Parameters']['totalSize']
            return int(data_size)
        else:
            if partition_str is not None:
                p_table_desc = self.client.get_partition(
                    DatabaseName=self.db_name,
                    TableName=self.table_name,
                    PartitionValues=[
                        partition_str,
                    ]
                )
                data_size = p_table_desc['Partition']['Parameters']['totalSize']
                return int(data_size)
            else:
                raise Exception('请指定表的分区信息！！！')
