import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class sqshandler : 
    
    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create SQS client
            self.sqs_client = session.client('sqs', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create SQS client', {'region': self.region})

        self.queues = self.list_queues()
        
    def list_queues(self):
        try:
            response = self.sqs_client.list_queues()

            if 'QueueUrls' in response:
                return response['QueueUrls']
            else:
                return []

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call SQS list_queues', {'region': self.region})
        
        

    def get_queue_attributes(self, queueurl):
        try:
            response = self.sqs_client.get_queue_attributes(QueueUrl=queueurl, AttributeNames=['Policy', 'QueueArn', 'KmsMasterKeyId'])

            return response['Attributes']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call SQS get_queue_attributes', {'region': self.region})

    def sqs_queue_server_side_encryption_not_enabled(self):
        failures = []

        for queue in self.queues:
            try:
                attributes = self.get_queue_attributes(queue)

                if 'KmsMasterKeyId' not in attributes:
                    splitArn = attributes['QueueArn'].split(':')
                    failures = self.helper.append_item_to_list(failures, 'sqs', splitArn[5], attributes['QueueArn'], self.region)

            except Exception as e:
                self.logger.error(f"Error while getting queue attribute for - {queue}: {e}")
            
        return failures

    def sqs_queue_not_encypted_with_kms_cmk(self):
        failures = []

        for queue in self.queues:
            try:
                attributes = self.get_queue_attributes(queue)

                if 'KmsMasterKeyId' in attributes:
                    if attributes['KmsMasterKeyId'] != 'alias/aws/sqs':
                        splitArn = attributes['QueueArn'].split(':')
                        failures = self.helper.append_item_to_list(failures, 'sqs', splitArn[5], attributes['QueueArn'], self.region)

            except Exception as e:
                self.logger.error(f"Error while getting queue attribute for - {queue}: {e}")
            
        return failures

    def sqs_queue_expose_to_eveyone(self):
        failures = []

        for queue in self.queues:
            try:
                attributes = self.get_queue_attributes(queue)

                if 'Policy' in attributes:
                    policy_statement = json.loads(attributes['Policy'])

                    is_exposed = self.helper.is_policy_exposed_to_everyone(policy_statement)
                    if is_exposed:
                        splitArn = attributes['QueueArn'].split(':')
                        failures = self.helper.append_item_to_list(failures, 'sqs', splitArn[5], attributes['QueueArn'], self.region)

            except Exception as e:
                self.logger.error(f"Error while getting queue attribute for - {queue}: {e}")
            
        return failures

    def sqs_queue_cross_account_access_allow(self):
        failures = []

        for queue in self.queues:
            try:
                attributes = self.get_queue_attributes(queue)

                if 'Policy' in attributes:
                    policy_statement = json.loads(attributes['Policy'])

                    is_caa_enabled = self.helper.is_policy_has_cross_account_access(policy_statement)
                    if is_caa_enabled:
                        splitArn = attributes['QueueArn'].split(':')
                        failures = self.helper.append_item_to_list(failures, 'sqs', splitArn[5], attributes['QueueArn'], self.region)

            except Exception as e:
                self.logger.error(f"Error while getting queue attribute for - {queue}: {e}")
            
        return failures
