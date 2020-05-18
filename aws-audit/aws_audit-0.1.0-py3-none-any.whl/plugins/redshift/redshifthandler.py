import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class redshifthandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create Redshift client
            self.redshift_client = session.client('redshift', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Redshift client', {'region': self.region})

        self.clusters = self.describe_clusters()

    def describe_clusters(self):
        clusters = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.redshift_client.describe_clusters(Marker = response['Marker'])
                else:
                    response = self.redshift_client.describe_clusters()

                clusters.extend(response['Clusters'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Redshift describe_clusters', {'region': self.region})

            if 'Marker' not in response:
                break

        return clusters

    def describe_cluster_parameters(self, parameter_group_name):
        parameters = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.redshift_client.describe_cluster_parameters(ParameterGroupName=parameter_group_name, Marker = response['Marker'])
                else:
                    response = self.redshift_client.describe_cluster_parameters(ParameterGroupName=parameter_group_name)

                parameters.extend(response['Parameters'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Redshift describe_cluster_parameters', {'region': self.region})

            if 'Marker' not in response:
                break

        return parameters

    def describe_logging_status(self, cluster_identifier):
        try:
            response = self.redshift_client.describe_logging_status(ClusterIdentifier=cluster_identifier)

            return response

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call Redshift describe_logging_status', {'region': self.region})

    def redshift_cluster_user_activity_logging_not_enabled(self):
        failures = []

        for cluster in self.clusters:
            failed = 0
            for parameter_group in cluster['ClusterParameterGroups']:
                try:                    
                    parameters = self.describe_cluster_parameters(parameter_group['ParameterGroupName'])
                    for parameter in parameters:
                        if parameter['ParameterName'] == 'enable_user_activity_logging' and parameter['ParameterValue'] == 'false':
                            failed = 1
                            break
            
                except Exception as e:
                    self.logger.error(f"Error while getting cluster paramter group details: {e}")

            if failed:
                failures = self.helper.append_item_to_list(failures, 'redshift', cluster['ClusterIdentifier'], cluster['ClusterIdentifier'] , self.region)

        return failures

    def redshift_cluster_audit_logging_not_enabled(self):
        failures = []

        for cluster in self.clusters:
            try:
                logging = self.describe_logging_status(cluster['ClusterIdentifier'])
                if not logging['LoggingEnabled']:
                    failures = self.helper.append_item_to_list(failures, 'redshift', cluster['ClusterIdentifier'], cluster['ClusterIdentifier'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting cluster logging status details: {e}")

        return failures

    def redshift_cluster_using_default_port(self):
        failures = []

        for cluster in self.clusters:
            if cluster['Endpoint']['Port'] == '5439' :
                failures = self.helper.append_item_to_list(failures, 'redshift', cluster['ClusterIdentifier'], cluster['ClusterIdentifier'] , self.region)

        return failures

    def redshift_clutser_encryption_not_enabled(self):
        failures = []

        for cluster in self.clusters:
            if not cluster['Encrypted']:
                failures = self.helper.append_item_to_list(failures, 'redshift', cluster['ClusterIdentifier'], cluster['ClusterIdentifier'] , self.region)

        return failures

    def redshift_cluster_not_encrypted_with_kms_cmk(self):
        failures = []

        for cluster in self.clusters:
            if not cluster['Encrypted']:
                failures = self.helper.append_item_to_list(failures, 'redshift', cluster['ClusterIdentifier'], cluster['ClusterIdentifier'] , self.region)
            else:                
                key_details = self.helper.get_kms_key_details(cluster['KmsKeyId'])
                if key_details['KeyManager'] != 'CUSTOMER':
                    failures = self.helper.append_item_to_list(failures, 'redshift', cluster['ClusterIdentifier'], cluster['ClusterIdentifier'] , self.region)

        return failures

    def redshift_cluster_not_in_vpc(self):
        failures = []

        for cluster in self.clusters:
            if not cluster.get('VpcId'):
                failures = self.helper.append_item_to_list(failures, 'redshift', cluster['ClusterIdentifier'], cluster['ClusterIdentifier'] , self.region)

        return failures

    def redshift_cluster_publicly_accessible(self):
        failures = []

        for cluster in self.clusters:
            if cluster['PubliclyAccessible']:
                failures = self.helper.append_item_to_list(failures, 'redshift', cluster['ClusterIdentifier'], cluster['ClusterIdentifier'] , self.region)

        return failures

    def redshift_cluster_required_ssl_parameter_not_enabled(self):
        failures = []

        for cluster in self.clusters:
            failed = 0
            for parameter_group in cluster['ClusterParameterGroups']:
                try:                    
                    parameters = self.describe_cluster_parameters(parameter_group['ParameterGroupName'])
                    for parameter in parameters:
                        if parameter['ParameterName'] == 'require_ssl' and parameter['ParameterValue'] == 'false':
                            failed = 1
                            break
            
                except Exception as e:
                    self.logger.error(f"Error while getting cluster paramter group details: {e}")

            if failed:
                failures = self.helper.append_item_to_list(failures, 'redshift', cluster['ClusterIdentifier'], cluster['ClusterIdentifier'] , self.region)

        return failures
