def connect_sql_alchemy(**options):
    database = options.pop("dbname")
    username = options.pop("user")
    sslmode = options.pop("sslmode")
    import sqlalchemy as db
    from sqlalchemy.engine.url import URL
    url = URL(drivername="postgresql", database=database,
              username=username, **options)
    return db.create_engine(url, connect_args={'ssl_mode': sslmode})
