#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/25 17:05
# @Author : yangpingyan@gmail.com

import os, json, inspect, sys
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

def sql_connect(sql_file, ssh_pkey=None):
    '''连接数据库'''
    with open(sql_file, encoding='utf-8') as f:
        sql_info = json.load(f)
        ssh_host = sql_info['ssh_host']
        ssh_user = sql_info['ssh_user']
        sql_address = sql_info['sql_address']
        sql_user = sql_info['sql_user']
        sql_password = sql_info['sql_password']
        database = sql_info['database']

        if ssh_pkey is not None:
            server = SSHTunnelForwarder((ssh_host, 22), ssh_username=ssh_user, ssh_pkey=fr"{ssh_pkey}",
                                        remote_bind_address=(sql_address, 3306))
            server.start()
            host="127.0.0.1"
            port = server.local_bind_port
        else:
            host = sql_address
            port = 3306

        sql_engine = create_engine(f'mysql+mysqldb://{sql_user}:{sql_password}@{host}:{port}/{database}?charset=utf8')

    return sql_engine

# sql_engine = create_engine('sqlite:///:memory:')  # sqlite database in memory

if __name__ == '__main__':
    print("Mission start!")
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
    exec_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    if 'ypyapi' not in exec_path:
        exec_path = os.path.join(exec_path, 'ypyapi')

    sql_engine = sql_connect( os.path.join(exec_path, 'bi_db.json'))

    # 创建对象的基类:
    Base = declarative_base()

    # 定义User对象:
    class User(Base):
        # 表的名字:
        __tablename__ = 'user'

        # 表的结构:
        id = Column(String(20), primary_key=True)
        name = Column(String(20))

        # 初始化数据库连接:
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=sql_engine)

    # 创建session对象:
    session = DBSession()
    # 创建新User对象:
    new_user = User(id='5', name='Bob')
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()

    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    user = session.query(User).filter(User.id=='5').one()
    # 打印类型和对象的name属性:
    print('type:', type(user))
    print('name:', user.name)
    # 关闭Session:
    session.close()



    print("Mission complete!")



    from sqlalchemy import (create_engine, Table, Column, Integer,
    String, MetaData)
    meta = MetaData()
    cars = Table('bus', meta,
         Column('Id', Integer, primary_key=True),
         Column('Name', String),
         Column('Price', Integer)
    )

    meta = MetaData()
    meta.reflect(bind=sql_engine)

    for table in meta.tables:
        print(table)