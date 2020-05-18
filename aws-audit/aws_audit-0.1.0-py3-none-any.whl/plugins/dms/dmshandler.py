import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class dmshandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create DMS client
            self.dms_client = session.client('dms', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create DMS client', {'region': self.region})

        self.instances = self.describe_replication_instances()
    
    def describe_replication_instances(self):
        instances = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.dms_client.describe_replication_instances(Marker = response['Marker'])
                else:
                    response = self.dms_client.describe_replication_instances()
                
                instances.extend(response['ReplicationInstances'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Backup list_backup_vaults', {'region': self.region})

            if 'Marker' not in response:
                break

        return instances

    def dms_replication_instance_not_encrypted_with_kms_cmk(self):
        failures = []

        for instance in self.instances:
            if 'KmsKeyId' in instance:
                key_details = self.helper.get_kms_key_details(instance['KmsKeyId'])
                if key_details['KeyManager'] != 'CUSTOMER':
                    failures = self.helper.append_item_to_list(failures, 'dms', instance['ReplicationInstanceIdentifier'], instance['ReplicationInstanceArn'] , self.region)

        return failures

    def dms_replication_instance_publicly_accessible(self):
        failures = []

        for instance in self.instances:
            if instance['PubliclyAccessible']:
                failures = self.helper.append_item_to_list(failures, 'dms', instance['ReplicationInstanceIdentifier'], instance['ReplicationInstanceArn'] , self.region)

        return failures

    def dms_replication_instance_auto_minor_version_upgrade_not_enabled(self):
        failures = []

        for instance in self.instances:
            if not instance['AutoMinorVersionUpgrade']:
                failures = self.helper.append_item_to_list(failures, 'dms', instance['ReplicationInstanceIdentifier'], instance['ReplicationInstanceArn'] , self.region)

        return failures
