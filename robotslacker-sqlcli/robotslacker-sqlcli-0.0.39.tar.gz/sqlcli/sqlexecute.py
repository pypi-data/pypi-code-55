# -*- coding: utf-8 -*-
from .sqlparse import SQLAnalyze
from .sqlparse import SQLFormatWithPrefix
from .commandanalyze import execute
from .commandanalyze import CommandNotFound
from .sqlcliexception import SQLCliException
import click
import time


class SQLExecute(object):
    conn = None                         # 数据库连接
    options = None                      # 用户设置的各种选项
    logfile = None                      # 打印的日志文件
    sqlscript = None                    # 需要执行的SQL脚本
    SQLMappingHandler = None            # SQL重写处理
    m_Current_RunningSQL = None         # 目前程序运行的当前SQL
    m_Current_RunningStarted = None     # 目前程序运行的当前SQL开始时间
    NoConsole = False                   # 屏幕输出Console，如果为True, 不再输出屏幕信息

    def __init__(self):
        # 设置一些默认的参数
        self.options = {"WHENEVER_SQLERROR": "CONTINUE", "PAGE": "OFF", "OUTPUT_FORMAT": "ASCII", "ECHO": "ON",
                        "LONG": 20, 'KAFKA_SERVERS': None, 'TIMING': 'OFF', 'TERMOUT': 'ON', 'FEEDBACK': 'ON',
                        "ARRAYSIZE": 10000, 'SQLREWRITE': 'ON', "DEBUG": 'OFF'}

    def set_logfile(self, p_logfile):
        self.logfile = p_logfile

    def set_connection(self, p_conn):
        self.conn = p_conn

    def run(self, statement):
        """Execute the sql in the database and return the results. The results
        are a list of tuples. Each tuple has 4 values
        (title, rows, headers, status).
        """

        # Remove spaces and EOL
        statement = statement.strip()
        if not statement:  # Empty string
            yield None, None, None, None

        # 分析SQL语句
        (ret_bSQLCompleted, ret_SQLSplitResults, ret_SQLSplitResultsWithComments) = SQLAnalyze(statement)
        for m_nPos in range(0, len(ret_SQLSplitResults)):

            sql = ret_SQLSplitResults[m_nPos]
            m_CommentSQL = ret_SQLSplitResultsWithComments[m_nPos]

            # 如果打开了回显，并且指定了输出文件，则在输出文件里显示SQL语句
            if self.options["ECHO"] == 'ON' and len(m_CommentSQL.strip()) != 0 and self.logfile is not None:
                click.echo(SQLFormatWithPrefix(m_CommentSQL), file=self.logfile)

            # 如果运行在脚本模式下，需要在控制台回显SQL
            if self.sqlscript is not None:
                if not self.NoConsole:
                    click.secho(SQLFormatWithPrefix(m_CommentSQL))

            # 如果打开了回显，并且指定了输出文件，且SQL被改写过，输出改写后的SQL
            if self.options["SQLREWRITE"] == 'ON':
                old_sql = sql
                sql = self.SQLMappingHandler.RewriteSQL(self.sqlscript, old_sql)
                if old_sql != sql:
                    if self.options["ECHO"] == 'ON' and self.logfile is not None:
                        # SQL已经发生了改变
                        click.echo(SQLFormatWithPrefix(
                            "Your SQL has been changed to:\n" + sql, 'REWROTED '), file=self.logfile)
                    if self.sqlscript is not None:
                        if not self.NoConsole:
                            click.secho(SQLFormatWithPrefix(
                                "Your SQL has been changed to:\n" + sql, 'REWROTED '))

            # 如果是空语句，不在执行
            if len(sql.strip()) == 0:
                continue

            # 打开游标
            cur = self.conn.cursor() if self.conn else None

            # 记录命令开始时间
            start = time.time()
            self.m_Current_RunningSQL = sql
            self.m_Current_RunningStarted = start

            # 执行SQL
            try:
                # 首先假设这是一个特殊命令
                for result in execute(cur, sql):
                    yield result
            except CommandNotFound:
                if cur is None:
                    # 进入到SQL执行阶段，但是没有conn，也不是特殊命令
                    if self.options["WHENEVER_SQLERROR"] == "EXIT":
                        raise SQLCliException("Not Connected. ")
                    else:
                        yield None, None, None, "Not connected. "

                # 执行正常的SQL语句
                if cur is not None:
                    try:
                        cur.execute(sql)
                        rowcount = 0
                        while True:
                            (title, result, headers, status, m_FetchStatus, m_FetchedRows) = \
                                self.get_result(cur, rowcount)
                            rowcount = m_FetchedRows
                            yield title, result, headers, status
                            if not m_FetchStatus:
                                break
                    except Exception as e:
                        if (
                                str(e).find("SQLSyntaxErrorException") != -1 or
                                str(e).find("SQLException") != -1
                        ):
                            # SQL 语法错误
                            if self.options["WHENEVER_SQLERROR"] == "EXIT":
                                raise SQLCliException(str(e))
                            else:
                                yield None, None, None, str(e)
                        else:
                            # 其他不明错误
                            raise e
            except SQLCliException as e:
                if self.options["WHENEVER_SQLERROR"] == "EXIT":
                    raise e
                else:
                    yield None, None, None, str(e.message)

            # 记录结束时间
            end = time.time()
            self.m_Current_RunningSQL = None
            self.m_Current_RunningStarted = None

            # 如果需要，打印语句执行时间
            if self.options['TIMING'] == 'ON':
                if sql.strip().upper() not in ('EXIT', 'QUIT'):
                    yield None, None, None, 'Running time elapsed: %8.2f Seconds' % (end - start)

    def get_Current_RunningSQL(self):
        return self.m_Current_RunningSQL

    def get_Current_RunningStarted(self):
        return self.m_Current_RunningStarted

    def get_result(self, cursor, rowcount):
        """Get the current result's data from the cursor."""
        title = headers = None
        m_FetchStatus = True

        # cursor.description is not None for queries that return result sets,
        # e.g. SELECT.
        result = []
        if cursor.description is not None:
            headers = [x[0] for x in cursor.description]
            status = "{0} row{1} selected."
            m_arraysize = int(self.options["ARRAYSIZE"])
            rowset = list(cursor.fetchmany(m_arraysize))
            if self.options['TERMOUT'] != 'OFF':
                for row in rowset:
                    m_row = []
                    for column in row:
                        if str(type(column)).find('JDBCClobClient') != -1:
                            m_row.append(column.getSubString(1, int(self.options["LONG"])))
                        else:
                            m_row.append(column)
                    m_row = tuple(m_row)
                    result.append(m_row)
            rowcount = rowcount + len(rowset)
            if len(rowset) < m_arraysize:
                # 已经没有什么可以取的了, 游标结束
                m_FetchStatus = False

        else:
            status = "{0} row{1} affected"
            rowcount = 0 if cursor.rowcount == -1 else cursor.rowcount
            result = None
            m_FetchStatus = False

        # 只要不是最后一次打印，不再返回status内容
        if m_FetchStatus:
            status = None

        if self.options['FEEDBACK'] == 'ON' and status is not None:
            status = status.format(rowcount, "" if rowcount == 1 else "s")
        else:
            status = None
        if self.options['TERMOUT'] == 'OFF':
            return title, [], headers, status, m_FetchStatus, rowcount
        else:
            return title, result, headers, status, m_FetchStatus, rowcount
