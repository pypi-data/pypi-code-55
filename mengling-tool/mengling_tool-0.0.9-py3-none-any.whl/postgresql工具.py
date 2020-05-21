import psycopg2


# mysql执行类
class postgresqlExecutor():
    def __init__(self, dbname: str, **connect):
        self.dbname = dbname
        self.host = connect.get('host', '127.0.0.1')
        self.port = connect.get('port', 5432)
        self.user = connect.get('user', 'postgres')
        self.password = connect.get('password', '246822')
        # 设置返回数据类型
        self.dataclass = connect.get('dataclass', list)
        # 打开数据库连接
        self.db = psycopg2.connect(host=self.host, port=self.port,
                                   user=self.user, password=self.password,
                                   database=self.dbname)

        self.cursor = self.db.cursor()

    # 使用sql操作
    def run(self, sql, datas: list = None, ifdatas=False):
        try:
            # 类型控制，避免出错
            if datas != None: datas = [str(value) for value in datas]
            # 执行sql语句
            try:
                self.cursor.execute(sql, datas)
            except:
                self.db.ping()
                self.cursor = self.db.cursor()
                self.cursor.execute(sql, datas)
            lies = list()  # 列名
            if self.cursor.description != None:
                for lie in self.cursor.description:
                    lies.append(lie[0])
            datas = self.dataclass(self.cursor.fetchall()) if ifdatas else None
            return [lies, datas]
        except Exception as e:
            print('\033[31m' + sql)
            print("datas:", str(datas))
            print("\033[30m命令错误", e)
            return None

    def close(self):
        try:
            self.db.close()
        except:
            pass

    '''事务操作'''

    # 提交事务
    def commit(self):
        try:
            self.db.commit()
        except:
            self.db.ping()
            self.cursor = self.db.cursor()
            self.db.commit()

    # 事务回滚
    def rollback(self):
        self.db.rollback()

    '''增删查改'''

    # 查询
    def select(self, lies, mode_table, **parameters):
        try:
            # 列名组
            if type(lies) != str:
                lie = ','.join(lies)
            else:
                lie = lies
            # 表名
            sql = "select " + lie + " from " + mode_table + " where " + \
                  parameters.get("where", 'True') + " " + parameters.get("other", "")
            return self.run(sql, ifdatas=True)
        except Exception as e:
            print("查询失败！")
            print(e)
            return None, None

    # 插入
    def insert(self, mode_table: str, lies: list, values: list):
        try:
            assert len(lies) > 0 and len(lies) == len(values), "数量有误！"
            # 列名组格式处理
            lies = list(lies)
            liestr_tuple = "(" + ','.join(lies) + ")"
            cstr_tuple = "(" + ','.join(["%s" for i in range(len(lies))]) + ")"
            # 插入语句
            sql = "INSERT INTO " + mode_table + liestr_tuple + " VALUES " + cstr_tuple
            return self.run(sql, values)
        except Exception as e:
            print("插入失败！")
            print(e)

    def insert_dict(self, mode_table: str, lie_value_dict: dict):
        lies, value = [], []
        for lie in list(lie_value_dict.items()):
            lies.append(lie[0])
            value.append(lie[1])
        return self.insert(mode_table, lies, value)

    # 删除
    def delete(self, mode_table, where: str):
        try:
            sql = "DELETE FROM " + mode_table + " WHERE " + where
            return self.run(sql)
        except Exception as e:
            print("删除失败！")
            print(e)

    # 修改
    def update(self, mode_table, lies: list, values: list, where: str):
        try:
            assert len(lies) > 0 and len(lies) == len(values), "数量有误！"
            sql = "UPDATE " + mode_table + " SET "
            # 列名组及参数
            lies = list(lies)
            for i in range(len(lies)):
                sql += lies[i] + '=%s,'
            sql = str(sql[0:-1])
            sql += " WHERE " + where
            return self.run(sql, values)
        except Exception as e:
            print("更新失败！")
            print(e)

    '''表操作'''

    # 创建表
    def createTable(self, mode_table, columns: list, **args):
        # CREATE TABLE table_name (column_name column_type);  Create Table If Not Exists
        key = args.get('key', None)
        columnclassdict = args.get('columnclassdict', {})
        # 列类型进行默认赋值
        for i in range(len(columns)):
            columnclassdict[i] = columnclassdict.get(i, 'text')
        # Create Table If Not Exists
        noexistcreate = args.get('noexistcreate', False)
        try:
            assert len(columns) > 0, "数量有误！"
            sql = '''
                        Create Table {exists} {mode_table} 
                        ({lies} {key})
                    '''.format(exists='If Not Exists' if noexistcreate else "", mode_table=mode_table,
                               lies=",".join(
                                   ["%s %s" % (columns[i], columnclassdict[i]) for i in range(len(columns))]),
                               key=" ,PRIMARY KEY(" + key + ")" if key != None else "")
            return self.run(sql)
        except Exception as e:
            print("创建表失败！")
            print(e)

    # 删除表
    def deleteTable(self, mode_table):
        # DROP TABLE mode_table_name
        try:
            sql = "DROP TABLE " + mode_table
            return self.run(sql)
        except Exception as e:
            print("删除表失败！")
            print(e)

    # 删除列
    def deleteColumn(self, mode_table, liename):
        # ALTER TABLE mode_tablename  DROP i;
        try:
            sql = "ALTER TABLE " + mode_table + " DROP " + liename
            return self.run(sql)
        except Exception as e:
            print("删除列失败！")
            print(e)

    # 修改列属性
    def setColumn(self, mode_table, liename, newname, dataclass="VARCHAR(255)"):
        try:
            sql = "ALTER TABLE " + mode_table + " CHANGE " + " ".join([liename, newname, dataclass])
            return self.run(sql)
        except Exception as e:
            print("修改列失败！")
            print(e)

    # 新增列
    def addColumn(self, mode_table, liename, dataclass="VARCHAR(255) ", other=""):
        # ALTER mode_table `tcl科技 (深证:000100)` add `昨日收盘` VARCHAR(255) AFTER `今日收盘`
        try:
            sql = "ALTER TABLE " + mode_table + " ADD " + liename + " " + dataclass + other
            return self.run(sql)
        except Exception as e:
            print("新增列失败！")
            print(e)


# 测试
if __name__ == "__main__":
    sqltool = postgresqlExecutor("test")
    resultlist = sqltool.createTable("ttt", ["id", "ce"], ["int", "varchar(255)"], "id")

    sqltool.commit()
