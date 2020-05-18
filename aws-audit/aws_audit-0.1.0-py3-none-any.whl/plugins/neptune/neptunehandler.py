import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class neptunehandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create Neptune client
            self.neptune_client = session.client('neptune', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Neptune client', {'region': self.region})

        self.instances = self.describe_db_instances()

    def describe_db_instances(self):
        instances = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.neptune_client.describe_db_instances(Marker = response['Marker'])
                else:
                    response = self.neptune_client.describe_db_instances()

                instances.extend(response['DBInstances'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Neptune describe_db_instances', {'region': self.region})

            if 'Marker' not in response:
                break

        return instances

    def neptune_iam_authentication_not_enabled(self):
        failures = []

        for instance in self.instances:
            if not instance['IAMDatabaseAuthenticationEnabled']:
                failures = self.helper.append_item_to_list(failures, 'neptune', instance['DBInstanceIdentifier'], instance['DBInstanceArn'] , self.region)

        return failures

    def neptune_database_encryption_not_enabled(self):
        failures = []

        for instance in self.instances:
            if not instance['StorageEncrypted']:
                failures = self.helper.append_item_to_list(failures, 'neptune', instance['DBInstanceIdentifier'], instance['DBInstanceArn'] , self.region)

        return failures

    def neptune_database_not_encrypted_with_kms_cmk(self):
        failures = []

        for instance in self.instances:
            if not instance['StorageEncrypted']:
                failures = self.helper.append_item_to_list(failures, 'neptune', instance['DBInstanceIdentifier'], instance['DBInstanceArn'] , self.region)
            else:
                kms_details = self.helper.get_kms_key_details(instance['KmsKeyId'])
                if kms_details['KeyManager'] != 'CUSTOMER':
                    failures = self.helper.append_item_to_list(failures, 'neptune', instance['DBInstanceIdentifier'], instance['DBInstanceArn'] , self.region)
        return failures
    
    def neptune_database_is_publicly_accessible(self):
        failures = []

        for instance in self.instances:
            if instance['PubliclyAccessible']:
                failures = self.helper.append_item_to_list(failures, 'neptune', instance['DBInstanceIdentifier'], instance['DBInstanceArn'] , self.region)

        return failures

    def neptune_database_auto_minor_version_upgrade_not_enabled(self):
        failures = []

        for instance in self.instances:
            if not instance['AutoMinorVersionUpgrade']:
                failures = self.helper.append_item_to_list(failures, 'neptune', instance['DBInstanceIdentifier'], instance['DBInstanceArn'] , self.region)

        return failures

    def neptune_database_using_default_port(self):
        failures = []

        for instance in self.instances:
            if instance['Endpoint']['Port'] == '8182':
                failures = self.helper.append_item_to_list(failures, 'neptune', instance['DBInstanceIdentifier'], instance['DBInstanceArn'] , self.region)

        return failures
