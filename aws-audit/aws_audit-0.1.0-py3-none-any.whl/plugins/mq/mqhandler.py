import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class mqhandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create MQ client
            self.mq_client = session.client('mq', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create MQ client', {'region': self.region})

        self.brokers = self.list_brokers()

    def list_brokers(self):
        brokers = []
        response = {}
        while True:
            try:
                if 'NextToken' in response:
                    response = self.mq_client.list_brokers(NextToken = response['NextToken'])
                else:
                    response = self.mq_client.list_brokers()

                brokers.extend(response['BrokerSummaries'])
                
            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call MQ list_brokers', {'region': self.region})

            if 'NextToken' not in response:
                break
        
        return brokers

    def describe_broker(self, broker_id):
        response = {}

        try:            
            response = self.mq_client.describe_broker(BrokerId=broker_id)
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call MQ describe_broker', {'region': self.region})
        
        return response

    def mq_log_export_not_enabled(self):

        failures = []
        
        for broker in self.brokers:

            try:

                audit_log_enabled = False
                general_log_enabled = False

                response = self.describe_broker(broker['BrokerId'])            

                if response['Logs']['Audit']:
                    audit_log_enabled = True
                if response['Logs']['General']:
                    general_log_enabled = True

                if not audit_log_enabled and not general_log_enabled:
                    msg = "Audit and General log is not enabled for broker."
                    failures = self.helper.append_item_to_list(failures, 'mq', broker['BrokerName'], broker['BrokerArn'] , self.region, msg)
                elif not audit_log_enabled and general_log_enabled:
                    msg = "Audit log is not enabled for broker."
                    failures = self.helper.append_item_to_list(failures, 'mq', broker['BrokerName'], broker['BrokerArn'] , self.region, msg)
                elif audit_log_enabled and not general_log_enabled:
                    msg = "General log is not enabled for broker."
                    failures = self.helper.append_item_to_list(failures, 'mq', broker['BrokerName'], broker['BrokerArn'] , self.region, msg)
            
            except Exception as e:
                self.logger.error(f"Error while getting broker details - { broker['BrokerArn'] }: {e}")
                continue
        
        return failures

    def mq_broker_publicaly_accessible(self):
        failures = []
        
        for broker in self.brokers:

            try:

                response = self.describe_broker(broker['BrokerId'])

                if not response['PubliclyAccessible']:
                    failures = self.helper.append_item_to_list(failures, 'mq', broker['BrokerName'], broker['BrokerArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting broker details - { broker['BrokerArn'] }: {e}")
                continue
        
        return failures

    def mq_broker_auto_minor_version_upgrade_not_enabled(self):
        failures = []
        
        for broker in self.brokers:

            try:

                response = self.describe_broker(broker['BrokerId'])

                if not response['AutoMinorVersionUpgrade']:
                    failures = self.helper.append_item_to_list(failures, 'mq', broker['BrokerName'], broker['BrokerArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting broker details - { broker['BrokerArn'] }: {e}")
                continue
        
        return failures