import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error


class kafkahandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create Kafka client
            self.backup_client = session.client('kafka', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Kafka client', {'region': self.region})

        self.clusters = self.list_clusters()
    
    def list_clusters(self):
        clusters = []
        response = {}

        while True:

            try:
                if 'NextToken' in response:
                    response = self.backup_client.list_clusters(NextToken = response['NextToken'])
                else:
                    response = self.backup_client.list_clusters()

                clusters.extend(response['ClusterInfoList'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Kafka list_clusters', {'region': self.region})

            if 'NextToken' not in response:
                break

        return clusters 

    def kafka_cluster_using_kms_cmk(self):
        failures = []

        for cluster in self.clusters:
            
            kms_key = self.helper.get_kms_key_details(cluster['EncryptionInfo']['EncryptionAtRest']['DataVolumeKMSKeyId'])
            if kms_key['KeyManager'] != 'CUSTOMER':
                failures = self.helper.append_item_to_list(failures, 'backup', cluster['ClusterName'], cluster['ClusterArn'] , self.region)
        
        return failures
