import pymysql


# mysql执行类
class mysqlExecutor():
    def __init__(self, dbname: str, **connect):
        self.dbname = dbname
        self.host = connect.get('host', '127.0.0.1')
        self.port = connect.get('port', 3306)
        self.user = connect.get('user', 'root')
        self.passwd = connect.get('passwd', '246822')
        self.charset = connect.get('charset', 'UTF8')
        # 设置返回数据类型
        self.dataclass = connect.get('dataclass', list)
        # 打开数据库连接
        self.db = pymysql.connect(host=self.host, port=self.port,
                                  user=self.user, passwd=self.passwd,
                                  db=self.dbname, charset=self.charset)

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
    def select(self, lies, table, **parameters):
        try:
            # 列名组
            lie = ""
            if type(lies) == str:
                lie = ("`" + lies + "`") if lies != '*' else lies
            else:
                for l in lies:
                    lie += '`' + l + '`,'
                lie = ''.join(lie[0:-1])
            # 表名
            table = "`" + table + "`"
            sql = "select " + lie + " from " + table + " where " + \
                  parameters.get("where", 'True') + " " + parameters.get("other", "")
            return self.run(sql, ifdatas=True)
        except Exception as e:
            print("查询失败！")
            print(e)
            return None, None

    # 插入
    def insert(self, table: str, lies: list, values: list):
        try:
            assert len(lies) > 0 and len(lies) == len(values), "数量有误！"
            # 表名
            table = "`" + table + "`"
            # 列名组格式处理
            lies = list(lies)
            for i in range(len(lies)):
                lies[i] = '`' + lies[i] + '`'
            liestr_tuple = str(tuple(lies)).replace("'", "")
            cstr_tuple = str(tuple(["%s" for i in range(len(lies))])).replace("'", "")
            # 处理单个数据时有多余逗号的情况
            if len(lies) < 2:
                liestr_tuple = liestr_tuple.replace(',', '')
                cstr_tuple = cstr_tuple.replace(',', '')
            # 插入语句
            sql = "INSERT INTO " + table + liestr_tuple + " VALUES " + cstr_tuple
            return self.run(sql, values)
        except Exception as e:
            print("插入失败！")
            print(e)

    def insert_dict(self, table: str, lie_value_dict: dict):
        lies, value = [], []
        for lie in list(lie_value_dict.items()):
            lies.append(lie[0])
            value.append(lie[1])
        return self.insert(table, lies, value)

    # 删除
    def delete(self, table, where: str):
        try:
            # 表名
            table = "`" + table + "`"
            sql = "DELETE FROM " + table + " WHERE " + where
            return self.run(sql)
        except Exception as e:
            print("删除失败！")
            print(e)

    # 修改
    def update(self, table, lies: list, values: list, where: str):
        try:
            assert len(lies) > 0 and len(lies) == len(values), "数量有误！"
            # 表名
            table = "`" + table + "`"
            sql = "UPDATE " + table + " SET "
            # 列名组及参数
            lies = list(lies)
            for i in range(len(lies)):
                sql += '`' + lies[i] + '`=%s,'
            sql = str(sql[0:-1])
            sql += " WHERE " + where
            return self.run(sql, values)
        except Exception as e:
            print("更新失败！")
            print(e)

    '''表操作'''

    # 创建表
    def createTable(self, table, columns: list, **args):
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
                Create Table {exists} `{table}` 
                ({lies} {key})
            '''.format(exists='If Not Exists' if noexistcreate else "", table=table,
                       lies=",".join(["`%s` %s" % (columns[i], columnclassdict[i]) for i in range(len(columns))]),
                       key=" ,PRIMARY KEY(`" + key + "`)" if key != None else "")
            return self.run(sql)
        except Exception as e:
            print("创建表失败！")
            print(e)

    # 删除表
    def deleteTable(self, table):
        # DROP TABLE table_name
        try:
            sql = "DROP TABLE `" + table + "`"
            return self.run(sql)
        except Exception as e:
            print("删除表失败！")
            print(e)

    # 删除列
    def deleteColumn(self, table, liename):
        # ALTER TABLE tablename  DROP i;
        try:
            sql = "ALTER TABLE `" + table + "` DROP `" + liename + "`"
            return self.run(sql)
        except Exception as e:
            print("删除列失败！")
            print(e)

    # 修改列属性
    def setColumn(self, table, liename, newname, dataclass="VARCHAR(255)"):
        try:
            sql = "ALTER TABLE `" + table + "` CHANGE `" + liename + "` `" + newname + "` " + dataclass
            return self.run(sql)
        except Exception as e:
            print("修改列失败！")
            print(e)

    # 新增列
    def addColumn(self, table, liename, dataclass="VARCHAR(255)", other=""):
        # ALTER TABLE `tcl科技 (深证:000100)` add `昨日收盘` VARCHAR(255) AFTER `今日收盘`
        try:
            sql = "ALTER TABLE `" + table + "` ADD `" + liename + "` " + dataclass + other
            return self.run(sql)
        except Exception as e:
            print("新增列失败！")
            print(e)


# 测试
if __name__ == "__main__":
    sqltool = mysqlExecutor("test")
    resultlist = sqltool.createTable("ttt", ["id", "ce"], ["int", "varchar(255)"], "id")

    sqltool.commit()
