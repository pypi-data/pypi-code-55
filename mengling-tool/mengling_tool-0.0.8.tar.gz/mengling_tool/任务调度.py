import mengling_tool.mysql工具 as sqltools

connect = {
    'dbname': 'task',

}

if __name__ == '__main__':
    sqltool = sqltools.mysqlExecutor(**connect)
    lies, datas = sqltool.select('*', 'task')
    exec()
    pass
