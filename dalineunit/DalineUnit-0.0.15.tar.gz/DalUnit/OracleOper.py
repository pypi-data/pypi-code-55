import cx_Oracle

class DalOracle:
    def __init__(self):
        self.connection = False

    def connect(self,connetion_dict: dict):
        try:
            user = connetion_dict['user']
            passwd = connetion_dict['pd']
            hosts = connetion_dict['hosts']
            port = connetion_dict['port']
            dbname = connetion_dict['dbname']
            str_tmp = "%s:%s/%s"%(hosts,port,dbname)
            self.db = cx_Oracle.connect(user, passwd, str_tmp)
            self.mycursor = self.db.cursor()
            self.connection = True
        except Exception as e:
            return str(e)

    def get_all_tables(self):
        """
        获取所有表明
        :return:
        """
        if self.connection:
            try:
                str_sql = "select table_name from user_tables "
                self.mycursor.execute(str_sql)
                sql_res = self.mycursor.fetchall()
                table_list = []
                for each in sql_res:
                    table_list.append(each[0])
                return table_list
            except Exception as e:
                return str(e)
        else:
            return 'please connect to DB'

    def get_table_columns(self, table_name: str):
        """
        获取表所有字段
        :param table_name:
        :return:
        """
        if self.connection:
            try:
                key_type_dict = {}
                str_sql = "SELECT column_name, data_type FROM all_tab_cols WHERE table_name = '%s'" % (table_name)
                self.mycursor.execute(str_sql)
                table_info = self.mycursor.fetchall()
                for each_table_info in table_info:
                    key_type_dict[each_table_info[0]] = each_table_info[1]
                return key_type_dict
            except Exception as e:
                return str(e)
        else:
            return 'please connect to DB'

    def sql_excute(self,sql_e: str):
        """
        执行语句，并返回结果
        :param sql_e:
        :return:
        """
        if self.connection:

            try:
                sql_res = self.mycursor.execute(sql_e)
                ret_res = [each for each in sql_res]
                return ret_res
            except Exception as e:
                return str(e)
        else:
            return 'please connect to DB'
    def get_table_data(self,tableName: str, columnList: list = [] , whereStr: str = '', orderColumn: str = "", Top: int =0):
        """
        获取表数据
        :param tableName:
        :param columnList:
        :param where:
        :return:
        """
        if self.connection:
            try:
                order_str = ''
                where_str = ''
                if not columnList:
                    columnList = []
                    columnList.append('*')

                if whereStr.strip():
                    where_str = 'where ' + whereStr
                    if Top:
                        where_str = where_str + ' and rownum< '+ str(Top)
                elif Top:
                    where_str = 'where rownum< ' + str(Top+1)

                if orderColumn.strip():
                    order_str = "order by " + orderColumn
                sql_e = "select %s from %s %s %s" % (','.join(columnList), tableName, where_str, order_str )

                sql_res = self.mycursor.execute(sql_e)
                ret_res = [each for each in sql_res]
                return ret_res
            except Exception as e:
                return str(e)
        else:
            return 'please connect to DB'
    # def fetch

oracle_connection = DalOracle()
def test():
    conn_dict = {}
    myconn = DalOracle()

    conn_dict['user'] = "system"
    conn_dict['pd'] = "Passw0rd"
    conn_dict['hosts']= "192.168.0.231"
    conn_dict['port']= "1521"
    conn_dict['dbname']= "ZHANG.ZKTEST"

    myconn.connect(conn_dict)
    print(myconn.get_all_tables())
    print(myconn.get_table_columns("LOGMNR_PARAMETER$"))
    print(myconn.get_table_columns("STUDENT"))
    sql_e = 'select * from STUDENT'
    print(myconn.sql_excute(sql_e))

    print(myconn.get_table_data('STUDENT',['XH','XM']))
    print(myconn.get_table_data('STUDENT'))
    print(myconn.get_table_data('STUDENT',['XH','XM'],Top=1))
    print(myconn.get_table_data('STUDENT',Top=1))

if __name__ == '__main__':
    test()

