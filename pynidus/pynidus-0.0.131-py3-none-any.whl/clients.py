import json
import pickle
import elasticsearch
import psycopg2
from google.cloud.storage import Client

class ElasticsearchClient:
    
    def __init__(self, config):
        self.host = config.get('HOST')
        self.user = config.get('USER')
        self.password = config.get('PASSWORD')
        self._es = self._connect()
    
    def _connect(self):
        return elasticsearch.Elasticsearch(
            hosts=[self.host],
            http_auth=(self.user, self.password),
            send_get_body_as='POST'
        )
    
    def query(self, index, body):
        return self._es.search(index=index, body=body)
         
class DatabaseClient:

    def __init__(self, config):
        self.host = config.get('HOST', 'localhost')
        self.database = config.get('DATABASE')
        self.user = config.get('USER')
        self.password = config.get('PASSWORD')
        self.port = config.get('PORT', 5432)
    
    def _connect(self):
        return psycopg2.connect(**self.__dict__)

    def query(self, query_):

        conn = None

        try:            
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(query_)
            return cursor.fetchall()
        
        except:
            raise
            
        finally:            
            if conn:
                cursor.close()
                conn.close()
    
class GCSClient:
    
    def __init__(self, config):
        self.bucket = config.get('BUCKET')
        self._client = self._connect()
        
    def _connect(self):
        return Client()
    
    def download(self, blob):
        return self._client.get_bucket(self.bucket).get_blob(blob)

    def upload(self, blob, obj):
        try:
            self._client.get_bucket(self.bucket).blob(blob).upload_from_string(
                data=json.dumps(obj),
                content_type='application/json'
            )
        except TypeError:
            self._client.get_bucket(self.bucket).blob(blob).upload_from_string(
                data=pickle.dumps(obj),
                content_type='application/octet-stream'
            )
        except Exception as e:
            raise e