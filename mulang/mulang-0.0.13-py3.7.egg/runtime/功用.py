import re

def 反馈信息(例外):
    提神符 = "(..•˘_˘•..)"
    类型 = 例外.__class__.__name__
    exc_type, exc_value, 回溯信息 = sys.exc_info()
    各层 = traceback.extract_tb(回溯信息)
    最上层 = 各层[-1]
    行信息 = '第' + str(最上层.lineno) + '行'
    行内容 = 层.line
    原信息 = str(例外)
    return 提神符 + 行信息 + 提示(类型, 原信息) + 行内容

def 提示(类型, 原信息)
    if 类型 == 'NameError':
        return re.sub(r"name '(.*)' is not defined", r"请先定义'\1'再使用", 原信息)
    elif 类型 == 'ZeroDivisionError':
        return "请勿除以零"
    elif 类型 == 'RecursionError':
        return "递归过深。请确认: 1、的确需要递归 2、递归的收敛正确"
    return 原信息


        #sys.stderr.write(repr(各层))
        错误信息 = 
        for 层 in 各层:
            文件名 = 层.filename
            if 文件名 == 源码文件:
                错误信息 += '第' + str(层.lineno) + '行'
                错误信息 += "请勿除零: "
                错误信息 += 层.line
        sys.stderr.write(错误信息 + '\n')