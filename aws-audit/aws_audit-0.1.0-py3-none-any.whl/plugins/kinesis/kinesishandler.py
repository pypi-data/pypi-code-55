import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class kinesishandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create Kinesis client
            self.kinesis_client = session.client('kinesis', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Kinesis client', {'region': self.region})

        self.streams = self.list_streams()

    def list_streams(self):
        streams = []
        response = {}

        while True:

            try:
                if 'HasMoreStreams' in response and response.get('HasMoreStreams'):
                    response = self.kinesis_client.list_streams(ExclusiveStartStreamName=response['StreamNames'][len(response['StreamNames']) - 1])
                else:
                    response = self.kinesis_client.list_streams()
                
                streams.extend(response['StreamNames'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Kinesis list_streams', {'region': self.region})

            if not response['HasMoreStreams']:
                break

        return streams

    def describe_stream(self, stream_name):
        try:
            response = self.kinesis_client.describe_stream(StreamName=stream_name)

            return response['StreamDescription']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call Kinesis describe_stream', {'region': self.region})

    def kinesis_server_side_encryption_not_enabled(self):

        failures = []

        for stream in self.streams:
            try:
                stream_detail = self.describe_stream(stream)

                if stream_detail['EncryptionType'] == 'NONE':
                    failures = self.helper.append_item_to_list(failures, 'kinesis', stream_detail['StreamName'], stream_detail['StreamARN'] , self.region)
            
            except Exception as e:
                self.logger.error(f"Error while getting Kinesis stream details : {e}")

        return failures

    def kinesis_stream_not_encrypted_with_cmk(self):

        failures = []

        for stream in self.streams:
            try:
                stream_detail = self.describe_stream(stream)

                if stream_detail['EncryptionType'] == 'AWS':
                    if stream_detail['KeyId'] != 'alias/aws/kinesis':
                        failures = self.helper.append_item_to_list(failures, 'kinesis', stream_detail['StreamName'], stream_detail['StreamARN'] , self.region)
            
            except Exception as e:
                self.logger.error(f"Error while getting Kinesis stream details : {e}")

        return failures