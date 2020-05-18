import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class dynamodbhandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create DynamoDB client
            self.dynamodb_client = session.client('dynamodb', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create DynamoDB client', {'region': self.region})

        self.tables  = self.list_tables()

    def list_tables(self):
        tables = []
        response = {}

        while True:

            try:
                if 'LastEvaluatedTableName' in response:
                    response = self.dynamodb_client.list_tables(ExclusiveStartTableName = response['LastEvaluatedTableName'])
                else:
                    response = self.dynamodb_client.list_tables()

                tables.extend(response['TableNames'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call DynamoDB list_tables', {'region': self.region})

            if 'LastEvaluatedTableName' not in response:
                break

        return tables

    def describe_table(self, table_name):
        try:
            response = self.dynamodb_client.describe_table(TableName=table_name)

            return response['Table']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call DynamoDB describe_table', {'region': self.region})

    def dynamodb_not_encrypted_with_kms_cmk(self):
        failures = []

        for table in self.tables:
            try:
                table_details = self.describe_table(table)  

                if 'SSEDescription' in table_details:
                    key_details = self.helper.get_kms_key_details(table_details['SSEDescription']['KMSMasterKeyArn'])
                    if key_details['KeyManager'] != 'CUSTOMER':
                        failures = self.helper.append_item_to_list(failures, 'dynamodb', table_details['TableName'], table_details['TableArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting DynamoDB details: {e}")

        return failures