import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class rdshandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.session = session
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create rds client
            self.rds_client = session.client('rds', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create rds client', {'region': self.region})

        self.snapshots = self.describe_db_snapshots()
        self.instances = self.describe_db_instances()
        self.clusters = self.describe_db_clusters()

    def describe_db_snapshots(self):
        snapshots = []
        response = {}
        while(True):
            try:
                if 'Marker' in response:
                    response = self.rds_client.describe_db_snapshots(Marker=response['Marker'])
                else:
                    response = self.rds_client.describe_db_snapshots()
                
                snapshots.extend(response['DBSnapshots'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call rds describe_db_snapshots', {'region': self.region})
            
            if 'Marker' not in response:
                break
        
        return snapshots

    def describe_db_instances(self):
        instances = []
        response = {}
        while(True):
            try:
                if 'Marker' in response:
                    response = self.rds_client.describe_db_instances(Marker=response['Marker'])
                else:
                    response = self.rds_client.describe_db_instances()
                
                instances.extend(response['DBInstances'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call rds describe_db_instances', {'region': self.region})
            
            if 'Marker' not in response:
                break
        
        return instances

    def describe_db_clusters(self):
        clusters = []
        response = {}
        while(True):
            try:
                if 'Marker' in response:
                    response = self.rds_client.describe_db_clusters(Marker=response['Marker'])
                else:
                    response = self.rds_client.describe_db_clusters()
                
                clusters.extend(response['DBClusters'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call rds describe_db_clusters', {'region': self.region})
            
            if 'Marker' not in response:
                break
        
        return clusters

    def describe_db_security_groups(self):
        security_groups = []
        response = {}
        while(True):
            try:
                if 'Marker' in response:
                    response = self.rds_client.describe_db_security_groups(Marker=response['Marker'])
                else:
                    response = self.rds_client.describe_db_security_groups()
                
                security_groups.extend(response['DBSecurityGroups'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call rds describe_db_security_groups', {'region': self.region})
            
            if 'Marker' not in response:
                break
        
        return security_groups

    def describe_db_snapshot_attributes(self, snapshot_identifire):
        try:
            response = self.rds_client.describe_db_snapshot_attributes(DBSnapshotIdentifier=snapshot_identifire)

            return response

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call rds describe_db_snapshot_attributes', {'region': self.region})

    def rds_public_snapshot(self):
        failures = []

        for snapshot in self.snapshots:
            try:
                result = self.describe_db_snapshot_attributes(snapshot['DBInstanceIdentifier'])
                if 'DBSnapshotAttributesResult' in result:
                    for attributes in result['DBSnapshotAttributesResult']['DBSnapshotAttributes']:
                        if attributes['AttributeName'] == 'restore' and 'all' in attributes['AttributeValues']:
                            failures = self.helper.append_item_to_list(failures, 'rds', snapshot['DBSnapshotIdentifier'], snapshot['DBSnapshotArn'], self.region)
                            break
            except Exception as e:
                self.logger.error(f"Failed to calling rds rds_public_snapshot: {e}")                

        return failures

    def rds_aurora_deletion_protection_not_enabled(self):
        failures = []
        for cluster in self.clusters:
            if cluster['Engine'] == 'aurora':
                if not cluster['DeletionProtection']:
                    failures = self.helper.append_item_to_list(failures, 'rds', cluster['DatabaseName'], cluster['DBClusterIdentifier'], self.region)

        return failures

    def rds_log_export_not_enabled(self):
        failures = []
        for instance in self.instances:
            if cluster['Engine'] == 'mysql' or cluster['Engine'] == 'mariadb' or cluster['Engine'] == 'aurora' :   
                if not instance['EnabledCloudwatchLogsExports']:
                    failures = self.helper.append_item_to_list(failures, 'rds', instance['DBName'], instance['DBInstanceIdentifier'], self.region)
        
        return failures

    def rds_aurora_serverless_log_exports_not_enabled(self):
        failures = []
        for cluster in self.clusters:
            
            if cluster['Engine'] == 'aurora' and cluster['EngineMode'] == 'serverless':
                if not cluster['EnabledCloudwatchLogsExports']:
                    failures = self.helper.append_item_to_list(failures, 'rds', cluster['DatabaseName'], cluster['DBClusterIdentifier'], self.region)
            
        return failures

    def rds_iam_authentication_not_enabled(self):
        failures = []
        for instance in self.instances:            
            if instance['Engine'] == 'mysql' or instance['Engine'] == 'postgres':
                if not instance['IAMDatabaseAuthenticationEnabled']:
                    failures = self.helper.append_item_to_list(failures, 'rds', instance['DBName'], instance['DBInstanceIdentifier'], self.region)
        
        return failures

    def rds_deletion_protection_not_enabled(self):
        failures = []
        for instance in self.instances:
            
            if not instance['DeletionProtection']:
                failures = self.helper.append_item_to_list(failures, 'rds', instance['DBName'], instance['DBInstanceIdentifier'], self.region)
        
        return failures

    def rds_auto_minor_version_upgrade_not_enabled(self):
        failures = []
        for instance in self.instances:
            
            if not instance['AutoMinorVersionUpgrade']:
                failures = self.helper.append_item_to_list(failures, 'rds', instance['DBName'], instance['DBInstanceIdentifier'], self.region)
        
        return failures

    def rds_default_port_using(self):
        failures = []
        db_engines = {'mysql': 3306, 'aurora': 3306, 'oracle': 1521, 'postgres': 5432, 'mariadb': 3306,'sqlserver': 1433}
        for instance in self.instances:
            
            if instance['Engine'] in db_engines.keys():
                if instance['Endpoint']['Port'] == db_engines[instance['Engine']]:
                    msg = f"RDS instance with DB name {instance['DBName']} with engine {instance['Engine']} is using default port {db_engines[instance['Engine']]}"
                    failures = self.helper.append_item_to_list(failures, 'rds', instance['DBName'], instance['Engine'], self.region, msg)

        return failures

    def rds_not_encypted_with_kms_cmk(self):
        failures = []
        for instance in self.instances:
            
            if not instance['StorageEncrypted']:
                failures = self.helper.append_item_to_list(failures, 'rds', instance['DBName'], instance['DBInstanceIdentifier'], self.region)
            if instance.get('KmsKeyId'):
                response = self.helper.get_kms_key_details(instance['KmsKeyId'])
                if response['KeyManager'] != 'CUSTOMER' : 
                    failures = self.helper.append_item_to_list(failures, 'volumes', instance['DBName'], instance['DBInstanceIdentifier'] , self.region)
        
        return failures

    def rds_encryption_not_enabled(self):
        failures = []
        for instance in self.instances:
            
            if not instance['StorageEncrypted']:
                failures = self.helper.append_item_to_list(failures, 'rds', instance['DBName'], instance['DBInstanceIdentifier'], self.region)
            
        return failures

    def rds_publicly_accessible(self):
        failures = []
        for instance in self.instances:
            
            if instance['PubliclyAccessible']:
                failures = self.helper.append_item_to_list(failures, 'rds', instance['DBName'], instance['DBInstanceIdentifier'], self.region)
        
        return failures

    def rds_unrestricted_security_group(self):
        failures = []
        security_groups = self.describe_db_security_groups()
        for security_group in security_groups: 
            failed = 0
            for iprange in security_group['IPRanges']:
                if iprange['CidrIp'] == "0.0.0.0/0" and iprange['Status'] == "authorized":
                    failed = 1
            if failed:
                failures = self.helper.append_item_to_list(failures, 'security_groups', security_group['GroupName'], security_group['GroupId'] , self.region)

        return failures

    def rds_snapshot_not_encrypted(self):
        failures = []
        for snapshot in self.snapshots:
            
            if not snapshot['Encrypted']:
                failures = self.helper.append_item_to_list(failures, 'rds', snapshot['DBSnapshotIdentifier'], snapshot['DBSnapshotArn'], self.region)

        return failures
    