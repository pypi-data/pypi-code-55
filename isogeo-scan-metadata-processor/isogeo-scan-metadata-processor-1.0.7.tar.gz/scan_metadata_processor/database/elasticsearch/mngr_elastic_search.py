#! python3  # noqa E265

"""
    Manager for Elastic Search.

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import environ
from pathlib import Path

# 3rd party
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, RequestError

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)


# ##############################################################################
# ########## Classes ###############
# ##################################
class ElasticSearchManager(object):
    """Manage operations related to Elastic Search. Mainly a wrapper around ES Python client.\
        See: https://elasticsearch-py.readthedocs.io/en/master/

    :param str host: database host server. Defaults to: "localhost" - optional
    :param int port: database port. Defaults to: 9200 - optional
    :param str user: database user (with write rights). Defaults to: None - optional
    :param str password: user password. Defaults to: None - optional
    :param bool ssl: enable secured connection. Defaults to: True - optional
    :param int pool_size: number of connections to the database. Defaults to: 10 - optional
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 9200,
        user: str = None,
        password: str = None,
        ssl: bool = True,
        pool_size: int = 10,
    ):
        # store parameters as attributes
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ssl = ssl
        self.pool_size = pool_size

    def connect(self) -> bool:
        """Establish connection to Elastic Search using module attributes."""
        # handle SSL options
        if self.ssl:
            self.scheme = "https"
        else:
            self.scheme = "http"

        # handle authentication
        if self.user is not None and self.password is not None:
            http_auth = (self.user, self.password)
        else:
            http_auth = None

        # try to connect
        self.es_client = None
        try:
            self.es_client = Elasticsearch(
                [{"host": self.host, "port": self.port,}],
                scheme=self.scheme,
                use_ssl=self.ssl,
                http_compress=True,
                http_auth=http_auth,
            )
        except ConnectionError as exc:
            logger.error(
                "Connection error. Are your settings ok? Traced error: {}".format(exc)
            )

        # check connection state
        if self.es_client.ping():
            logger.info(
                "Connection to Elastic Search succeeded: {}".format(
                    self.es_client.info()
                )
            )
            return True
        else:
            logger.error("Connection to Elastic Search failed.")
            return False

    def create_index(self, name: str = "isogeo", ignore_if_exists: bool = True):
        """Create the indice into the database using the defined mapping.

        :param str name: indice name. Defaults to: "isogeo" - optional
        :param bool ignore_if_exists: option to ignore existing index with same name. Defaults to: True - optional
        """
        try:
            if ignore_if_exists:
                self.es_client.indices.create(index=name, ignore=400)
            else:
                self.es_client.indices.create(index=name)
        except RequestError as exc:
            if ignore_if_exists and exc.error == "resource_already_exists_exception":
                logger.warning(
                    "Index '{}' already exists. Ignoring the error.".format(name)
                )
            else:
                logger.error(
                    "Index '{}' already exists. Traced error: {}".format(name, exc)
                )
                raise exc

        # store index name
        self.index_name = name

    def insert_document(
        self,
        document_to_index: dict,
        document_type: str = None,
        auto_refresh: str = "true",
    ):
        """Send documents to the Elastic indice.

        :param dict document_to_index: dictionary of document property to insert into database.
        :param str document_type: type of document to insert. Defaults to: None - optional
        :param bool auto_refresh: refresh just after the insertion. Valid choices: true, false, wait_for. Defaults to: "true" - optional
        """
        # insertion
        self.es_client.index(
            index=self.index_name,
            body=document_to_index,
            doc_type=document_type,
            refresh=auto_refresh,
        )


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    # additional imports
    from dotenv import load_dotenv

    # set log level
    logging.basicConfig(level=logging.INFO)
    # load dev environment variables
    if Path(".env").exists():
        load_dotenv(".env", override=True)

    elasticlient = ElasticSearchManager(
        host=environ.get("DATABASE_HOST"),
        port=environ.get("DATABASE_PORT"),
        pool_size=environ.get("DATABASE_POOL_CONNECTIONS"),
        user=environ.get("DATABASE_USER"),
        password=environ.get("DATABASE_PASSWORD"),
        ssl=False,
    )

    # connect
    elasticlient.connect()

    # ensure index is created
    elasticlient.create_index()

    # doc = {
    #     "author": "isogeo iioghjsfgkn",
    #     "abstract": "This is a sample testing metadata in a ES search engine",
    #     "title": "Sample metadata 2",
    #     "timestamp": datetime.now(),
    # }

    # # elasticlient.insert_document(document_to_index= )

    res = elasticlient.es_client.search(
        index=elasticlient.index_name, body={"query": {"match_all": {}}}
    )
    print("Got %d Hits:" % res["hits"]["total"]["value"])
    # for hit in res["hits"]["hits"]:
    #     print("%(timestamp)s %(author)s: %(title)s" % hit["_source"])
