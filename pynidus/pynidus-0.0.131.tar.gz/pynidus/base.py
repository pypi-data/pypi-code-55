import os
from pynidus.clients import ElasticsearchClient, DatabaseClient, GCSClient
from pynidus.errors import ErrorLogger
from pynidus.ab import ABTest

class MLTBase:
    
    def __init__(self, **kwargs):
        
        es_config = kwargs.get('es_config')
        pg_config = kwargs.get('pg_config')
        gcs_config = kwargs.get('gcs_config')
        bugsnag_config = kwargs.get('bugsnag_config')
        ab_config = kwargs.get('ab_config')

        if es_config:
            self.es_client = ElasticsearchClient(es_config)

        if pg_config:
            self.pg_client = DatabaseClient(pg_config)

        if gcs_config:
            self.gcs_client = GCSClient(gcs_config)

        if bugsnag_config:
            self.error_logger = ErrorLogger(bugsnag_config)

        if ab_config:
            self.ab = ABTest(config=ab_config)

        


