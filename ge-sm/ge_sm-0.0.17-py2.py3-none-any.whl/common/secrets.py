import os

# redshift cluster
rs_pwd = os.environ.setdefault('REDSHIFT_PWD', '****')
rs_dsn = os.environ.setdefault('REDSHIFT_DSN', '****')
rs_usr = os.environ.setdefault('REDSHIFT_USR', 'dataplatform')
