import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class confighandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create Config client
            self.config_client = session.client('config', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Config client', {'region': self.region})

        self.configuration_recorders = self.describe_configuration_recorders()

    def describe_configuration_recorders(self):
        try:
            response = self.config_client.describe_configuration_recorders()

            return response['ConfigurationRecorders']

        except Exception as e:
            raise classify_error(self.logger, e, "Failed to call Config describe_configuration_recorders", {'region': self.region})

    def describe_configuration_recorder_status(self, configuration_recorder_names):
        try:
            response = self.config_client.describe_configuration_recorder_status(ConfigurationRecorderNames=configuration_recorder_names)

            return response['ConfigurationRecordersStatus']

        except Exception as e:
            raise classify_error(self.logger, e, "Failed to call Config describe_configuration_recorder_status", {'region': self.region})

    def aws_config_not_enabled(self):
        failures = []
        if not len(self.configuration_recorders):
            msg = "AWS Config Service is not enabled."
            failures = self.helper.append_item_to_list(failures, 'config', "", "" , self.region, msg)
        return failures
    
    def aws_config_not_included_global_resources(self):
        failures = []

        for recorders in self.configuration_recorders:
            if not recorders['recordingGroup']['includeGlobalResourceTypes']:
                failures = self.helper.append_item_to_list(failures, 'config', recorders['name'], recorders['roleARN'], self.region)
        
        return failures

    def aws_config_delivery_failed(self):
        failures = []

        for recorders in self.configuration_recorders:
            try:
                statuses = self.describe_configuration_recorder_status(recorders['name'])
                for status in statuses:
                    if status['lastStatus'] == 'Failure':
                        failures = self.helper.append_item_to_list(failures, 'config', recorders['name'], recorders['roleARN'], self.region)
            except Exception as e:
                self.logger.error(f"Error while getting configuration recorder status: {e}")

        return failures