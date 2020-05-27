"""
@File    :   Template.py    
@Software:   PyCharm
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/5/11 18:41  kun.z      1.0         None
"""
DIC_TEMPLATE = {} # unit单元的模板文档
# DIC_TEMPLATE_GET_UNIT_DATA = {} # 获取unit数据的函数模板
DIC_TEMPLATE['ST_PU'] = {}

DIC_TEMPLATE['ST_PU']['frame'] = """
import time
from DalBaseUnit import DalBaseUnit

class $CLASS_NAME$(DalBaseUnit):
    def __init__(self):
        self._start_frame()
        $DB_INIT$
    $FUNCTION_METHOD$
    $DB_METHOD$
    $CALL_UPPER_UNITS$
    $TEST$
if __name__ == '__main__':
    pcu = $CLASS_NAME$()
    pcu.test()
"""

DIC_TEMPLATE['ST_PU']['function_method'] ="""
    def $FUNCTION_NAME$_Info(self):
        # 函数信息
        retInfo={}
        retInfo['accode'] = '$AC_CODE$'
        retInfo['desc'] = '$DESCRIPTION$'
        # 输入的示例
        retInfo['example'] = \'\'\'
            $INPUTE_EXAMPLE$
        \'\'\'
        return retInfo

    def $FUNCTION_NAME$_Meta(self,dicUser,dicInput):
        # 数据权限、版本、时间、元数据大小、压缩数据大小
        retMeta='$META_DATA$'
        return retMeta

    def $FUNCTION_NAME$_Data(self,dicUser,tupleMeta):
        # 请将输出数据作为retData返回
        retData={}        
        # ----------测试数据------------
        retData = $RET_DATA$
        return retData

    def $FUNCTION_NAME$_NewData(self):
        # 数据订阅的更新入口
        dicMeta=$META_DATA$
        dicData=$RET_DATA$
        self.newdata(dicMeta,dicData)
        time.sleep(2)
"""

DIC_TEMPLATE['ST_PU']['get_upper_unit_data_template'] = """
    def _get_$UNIT_NAME$_$FUNCTION_NAME$_data($UPPER_INPUTE$):
        ret_data = {}
        # ----------测试数据------------
        ret_data = $UPPER_OUTPUT_EXAMPLE$
        return ret_data
"""

DIC_TEMPLATE['ST_PU']['test_template'] ="""
    def test(self):
        dicUser={}
        dicUser['name']='hellodal'
        dicUser['accountStauts']='normal'
        dicUser['uidNumber']=500
        dicUser['gidNumber']=200
        dicUser['description']='this is a sample user'
        dicUser['listGPID']=['201','202']
        $FUNCTION_TEST$
        time.sleep(20)
        self.quit()
"""

DIC_TEMPLATE['ST_PU']['test_functest_template'] = """
        dicInfo = self.$FUNCTION_NAME$_Info()
        print('$FUNCTION_NAME$ info:{}',dicInfo)
        dicInput=$INPUTE_EXAMPLE$
        dicMeta = self.$FUNCTION_NAME$_Meta(dicUser,dicInput)
        print('$FUNCTION_NAME$ meta:{}',dicMeta)
        dicData = self.$FUNCTION_NAME$_Data(dicUser,dicMeta)
        print('$FUNCTION_NAME$ data:{}',dicData)
"""

DIC_TEMPLATE['ST_PU']['run_template'] = """
from concurrent import futures
import grpc
import puwrapper_pb2_grpc
from $CLASS_NAME$ import $CLASS_NAME$

def serve(wport,port):
    if wport == 0:
        print('Wport should be set!')
        return
    if port == 0:
        print('Port should be set!')
        return
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    puwrapper_pb2_grpc.add_PURequestServicer_to_server(
        $CLASS_NAME$(), server)
    server.add_insecure_port("[::]:{}".format(port))
    server.start()
    print('----------unit started---------')
    server.wait_for_termination()

if __name__ == '__main__':
    serve(9091,9092)
"""

DIC_TEMPLATE['ST_PU']['ORACLE_TALBE_Template'] = """
    def _get_$TABLENAME$_data(self):
        column_list = self.myconn.get_table_columns("$TABLENAME$")
        columns_to_get = list(column_list.keys())
        res_ret = self.myconn.get_table_data("$TABLENAME$", columnList=columns_to_get,
                                             whereStr='', orderColumn='', Top=10)
        return res_ret
"""
DIC_TEMPLATE['ST_PU']['ORACLE_SQL_Template'] = """
    def _execute_$SQLNAME$_data(self):
        res_ret = self.myconn.sql_excute('$SQLSTRING$')
        return res_ret
"""

DIC_TEMPLATE['ST_PU']['ORACLE_INIT_Template'] = """
        from OracleOper import DalOracle
        self.myconn = DalOracle()
        conn_dict = {}
        conn_dict['user'] = "$USER$"
        conn_dict['pd'] = "$PD$"
        conn_dict['hosts']= "$HOST$"
        conn_dict['port']= "$PORT$"
        conn_dict['dbname']= "$DBNAME$"
        self.myconn.connect(conn_dict)
"""


DIC_TEMPLATE['ST_TU'] = {}
DIC_TEMPLATE['ST_TU']['frame']="""
import os
%s
%s

if __name__ == '__main__'
    run()
"""


# print(DIC_TEMPLATE['ST_PU'].keys())