import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class ekshandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create EKS client
            self.eks_client = session.client('eks', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create EKS client', {'region': self.region})

        try:
            # Create EC2 client
            self.ec2_client = session.client('ec2', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create EC2 client', {'region': self.region})

        self.clusters = self.list_clusters()

    def list_clusters(self):
        clusters = []
        response = {}

        while True:

            try:
                if 'nextToken' in response:
                    response = self.eks_client.list_clusters(nextToken = response['nextToken'])
                else:
                    response = self.eks_client.list_clusters()
                
                clusters.extend(response['clusters'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call EKS list_clusters', {'region': self.region})
            
            if 'nextToken' not in response:
                break

        return clusters

    def describe_cluster(self, cluster_name):
        try:
            response = self.eks_client.describe_cluster(name=cluster_name)

            return response['cluster']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call EKS describe_cluster', {'region': self.region})

    def describe_security_groups(self, security_groups):
        try:
            response = self.ec2_client.describe_security_groups(GroupIds=security_groups)
            
            return response['SecurityGroups']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to EC2 describe_security_groups', {'region': self.region})        

    def eks_cluster_logging_not_enabled(self):
        failures = []
        for cluster in self.clusters:
            try:
                cluster_details = self.describe_cluster(cluster)
                logging_disabled = ''
                for logging in cluster_details['logging']['clusterLogging']:
                    if not logging['enabled']:
                        logging_disabled = ', '.join(logging['types'])
                if logging_disabled != '' : 
                    msg = "%s logging disabled for %s" %(cluster,logging_disabled)
                    failures = self.helper.append_item_to_list(failures, 'eks', cluster, cluster_details['arn'] , self.region, msg)
                    

            except Exception as e:
                self.logger.error(f"Error while getting EKS cluster details: {e}")
            
        return failures

    def eks_security_group_not_secure(self):
        failures = []
        
        for cluster in self.clusters:
            try:
                cluster_details = self.describe_cluster(cluster)
                cluster_security_groups = cluster_details['resourcesVpcConfig']['securityGroupIds']
                failed = 0
                if len(cluster_security_groups) > 0 :
                    security_group_details = self.describe_security_groups(cluster_security_groups)
                    for security_group in security_group_details:
                        for permission in security_group['IpPermissions']:
                            if permission['FromPort'] != 443 and  permission['ToPort'] != 443 : 
                                failed = 1
                if failed:
                    failures = self.helper.append_item_to_list(failures, 'eks', cluster, cluster_details['arn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting EKS cluster details: {e}")
        
        return failures

    def eks_cluster_endpoint_publicly_accessible(self):
        failures = []
        for cluster in self.clusters:
            try:
                cluster_details = self.describe_cluster(cluster)
                if cluster_details['resourcesVpcConfig']['endpointPublicAccess']:
                    failures = self.helper.append_item_to_list(failures, 'eks', cluster, cluster_details['arn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting EKS cluster details: {e}")

        return failures

