# sybase/pyodbc.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""
.. dialect:: sybase+pyodbc
    :name: PyODBC
    :dbapi: pyodbc
    :connectstring: sybase+pyodbc://<username>:<password>@<dsnname>[/<database>]
    :url: http://pypi.python.org/pypi/pyodbc/

Unicode Support
---------------

The pyodbc driver currently supports usage of these Sybase types with
Unicode or multibyte strings::

    CHAR
    NCHAR
    NVARCHAR
    TEXT
    VARCHAR

Currently *not* supported are::

    UNICHAR
    UNITEXT
    UNIVARCHAR

"""  # noqa

import decimal

from sqlalchemy import processors
from sqlalchemy import types as sqltypes
from sqlalchemy.connectors.pyodbc import PyODBCConnector
from .base import SybaseDialect
from .base import SybaseExecutionContext


class _SybNumeric_pyodbc(sqltypes.Numeric):
    """Turns Decimals with adjusted() < -6 into floats.

    It's not yet known how to get decimals with many
    significant digits or very large adjusted() into Sybase
    via pyodbc.

    """

    def bind_processor(self, dialect):
        super_process = super(_SybNumeric_pyodbc, self).bind_processor(dialect)

        def process(value):
            if self.asdecimal and isinstance(value, decimal.Decimal):

                if value.adjusted() < -6:
                    return processors.to_float(value)

            if super_process:
                return super_process(value)
            else:
                return value

        return process


class SybaseExecutionContext_pyodbc(SybaseExecutionContext):
    def set_ddl_autocommit(self, connection, value):
        if value:
            connection.autocommit = True
        else:
            connection.autocommit = False


class SybaseDialect_pyodbc(PyODBCConnector, SybaseDialect):
    execution_ctx_cls = SybaseExecutionContext_pyodbc

    # TODO: remove once https://github.com/sqlalchemy/sqlalchemy/issues/5321
    #       is resolved and released
    supports_sane_rowcount_returning = True

    colspecs = {sqltypes.Numeric: _SybNumeric_pyodbc}

    @classmethod
    def dbapi(cls):
        return PyODBCConnector.dbapi()

    def on_connect(self):
        super_ = super(SybaseDialect_pyodbc, self).on_connect()

        def on_connect(conn):
            if super_ is not None:
                super_(conn)

        return on_connect


dialect = SybaseDialect_pyodbc
