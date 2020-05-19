from datetime import datetime, timedelta
from typing import List, Tuple

import boto3


class RedshiftCredentialsManager(object):
    def __init__(self, cluster_id: str, user: str, database_name: str,
                 groups: List[str] = None, grace_period=None, session=None,
                 duration: int = 3600):
        self.cluster_id = cluster_id
        self.user = user
        self.database_name = database_name
        self.groups = groups or []
        self.auto_create = True
        self._credential_expiration = datetime.max
        self._grace_period = grace_period or timedelta(seconds=1)
        self._connection_info = None
        self._redshift_client = (session or boto3).client("redshift")
        self.duration = duration

    def connect(self, connect_with_options):
        """
        Passes psycopg2.connect arguments to connect_with_options
        :param connect_with_options: has same signature as psycopg2.connect
        :return: the return type of connect_with_options
        """
        options = self.build_options()
        return connect_with_options(**options)

    def connect_sql_alchemy(self):
        options = self.build_options()
        database = options.pop("dbname")
        username = options.pop("user")
        sslmode = options.pop("sslmode")
        import sqlalchemy as db
        from sqlalchemy.engine.url import URL
        url = URL(drivername="postgresql", database=database,
                  username=username, **options)
        return db.create_engine(url, connect_args={'ssl_mode': sslmode})

    def connect_psycopg2(self):
        import psycopg2
        options = self.build_options()
        return psycopg2.connect(**options)

    def build_options(self):
        """
        Builds options for psycopg2.connect.
        These can be translated to work with other functions.
        :return: connect options
        """
        host, port = self.get_address_port()
        user, password = self.get_user_password()
        return dict(host=host, port=port, user=user, password=password,
                    dbname=self.database_name, sslmode="require")

    def get_address_port(self) -> Tuple[str, int]:
        """
        Gets the address and port of the Redshift cluster via AWS.
        :return:
        """
        if self._connection_info:
            return self._connection_info
        response = self._redshift_client.describe_clusters(
            ClusterIdentifier=self.cluster_id)

        try:
            clusters = response['Clusters']
            cluster = clusters[0]
            endpoint = cluster['Endpoint']
            self._connection_info = (endpoint['Address'], endpoint['Port'])
            return self._connection_info
        except IndexError:
            raise Exception(f"Cluster {self.cluster_id} not found")

    def get_user_password(self) -> Tuple[str, str]:
        """
        Calls the GetClusterCredentials
        :return:
        """
        response = self._redshift_client.get_cluster_credentials(
            ClusterIdentifier=self.cluster_id,
            DbUser=self.user,
            DbName=self.database_name,
            DbGroups=self.groups,
            AutoCreate=self.auto_create,
            DurationSeconds=self.duration
        )

        credentials = (response['DbUser'], response['DbPassword'])
        self._credential_expiration = response['Expiration']
        return credentials
