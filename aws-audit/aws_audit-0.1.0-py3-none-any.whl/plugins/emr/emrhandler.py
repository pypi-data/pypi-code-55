import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class emrhandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create EMR client
            self.emr_client = session.client('emr', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create EMR client', {'region': self.region})

        self.clusters = self.list_clusters()
    
    def list_clusters(self):
        clusters = []
        response = {}

        while True:

            try:
                cluster_states = ['STARTING','BOOTSTRAPPING','RUNNING','WAITING']
                if 'Marker' in response:
                    response = self.emr_client.list_clusters(ClusterStates=cluster_states, Marker = response['Marker'])
                else:
                    response = self.emr_client.list_clusters(ClusterStates=cluster_states)

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call EMR list_clusters', {'region': self.region})
            
            clusters.extend(response['Clusters'])

            if 'Marker' not in response:
                break

        return clusters

    def describe_cluster(self, cluster_id):
        try:
            response = self.emr_client.describe_cluster(ClusterId=cluster_id)

            return response['Cluster']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call EMR describe_cluster', {'region': self.region})

    def emr_cluster_not_in_vpc(self):

        failures = []

        for cluster in self.clusters:
            try:
                details = self.describe_cluster(cluster)
                if 'Ec2SubnetId' in details['Ec2InstanceAttributes']:
                    if details['Ec2InstanceAttributes']['Ec2SubnetId'] == '':
                        failures = self.helper.append_item_to_list(failures, 'backup', cluster['Name'], cluster['ClusterArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting EMR Cluster details: {e}")
        
        return failures

    def emr_cluster_in_transit_and_at_rest_encryption_not_enabled(self):
        failures = []

        for cluster in self.clusters:
            try:
                details = self.describe_cluster(cluster)
                if 'SecurityConfiguration' not in details:
                    failures = self.helper.append_item_to_list(failures, 'backup', cluster['Name'], cluster['ClusterArn'] , self.region)
                elif not details['SecurityConfiguration']:
                    failures = self.helper.append_item_to_list(failures, 'backup', cluster['Name'], cluster['ClusterArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting EMR Cluster details: {e}")
        
        return failures