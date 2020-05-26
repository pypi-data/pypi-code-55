import copy
import boto3

from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
from botocore import exceptions


class IndexNotValidException(Exception):
    pass


class ConditionalCheckFailedException(Exception):
    pass


class DynamoDBDataStore(object):
    serializer = TypeSerializer()
    deserializer = TypeDeserializer()

    def __init__(self, table_name):

        DB_SETTINGS = {
            'TableName': table_name,
            'HashKeyName': 'PK',
            'SortKeyName': 'SK'
        }

        self.table_name = DB_SETTINGS['TableName']
        self.hash_key_name = DB_SETTINGS['HashKeyName']
        self.sort_key_name = DB_SETTINGS.get('SortKeyName', None)
        self.index_keys = [
            self.hash_key_name,
            self.sort_key_name,
            'GSI1PK',
            'GSI1SK',
            'GSI2PK',
            'GSI2SK',
        ]
        self.client = boto3.client('dynamodb')

    def save_document(self, document, index=None, parameters={}):
        document = copy.deepcopy(document)

        if len(index) not in [1, 2]:
            raise IndexNotValidException

        if len(index) == 1:
            self._save_document_using_hash_key(document, hash_key=index[0], parameters=parameters)
        else:
            self._save_document_using_composite_key(document, hash_key=index[0], sort_key=index[1],
                                                    parameters=parameters)

    def _save_document_using_composite_key(self, document, hash_key, sort_key, parameters={}):
        document[self.hash_key_name] = hash_key
        document[self.sort_key_name] = sort_key

        document = self.serialize(document)
        self._put_item(document, parameters=parameters)

    def _save_document_using_hash_key(self, document, hash_key, parameters={}):
        document[self.hash_key_name] = hash_key

        document = self.serialize(document)

        self._put_item(document, parameters=parameters)

    def _put_item(self, item, parameters={}):

        params = {
            'TableName': self.table_name,
            'Item': item,
            **parameters
        }

        try:
            self.client.put_item(**params)
        except exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise e
            raise ConditionalCheckFailedException

    def get_document(self, index=None, return_index=False, consistent_read=False):
        if len(index) not in [1, 2]:
            raise IndexNotValidException

        key = {
            self.hash_key_name: {'S': index[0]}
        }

        if len(index) == 2:
            key[self.sort_key_name] = {'S': index[1]}

        item = self.client.get_item(
            TableName=self.table_name,
            Key=key,
            ConsistentRead=consistent_read
        ).get('Item', None)

        if not item:
            return None

        deserialized_item = self.deserialize(item)

        if not return_index:
            deserialized_item.pop(self.hash_key_name, None)
            deserialized_item.pop(self.sort_key_name, None)

        return deserialized_item

    def serialize(self, document):
        return DynamoDBDataStore.serializer.serialize(document)['M']

    def deserialize(self, document):
        return DynamoDBDataStore.deserializer.deserialize({'M': document})

    def paginate(self, parameters):
        parameters['TableName'] = self.table_name

        paginator = self.client.get_paginator('query')
        return paginator.paginate(**parameters)

    def update_document(self, index=None, parameters={}):

        if len(index) not in [1, 2]:
            raise IndexNotValidException

        key = {
            self.hash_key_name: {'S': index[0]}
        }

        if len(index) == 2:
            key[self.sort_key_name] = {'S': index[1]}

        params = {
            'TableName': self.table_name,
            'Key': key,
            **parameters
        }

        try:
            self.client.update_item(**params)
        except exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise e
            raise ConditionalCheckFailedException

    def delete_document(self, index=None, parameters={}):
        if len(index) not in [1, 2]:
            raise IndexNotValidException

        key = {
            self.hash_key_name: {'S': index[0]}
        }

        if len(index) == 2:
            key[self.sort_key_name] = {'S': index[1]}

        params = {
            'TableName': self.table_name,
            'Key': key,
            **parameters
        }

        try:
            self.client.delete_item(**params)
        except exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise e
            raise ConditionalCheckFailedException

    def batch_request(self, request_items):
        self.client.batch_write_item(RequestItems={
            self.table_name: request_items
        })

    def get_documents(self, query, return_index=False):
        pages = self.paginate(query)
        documents = []

        for page in pages:
            items = page['Items']

            for item in items:
                document = self.deserialize(item)
                if not return_index:
                    for key in self.index_keys:
                        document.pop(key, None)

                documents.append(document)

        return documents
