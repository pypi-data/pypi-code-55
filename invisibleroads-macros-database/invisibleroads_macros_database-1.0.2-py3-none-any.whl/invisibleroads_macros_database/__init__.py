from abc import ABC, abstractmethod
from sqlalchemy.event import listen
from sqlalchemy.sql import func, select


class DatabaseExtension(ABC):

    def __init__(self, settings, prefix='sqlalchemy.'):
        self.settings = settings
        self.prefix = prefix

    @abstractmethod
    def configure(self, engine):
        pass


class SpatialiteExtension(DatabaseExtension):

    def configure(self, engine):
        sqlalchemy_url = self.settings[self.prefix + 'url']
        if not sqlalchemy_url.startswith('sqlite'):
            return
        load_spatialite_sqlite_extension(engine)


def load_spatialite_sqlite_extension(engine):

    def load_spatialite(api_connection, connection_record):
        api_connection.enable_load_extension(True)
        api_connection.load_extension('mod_spatialite.so')

    listen(engine, 'connect', load_spatialite)
    # https://github.com/Toblerity/Shapely/issues/904
    from shapely import speedups  # noqa
    engine_connection = engine.connect()
    engine_connection.execute(select([func.InitSpatialMetaData()]))
    engine_connection.close()
