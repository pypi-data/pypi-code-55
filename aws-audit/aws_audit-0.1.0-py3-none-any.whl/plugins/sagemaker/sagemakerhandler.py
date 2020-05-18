import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class sagemakerhandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create Sagemaker client
            self.sagemaker_client = session.client('sagemaker', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Sagemaker client', {'region': self.region})
        
        self.notebook_instances = self.list_notebook_instances()

    def list_notebook_instances(self):
        notebook_instances = []
        response = {}

        while True:

            try:
                if 'NextToken' in response:
                    response = self.sagemaker_client.list_notebook_instances(NextToken = response['NextToken'])
                else:
                    response = self.sagemaker_client.list_notebook_instances()

                notebook_instances.extend(response['NotebookInstances'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Sagemaker list_notebook_instances', {'region': self.region})

            if 'NextToken' not in response:
                break

        return notebook_instances

    def describe_notebook_instance(self, notebook_instance_name):
        try:
            response = self.sagemaker_client.describe_notebook_instance(NotebookInstanceName=notebook_instance_name)

            return response

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call Sagemaker describe_notebook_instance', {'region': self.region})

    def sagemaker_notebook_instance_not_in_vpc(self):
        failures = []

        for instance in self.notebook_instances:
            try:
                details = self.describe_notebook_instance(instance['NotebookInstanceName'])

                if 'SubnetId' not in details:
                    failures = self.helper.append_item_to_list(failures, 'sagemaker', instance['NotebookInstanceName'], instance['NotebookInstanceArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting Sagemaker notebook details: {e}")

        return failures

    def sagemaker_notebook_data_is_not_encrypted(self):
        failures = []

        for instance in self.notebook_instances:
            try:
                details = self.describe_notebook_instance(instance['NotebookInstanceName'])

                if 'KmsKeyId' not in details:
                    failures = self.helper.append_item_to_list(failures, 'sagemaker', instance['NotebookInstanceName'], instance['NotebookInstanceArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting Sagemaker notebook details: {e}")

        return failures

    def sagemaker_notebook_not_encrypted_with_kms_cmk(self):
        failures = []

        for instance in self.notebook_instances:
            try:
                details = self.describe_notebook_instance(instance['NotebookInstanceName'])

                if 'KmsKeyId' in details:
                    key_details = self.helper.get_kms_key_details(details['KmsKeyId'])
                    if key_details['KeyManager'] != 'CUSTOMER':
                        failures = self.helper.append_item_to_list(failures, 'sagemaker', instance['NotebookInstanceName'], instance['NotebookInstanceArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting Sagemaker notebook details: {e}")

        return failures

    def sagemaker_notebook_direct_internet_access_enabled(self):
        failures = []

        for instance in self.notebook_instances:
            try:
                details = self.describe_notebook_instance(instance['NotebookInstanceName'])

                if details['DirectInternetAccess'] == 'Enabled':
                    failures = self.helper.append_item_to_list(failures, 'sagemaker', instance['NotebookInstanceName'], instance['NotebookInstanceArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting Sagemaker notebook details: {e}")

        return failures

