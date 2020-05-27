import pymssql


# 建立数据库连接
def conn_create(ip, user_name, password, db_name):
    connect = pymssql.connect(ip, user_name, password, db_name)
    res = {}
    if connect:
        print("连接成功!")
        res["status"] = True
        res["result"] = connect
    else:
        res["status"] = False
        res["result"] = "error"
    return res


# 关闭连接信息
def conn_close(conn):
    if conn["status"]:
        connect = conn["result"]
        connect.close()


# 执行SQL语句
def sql_exec(conn, sql):
    if conn["status"]:
        connect = conn["result"]
        cursor = connect.cursor()
        cursor.execute(sql)  # 执行sql语句
        connect.commit()  # 提交
    else:
        print("连接信息有误，请检查")


# 插入SQL
def sql_insert(conn, sql):
    sql_exec(conn, sql)


# 更新SQL
def sql_update(conn, sql):
    sql_exec(conn, sql)


# 删除SQL
def sql_delete(conn, sql):
    sql_exec(conn, sql)


# 查询SQL
def sql_select(conn, sql):
    if conn["status"]:
        connect = conn["result"]
        cursor = connect.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()  # 读取查询结果,
        cursor.close()  # 关闭游标
        return res


