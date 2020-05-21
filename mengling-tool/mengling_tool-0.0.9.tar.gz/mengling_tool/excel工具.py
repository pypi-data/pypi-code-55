import xlrd
import xlwt
from xlutils3.copy import copy  # 导入copy模块


# 暂未测试
class excelTool:
    def __init__(self, filepath):
        self.filepath = filepath
        self.__xlsread = xlrd.open_workbook(filepath)
        self.__wb = copy(self.__xlsread)

    # 获取指定位置数据
    def getValue(self, row, col, sheets_index=0):
        try:
            xls_sheet = self.__xlsread.sheets()[sheets_index]
            # 读取x行y列数据
            value = xls_sheet.cell(row, col).value
            return value
        except Exception as e:
            print(e)
            return None

    # 获取指定行数据
    def getRowValue(self, row, sheets_index=0):
        try:
            xls_sheet = self.__xlsread.sheets()[sheets_index]
            # 读取第x行数据，返回list保存
            row_value = xls_sheet.row_values(row)
            return row_value
        except Exception as e:
            print(e)
            return []

    # 获取指定列数据
    def getColValue(self, col, sheets_index=0):
        try:
            xls_sheet = self.__xlsread.sheets()[sheets_index]
            # 读取第y列数据，返回list保存
            col_value = xls_sheet.col_values(col)
            return col_value
        except Exception as e:
            print(e)
            return []

    # 获取表的行数及列数
    def getSizes(self, sheets_index=0):
        try:
            xls_sheet = self.__xlsread.sheets()[sheets_index]
            # 读取表中最大行数
            row_size = xls_sheet.nrows
            # 读取表中最大列数
            col_size = xls_sheet.ncols
            return (row_size, col_size)
        except Exception as e:
            print(e)
            return (-1, -1)

    # 新建excel
    def newExcel(self, filepath, p_values_dict, encoding='utf-8'):
        try:
            wb = xlwt.Workbook(encoding=encoding)  # 创建新的Excel
            ws = wb.add_sheet('sheet1')  # 创建新的表单
            for p in p_values_dict.keys():
                ws.write(p[0], p[1], label=p_values_dict[p])
            wb.save(filepath)
        except Exception as e:
            print(e)
            print('新建失败！')

    # 修改excel
    def setValue(self, row, col, newvalue, sheets_index=0):
        try:
            ws = self.__wb.get_sheet(sheets_index)  # 获取表单0
            ws.write(row, col, newvalue)
        except Exception as e:
            print(e)
            print('修改失败！')

    # 保存修改
    def save(self, filepath=None):
        try:
            filepath = self.filepath if filepath == None else filepath
            self.__wb.save(filepath)
            # 重置记录的表信息
            self.__init__(filepath)
        except Exception as e:
            print(e)
            print('保存失败！')
