import os
import json
from .Template import DIC_TEMPLATE
from .DesignFile import DesignFile
from .GenTestData import gem_test_data
from .DalDecorate import gen_exception_decorate
from .OracleOper import oracle_connection

class DalGen:

    def __init__(self):
        super().__init__()
        self.template_list = DIC_TEMPLATE

    def _get_config(self, config_file):
        """
        读取配置文件，比如：包括模板文件位置等
        :param config_file:
        :return:
        """
        pass

    def _get_all_template_type(self):
        """
        获取所有模板类型
        :return:所有类型
        """
        return self.template_list.keys()

    def read_design_file(self, design_file_name: str):
        """
        读取设计文件的文档，返回设计文件的关键字
        :param design_file_name:设计文件文档
        :return:文档关键字字典，不做成员变量，返回格式{'sttime':'datetime','symbol':'string'}
        """
        self._design_file = DesignFile(design_file_name)
        return self._design_file.get_all_design_unit()

    def _gen_test_data(self, data_dic: dict):
        """
        给定数据类型，生成测试数据
        Enum：列表中随机选取1个数据
        基本数据类型: 按类型创建

        :param data_dic: 单个单元的设计字典，格式{'sttime':'datetime','symbol':'string'}
        :return:测试数据 json
        """
        for each_val in data_dic:
            if isinstance(data_dic[each_val],dict):
                data_dic[each_val] = self._gen_test_data(data_dic[each_val])  # 递归实现无限遍历
            else:
                data_dic[each_val] = gem_test_data.gen_test_data_str(data_dic[each_val])
        return data_dic
        # return json.dumps(data_dic)

    def _gen_get_upper_units_data(self, unit_name_list: list):
        """
        生成获取父节点数据的方法
        1、若能找到父节点的文档或单元信息，将父节点的paralist作为参数填入
        2、找不到父节点，生成空函数
        :param unit_name_list: 上级unit名称列表
        :return:父节点的数据
        """
        ret_scritp = ''
        all_unit_dic = self._design_file.get_all_design_unit()  # todo: 目前无法获取全部的unit单元函数信息，暂用设计文档的信息替代
        for each_parent_unit in unit_name_list:
            if each_parent_unit in all_unit_dic:
                func_script_tmp = ''
                for each_upper_function in all_unit_dic[each_parent_unit]['function_list']:
                    scritpTemplate = DIC_TEMPLATE['ST_PU']['get_upper_unit_data_template']
                    scritpTemplate = scritpTemplate.replace('$UNIT_NAME$',all_unit_dic[each_parent_unit]['unit_info']['unitname'])
                    scritpTemplate = scritpTemplate.replace('$FUNCTION_NAME$',each_upper_function)
                    str_tmp = 'self,' + ','.join( all_unit_dic[each_parent_unit]['function_list'][each_upper_function]['input'].keys() )
                    scritpTemplate = scritpTemplate.replace('$UPPER_INPUTE$',str_tmp)
                    str_tmp = json.dumps( self._gen_test_data(all_unit_dic[each_parent_unit]['function_list'][each_upper_function]['output']) )
                    scritpTemplate = scritpTemplate.replace('$UPPER_OUTPUT_EXAMPLE$',str_tmp)
                    func_script_tmp = func_script_tmp + scritpTemplate
            else:
                func_script_tmp = ''
            ret_scritp = ret_scritp + func_script_tmp
        return ret_scritp

    def _gen_unit_function_script(self,function_dict: dict):
        """
        根据函数字典生成函数脚本
        :param function_dict:
        :return:
        """
        ret_script = ''
        for each_func in function_dict:
            tmp_script = ''
            tmp_script = tmp_script + DIC_TEMPLATE['ST_PU']['function_method']
            tmp_script = tmp_script.replace('$FUNCTION_NAME$',each_func)
            tmp_script = tmp_script.replace('$AC_CODE$',function_dict[each_func]['meta_data']['acCode'])
            tmp_script = tmp_script.replace('$DESCRIPTION$',function_dict[each_func]['meta_data']['description'])
            tmp_script = tmp_script.replace('$INPUTE_EXAMPLE$',json.dumps(function_dict[each_func]['input']) )
            tmp_script = tmp_script.replace('$META_DATA$',json.dumps(function_dict[each_func]['meta_data'],ensure_ascii=False) )
            tmp_script = tmp_script.replace('$RET_DATA$',json.dumps(self._gen_test_data(function_dict[each_func]['output']) ) )

            ret_script = ret_script + tmp_script
        return ret_script

    def _gen_test_script(self,function_dict: dict):
        """
        根据函数字典生成函数测试脚本
        :param function_dict:
        :return:
        """
        tmp_script = DIC_TEMPLATE['ST_PU']['test_template']
        tmp_func_script = ''
        for each_func in function_dict:
            # 对每个函数生成 info  meta   data三个测试用例函数
            str_tmp = DIC_TEMPLATE['ST_PU']['test_functest_template']
            str_tmp = str_tmp.replace('$FUNCTION_NAME$',each_func)
            str_tmp = str_tmp.replace('$INPUTE_EXAMPLE$',json.dumps(function_dict[each_func]['input']) )
            tmp_func_script = tmp_func_script + str_tmp
        tmp_script = tmp_script.replace('$FUNCTION_TEST$',tmp_func_script)

        return tmp_script
    def _gen_Oracle_script(self, DB_dict: dict):
        """
        生成数据库脚本
        :param DB_dict:
        :return:
        """
        db_script_dic = {}

        # 初始化模板
        db_script_dic['db_init'] = DIC_TEMPLATE['ST_PU']['ORACLE_INIT_Template']
        db_script_dic['db_init'] = db_script_dic['db_init'].replace("$USER$",DB_dict['user'])
        db_script_dic['db_init'] = db_script_dic['db_init'].replace("$PD$",DB_dict['pd'])
        db_script_dic['db_init'] = db_script_dic['db_init'].replace("$HOST$",DB_dict['hosts'])
        db_script_dic['db_init'] = db_script_dic['db_init'].replace("$PORT$",DB_dict['port'])
        db_script_dic['db_init'] = db_script_dic['db_init'].replace("$DBNAME$",DB_dict['dbname'])

        oracle_connection.connect(DB_dict)
        if not oracle_connection.connection:
            db_script_dic['method_script'] = ''
            return db_script_dic

        # 表函数模板
        db_script_dic['method_script'] = ''

        tablelist = oracle_connection.get_all_tables()
        for each_table in tablelist:
            each_table_tmp = each_table
            if "$" in each_table_tmp:
                each_table_tmp = each_table_tmp.replace('$','')
            table_script_tmp = DIC_TEMPLATE['ST_PU']['ORACLE_TALBE_Template']
            table_script_tmp = table_script_tmp.replace('$TABLENAME$',each_table_tmp)
            db_script_dic['method_script'] = db_script_dic['method_script']+table_script_tmp
        if 'SQL' in DB_dict:
            for each_sql_name in DB_dict['SQL']:
                sql_script_tmp = DIC_TEMPLATE['ST_PU']['ORACLE_SQL_Template']
                sql_script_tmp = sql_script_tmp.replace('$SQLNAME$',each_sql_name)
                sql_script_tmp = sql_script_tmp.replace('$SQLSTRING$',DB_dict['SQL'][each_sql_name])
                db_script_dic['method_script'] = db_script_dic['method_script'] + sql_script_tmp
        return db_script_dic
    def _gen_SqlServer_script(self, DB_dict: dict):
        """
        生成数据库脚本
        :param DB_dict:
        :return:
        """
        db_script_dic = {}
        db_script_dic['method_script'] = ''
        db_script_dic['db_init'] = ''

    def _gen_Mysql_script(self, DB_dict: dict):
        """
        生成数据库脚本
        :param DB_dict:
        :return:
        """
        db_script_dic = {}
        db_script_dic['method_script'] = ''
        db_script_dic['db_init'] = ''


    def _gen_DB_script(self, DB_dict: dict):
        """
        生成DB部分的脚本,需要连接数据库，然后扫描所有表
        需要生成连接函数，在init中调用
        设计文档可能连不了数据库，无法得到表结构，则打印提示，生成注释的示例
        :param DB_dict:
        :return:
        """
        if DB_dict['dbtype'].lower() == 'oracle':
            db_script_dic = self._gen_Oracle_script(DB_dict)
        elif DB_dict['dbtype'].lower() == 'sqlserver':
            db_script_dic = self._gen_SqlServer_script(DB_dict)
        elif DB_dict['dbtype'].lower() == 'mysql':
            db_script_dic = self._gen_Mysql_script(DB_dict)

        return db_script_dic

    @gen_exception_decorate
    def gen_py(self, unit_dic: dict):
        """
        生成py文件
        :param unit_dic: 单个单元的设计字典
        :param gen_test_data: 是否生成测试数据
        :return:
        """
        if unit_dic['unit_info']['type'] == 'pu':
            scritpTemplate = DIC_TEMPLATE['ST_PU']['frame']
            # unit名称替换
            scritpTemplate =scritpTemplate.replace('$CLASS_NAME$',unit_dic['unit_info']['unitname'])

            # 将每个方法生成四个函数
            str_tmp = self._gen_unit_function_script(unit_dic['function_list'])  # done
            scritpTemplate =scritpTemplate.replace('$FUNCTION_METHOD$',str_tmp)

            if 'data_base' in unit_dic and unit_dic['data_base']:
                # 根据数据库配置生成function，每个表生成简单的获取表数据语句，此方法不同于function，只生成单个的函数
                db_script_dic = self._gen_DB_script(unit_dic['data_base'])
                scritpTemplate = scritpTemplate.replace('$DB_METHOD$', db_script_dic['method_script'])
                scritpTemplate = scritpTemplate.replace('$DB_INIT$', db_script_dic['db_init'])
            else:
                scritpTemplate = scritpTemplate.replace('$DB_METHOD$', '')
                scritpTemplate = scritpTemplate.replace('$DB_INIT$', '')

            # 调用上层pu方法脚本生成，如果db_unit不会同时支持upper_unit，将下部分移到上面else后面
            if 'upper_unit' in unit_dic:
                str_tmp = self._gen_get_upper_units_data(unit_dic['upper_unit'])  # done
                scritpTemplate =scritpTemplate.replace('$CALL_UPPER_UNITS$',str_tmp)
            else:
                scritpTemplate = scritpTemplate.replace('$CALL_UPPER_UNITS$', '')

            # 测试用例生成
            str_tmp = self._gen_test_script(unit_dic['function_list'])  # done
            scritpTemplate =scritpTemplate.replace('$TEST$', str_tmp )

            # 写文件
            if not os.path.exists(unit_dic['unit_info']['folder']):
                os.mkdir(unit_dic['unit_info']['folder'])
            sub_path = unit_dic['unit_info']['folder']+unit_dic['unit_info']['unitname']+'\\'
            if not os.path.exists(sub_path):
                os.mkdir(sub_path)
            scriptF = sub_path + unit_dic['unit_info']['unitname'] + '.py'
            file_script = open(scriptF, 'w+',encoding='utf8')
            file_script.write(scritpTemplate )
            file_script.close()
        elif unit_dic['unit_info']['type'] == 'tu':
            scritpTemplate = DIC_TEMPLATE['ST_TU']
        else:
            # print('type should be pu or tu')
            return 'type should be pu or tu'

    @gen_exception_decorate
    def gen_run(self, unit_dic: dict):
        """
        生成运行测试文件
        """
        run_template = DIC_TEMPLATE['ST_PU']['run_template']
        run_template = run_template.replace('$CLASS_NAME$',unit_dic['unit_info']['unitname'])
        # 写文件
        if not os.path.exists(unit_dic['unit_info']['folder']):
            os.mkdir(unit_dic['unit_info']['folder'])
        sub_path = unit_dic['unit_info']['folder'] + unit_dic['unit_info']['unitname'] + '\\'
        if not os.path.exists(sub_path):
            os.mkdir(sub_path)
        scriptF = sub_path + 'run_test.py'
        file_script = open(scriptF, 'w+', encoding='utf8')
        file_script.write(run_template)
        file_script.close()
        pass

    @gen_exception_decorate
    def gen_info(self, unit_dic: dict):
        """
        生成info文件
        :param unit_dic: 单个单元的设计字典
        :return:
        """
        dicInfo = {}
        dicInfo['folder'] = unit_dic['unit_info']['folder']
        dicInfo['name'] = unit_dic['unit_info']['unitname']
        dicInfo['type'] = unit_dic['unit_info']['type']
        dicInfo['lang'] = unit_dic['unit_info']['lang']

        if not os.path.exists(unit_dic['unit_info']['folder']):
            os.mkdir(unit_dic['unit_info']['folder'])
        sub_path = unit_dic['unit_info']['folder'] + unit_dic['unit_info']['unitname'] + '\\'
        if not os.path.exists(sub_path):
            os.mkdir(sub_path)
        infoF = sub_path +unit_dic['unit_info']['unitname']+ '_info.json'
        file_script = open(infoF, 'w+',encoding='utf8')
        file_script.write(json.dumps(dicInfo))
        file_script.close()

    def gen_unit(self, design_file: str):
        """
        通过设计文档生成unit单元
        :param design_file: 设计文档
        :param gen_test_data: 是否生成测试数据
        :return:
        """
        design_units = self.read_design_file(design_file)
        self._design_file.gen_design_md()
        for each_unit in design_units:
            self.gen_py(design_units[each_unit])
            self.gen_info(design_units[each_unit])
            self.gen_run(design_units[each_unit])
import click
@click.command()
@click.option('--designPath', help='target design file path')
def run(designPath):
    dalgen = DalGen()
    dalgen.gen_unit(designPath)

def GenScriptFromMd(designPath):
    dalgen = DalGen()
    dalgen.gen_unit(designPath)

if __name__ == '__main__':
    # md_path = input('请输入设计文档路径：')
    # GenScriptFromMd(md_path)
    GenScriptFromMd(r'UnitDesign\design_test2.md')
    # GenScriptFromMd(r'UnitDesign\design.md')
