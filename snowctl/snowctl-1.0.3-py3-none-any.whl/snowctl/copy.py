import sys
from snowctl.utils import *
from snowctl.snowctl import Controller

class Copycat(Controller):
    """
    Subclass of Controller to handle view copying
    """
    def __init__(self, conn, safe):
        super().__init__(conn, safe)

    def prompt_input(self, msg):
        print(msg, end='', flush=True)
        return sys.stdin.readline().replace('\n', '').strip().split(',')

    def get_views(self):
        views = []
        rows = self.execute_query('show views')
        for i, row in enumerate(rows):
            views.append(row[1])
            print(f'{i} - {row[1]}')
        return views

    def select_views(self):
        views = self.get_views()
        user_input = self.prompt_input('choose view(s) to copy ([int, int, ...]|all): ')
        copy_these = []
        if user_input[0] == 'all':
            copy_these = views
        else:
            for index in user_input:
                copy_these.append(views[int(index)])
        print(f'chose view(s) {", ".join(copy_these)}')
        return copy_these

    def get_ddls(self, views):
        ddls = []
        for view in views:
            ddl = self.execute_query(f"select GET_DDL('view', '{view}')")[0][0]
            ddls.append(ddl)
        return ddls

    def get_schemas(self):
        schemas = []
        rows = self.execute_query('show schemas')
        rows.pop(0)  # Ignore information schema
        for i, row in enumerate(rows):
            schemas.append(row[1])
            print(f'{i} - {row[1]}')
        return schemas

    def select_schemas(self):
        schemas = self.get_schemas()
        user_input = self.prompt_input('copy into ([int, int, ...]|all): ')
        copy_into = []
        if user_input[0] == 'all':
            copy_into = schemas
        else:
            for index in user_input:
                copy_into.append(schemas[int(index)])
        print(f'chose schema(s) {", ".join(copy_into)}')
        return copy_into

    def copy_views(self, db, filter_cols=False):
        clear_screen()
        copy_these = self.select_views()
        ddls = self.get_ddls(copy_these)
        copy_into = self.select_schemas()
        if filter_cols:
            clear_screen()    
        for i, view in enumerate(copy_these):
            for schema in copy_into:
                query = format_ddl(ddls[i], view, schema, db)
                if filter_cols:
                    query = filter_ddl(query, view, db, schema)
                if self.safe_mode:
                    if not self.ask_confirmation(query):
                        continue
                self.cursor.execute(query)
                response = self.cursor.fetchone()
                print(f'{response[0]} (target: {db}.{schema})')
