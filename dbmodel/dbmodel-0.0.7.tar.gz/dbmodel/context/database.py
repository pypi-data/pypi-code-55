# -*- coding: utf-8 -*-
import mysql.connector as mariadb


class DataBase():

    # Init
    def __init__(self, db_user=None, db_password=None, db_host=None, db_port=None, db_database=None, db_ssl=False, db_ssl_ca=None, db_ssl_cert=None, db_ssl_key=None):
        try:
            self._deletelist = []
            if not db_ssl:
                self._conn = mariadb.connect(
                    user=db_user, password=db_password, host=db_host, port=db_port, database=db_database)
            else:
                self._conn = mariadb.connect(user=db_user, password=db_password, host=db_host, port=db_port,
                                             database=db_database, ssl_ca=db_ssl_ca, ssl_cert=db_ssl_cert, ssl_key=db_ssl_key)
        # ERRO CONEXÃO COM BANCO DE DADOS
        except mariadb.Error as e:
            raise e
        # ERRO GENÉRICO
        except Exception as e:
            raise e

    # INICIA CURSOR
    @property
    def cursor(self):
        try:
            return self._conn.cursor(dictionary=True)
        except mariadb.Error as e:
            raise e
        except Exception as e:
            raise e

    # FECHA CONEXÃO
    def close(self):
        try:
            self._conn.close()
        # ERRO EM FECHAMENTO CONEXÃO COM BANCO DE DADOS
        except mariadb.Error as e:
            raise e
        # ERRO GENÉRICO EM FECHAMENTO CONEXÃO COM BANCO DE DADOS
        except Exception as e:
            raise e

    # EXECUÇÃO SELECT SQL
    def fetchall(self, sql_query):
        cursor = self.cursor
        try:
            cursor.execute(sql_query)
            registros = cursor.fetchall()
            return registros
        except mariadb.Error as e:
            raise e
        except Exception as e:
            raise e
        finally:
            cursor.close()

    # EXECUÇÃO SELECT SQL
    def save(self, sql_statement, data):
        cursor = self.cursor
        try:
            cursor.execute(sql_statement, data)
            return cursor.lastrowid if cursor.lastrowid > 0 else None
        except mariadb.Error as e:
            raise e
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def commit(self):
        try:
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
