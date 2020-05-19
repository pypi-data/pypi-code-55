import mock
import pytest


@pytest.fixture
def db_backend(postgresql_db):
    from geospin.utilities.backend import DatabaseBackend

    with mock.patch('geospin.utilities.backend.create_engine') as mock_engine, \
            mock.patch(
                'geospin.utilities.backend.sessionmaker') as mock_factory, \
            mock.patch(
                'geospin.utilities.backend.scoped_session') as mock_session:
        mock_factory.return_value = '<FACTORY>'
        mock_session.return_value = '<SESSION>'
        mock_engine.return_value = postgresql_db.engine

        db = DatabaseBackend(
            user='user', password='pw', host='my.db.host', port=5432,
            database='database')

        db.conn_url = postgresql_db.engine.url
    return db
