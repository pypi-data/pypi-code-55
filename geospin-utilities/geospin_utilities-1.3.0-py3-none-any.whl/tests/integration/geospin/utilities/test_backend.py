import pytest


@pytest.fixture
def my_db(postgresql_db):
    with postgresql_db.engine.connect() as conn:
        sql = f"""
        CREATE TABLE my_table (
            hex_id varchar(80) PRIMARY KEY,
            feature_1 float,
            feature_2 float
        );
        INSERT INTO my_table VALUES ('b', 1., 0.);
        INSERT INTO my_table VALUES ('c', 3., 2.);
        """
        conn.execute(sql)

    return postgresql_db


def test_get_column_names(db_backend, my_db):
    expected = ['hex_id', 'feature_1', 'feature_2']
    table = 'my_table'
    result = db_backend.get_column_names_in_table(table=table)
    assert expected == result
