import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error


class firehosehandler : 
    
    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create firehose client
            self.firehose_client = session.client('firehose', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Firehose client', {'region': self.region})

        self.delivery_streams = self.list_delivery_streams()

    def list_delivery_streams(self):
        delivery_streams = []
        response = {}

        while True:

            try:
                if 'HasMoreDeliveryStreams' in response and response.get('HasMoreDeliveryStreams'):
                    response = self.firehose_client.list_delivery_streams(ExclusiveStartDeliveryStreamName=response['DeliveryStreamNames'][len(response['DeliveryStreamNames']) - 1])
                else:
                    response = self.firehose_client.list_delivery_streams()
                
                delivery_streams.extend(response['DeliveryStreamNames'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Firehose list_delivery_streams', {'region': self.region})

            if not response['HasMoreDeliveryStreams']:
                break

        return delivery_streams

    def describe_delivery_stream(self, delivery_stream):
        try:
            response = self.firehose_client.describe_delivery_stream(DeliveryStreamName=delivery_stream)

            return response['DeliveryStreamDescription']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call Firehose describe_delivery_stream', {'region': self.region})

    def firehose_delivery_stream_source_records_not_encrypted(self):

        failures = []

        for delivery_stream in self.delivery_streams:
            try:
                delivery_stream_detail = self.describe_delivery_stream(delivery_stream)

                if delivery_stream_detail['DeliveryStreamEncryptionConfiguration']['Status'] == 'DISABLED':
                    failures = self.helper.append_item_to_list(failures, 'firehose', delivery_stream, delivery_stream_detail['DeliveryStreamARN'] , self.region)
            
            except Exception as e:
                self.logger.error(f"Error while getting firehose delivery stream details : {e}")

        return failures

    def firehose_delivery_stream_s3_destination_not_encrypted(self):
        failures = []

        for delivery_stream in self.delivery_streams:
            try:
                delivery_stream_detail = self.describe_delivery_stream(delivery_stream)
                for destination in delivery_stream_detail['Destinations']:                    
                    if 'ExtendedS3DestinationDescription' in destination:
                        if 'NoEncryptionConfig' in destination['ExtendedS3DestinationDescription']['EncryptionConfiguration']:
                            failures = self.helper.append_item_to_list(failures, 'firehose', delivery_stream, delivery_stream_detail['DeliveryStreamARN'] , self.region)
            
            except Exception as e:
                self.logger.error(f"Error while getting firehose delivery stream details : {e}")

        return failures
