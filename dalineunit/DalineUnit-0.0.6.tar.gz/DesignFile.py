"""
@File    :   DesignFile.py
@Software:   PyCharm
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/5/12 9:45  kun.z      1.0         None
"""
import re
import json
import pprint
from DalDecorate import gen_exception_decorate

MD_GRAPH_TEMPLATE = """
```mermaid
    graph TB
$GRAPH_CODE$
```
        """

class DesignFile():
    """
    设计文档类，用来获取设计文档的内容
    """
    def __init__(self,filename = ''):
        self._dic_unit = {}
        if filename:
            self.read_design_file(filename)
    def read_design_file(self, filename):
        """
        读取设计文档
        :param filename:设计文档名称
        :return:设计文档各单元
        """
        self._file_name = filename
        with open(filename,encoding='utf8') as f:
            unit_name = ''
            second_title_name = ''
            # 只有function_list有三四级标题
            third_title_name = ''
            fourth_title_name = ''
            out_json_str = ''
            for line in f:
                if re.match('>',line.strip()) or re.match('//',line.strip()) or re.match('---',line.strip()) :
                    # md 的注释文档、分割线  跳过
                    continue
                if not line.strip():
                    # 空行跳过
                    continue
                if re.match('# ',line):
                    unit_name = line.strip('# ').strip()
                    self._dic_unit[unit_name] = {}
                    self._dic_unit[unit_name]['unit_info'] = {}
                    self._dic_unit[unit_name]['unit_info']['unitname'] = unit_name
                    second_title_name = ''
                    third_title_name = ''
                    fourth_title_name = ''
                    continue
                # --------二级标题切换-----------
                elif re.match('## ',line):
                    second_title_name = line.strip('## ').strip()
                    if 'unit_info' not in line: # 上面已经定义了unit_info,并赋值了，其余的都可以初始化
                        self._dic_unit[unit_name][second_title_name] = {}
                        third_title_name = ''
                        fourth_title_name = ''
                        continue
                # --------三级标题切换-----------
                elif re.match('### ',line):
                    third_title_name = line.strip('### ').strip().strip('()')
                    self._dic_unit[unit_name][second_title_name][third_title_name] = {}
                    fourth_title_name = ''
                    continue
                # --------四级标题切换-----------
                # 只有function_list有四级标题
                elif re.match('#### ',line):
                    fourth_title_name = line.strip('#### ').strip()
                    self._dic_unit[unit_name][second_title_name][third_title_name][fourth_title_name] = {}
                    out_json_str = ''
                    continue

                elif '+' in line:
                    line_tmp = line.strip('+').strip(' ').split("#")[0].split('=')
                    if len(line_tmp) == 1:
                        line_tmp.append('')
                    if third_title_name :
                        if fourth_title_name :
                            self._dic_unit[unit_name][second_title_name][third_title_name][fourth_title_name][
                                line_tmp[0].strip()] = line_tmp[1].strip()
                        else:
                            self._dic_unit[unit_name][second_title_name][third_title_name][line_tmp[0].strip()] = \
                            line_tmp[1].strip()
                    else:
                        self._dic_unit[unit_name][second_title_name][line_tmp[0].strip()] = line_tmp[1].strip()
                    continue

                # --------内容读取，output,function_list-----------
                # output的数据开头没有标志，仅仅用四级标题确定
                elif 'output' in fourth_title_name :
                    out_json_str = out_json_str + line.split('#')[0]
                    try:
                        self._dic_unit[unit_name][second_title_name][third_title_name][fourth_title_name] = json.loads(out_json_str)
                    except Exception as e:
                        pass
                    continue
            # print(out_json_str)
        return self._dic_unit
    def get_all_design_unit(self):
        """
        获取所有设计的单元
        :return:所有设计单元
        """
        return self._dic_unit

    @gen_exception_decorate
    def gen_design_md(self):
        """
        重新生成设计文档的md文档，包括mermaid的图
        :return:
        """
        f_old = open(self._file_name,'r',encoding='utf8')
        old_context = f_old.readlines()
        file_name_gen = '%s.%s'%(self._file_name.split('.')[0]+'_gen',self._file_name.split('.')[1])
        f_gen = open(file_name_gen,'w',encoding='utf8')

        script_graph = ''
        for each_unit in self._dic_unit:
            if 'upper_unit' not in self._dic_unit[each_unit]:
                continue
            for each_data in self._dic_unit[each_unit]['upper_unit']:
                script_graph = script_graph + '\t\t%s[%s]-->%s[%s]\n'%(each_data,each_data,self._dic_unit[each_unit]['unit_info']['unitname'],self._dic_unit[each_unit]['unit_info']['unitname'])
        script_graph = MD_GRAPH_TEMPLATE.replace('$GRAPH_CODE$', script_graph)
        f_gen.writelines(old_context)
        f_gen.write('----\n')
        f_gen.write('# 拓扑图如下')
        f_gen.write(script_graph)

        f_gen.close()
        f_old.close()
    def gen_design_PDF(self):
        """
        生成设计文档的PDF
        :return:
        """
        return '暂不支持'

def mytest():
    tmp = DesignFile()
    pprint.pprint('read_design_file:'+str(tmp.read_design_file(r'UnitDesign\design.md')))
    pprint.pprint("get_all_design_unit:"+str(tmp.get_all_design_unit()))

    tmp2 = DesignFile(r'UnitDesign\design.md')
    pprint.pprint("init函数读文件get_all_design_unit:"+str(tmp2.get_all_design_unit()))
    tmp2.gen_design_md()
if __name__=='__main__':
    mytest()