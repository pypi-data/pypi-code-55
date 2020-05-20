
class Table(object):

    def __init__(self, table_name, spark_session):
        self.table_name = table_name
        self.spark_session = spark_session

    @property
    def table(self):
        return self.spark_session.table(self.table_name)