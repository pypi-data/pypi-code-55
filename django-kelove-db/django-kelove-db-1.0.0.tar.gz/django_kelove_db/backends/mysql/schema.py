from abc import ABC

from django.db.backends.mysql.schema import DatabaseSchemaEditor as MySqlDatabaseSchemaEditor


class DatabaseSchemaEditor(MySqlDatabaseSchemaEditor, ABC):

    def column_sql(self, model, field, include_default=False):
        sql, params = super().column_sql(model, field, include_default)
        if field.help_text:
            sql += " COMMENT '%s'" % field.help_text
        elif field.verbose_name:
            sql += " COMMENT '%s'" % field.verbose_name
        return sql, params

    def table_sql(self, model):
        sql, params = super().table_sql(model)
        if model._meta.verbose_name:
            sql += " COMMENT '%s'" % model._meta.verbose_name
        return sql, params
