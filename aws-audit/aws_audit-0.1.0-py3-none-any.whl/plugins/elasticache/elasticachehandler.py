import json, os
# from botocore.exceptions import Exception
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class elasticachehandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create ElastiCache client
            self.elasticache_client = session.client('elasticache', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create ElastiCache client', {'region': self.region})
        
        self.clusters = self.describe_cache_clusters()

    def describe_cache_clusters(self):
        clusters = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.elasticache_client.describe_cache_clusters(Marker = response['Marker'])
                else:
                    response = self.elasticache_client.describe_cache_clusters()

                clusters.extend(response['CacheClusters'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call ElastiCache describe_cache_clusters', {'region': self.region})

            if 'Marker' not in response:
                break

        return clusters

    def elasticache_cluster_using_default_port(self):
        failures = []

        for cluster in self.clusters:
            if cluster['Engine'] == 'memcached' and int(cluster['ConfigurationEndpoint']['Port']) == 11211:
                failures = self.helper.append_item_to_list(failures, 'elasticache', cluster['CacheClusterId'], cluster['CacheClusterId'] , self.region)
            if cluster['Engine'] == 'redis' and int(cluster['ConfigurationEndpoint']['Port']) == 6379:
                failures = self.helper.append_item_to_list(failures, 'elasticache', cluster['CacheClusterId'], cluster['CacheClusterId'] , self.region)

        return failures
    
    def elasticache_cluster_not_in_vpc(self):
        failures = []

        for cluster in self.clusters:
            if 'CacheSubnetGroupName' not in cluster:
                failures = self.helper.append_item_to_list(failures, 'elasticache', cluster['CacheClusterId'], cluster['CacheClusterId'] , self.region)
            elif cluster['CacheSubnetGroupName'] == '':
                failures = self.helper.append_item_to_list(failures, 'elasticache', cluster['CacheClusterId'], cluster['CacheClusterId'] , self.region)

        return failures

    def elasticache_redis_cluster_encryption_at_rest_and_in_transit_not_enabled(self):
        failures = []

        for cluster in self.clusters:
            not_supported_versions = ['3.2.4','3.2.10','2.8.24','2.8.23','2.8.22','2.8.21','2.8.19','2.8.6','2.6.13']
            if cluster['Engine'] == 'memcached':
                if cluster['EngineVersion'] not in not_supported_versions:
                    if not cluster['AtRestEncryptionEnabled'] and not cluster['TransitEncryptionEnabled']:
                        msg = "In-Transit and At-Rest encryption not enabled for redis cluster."
                        failures = self.helper.append_item_to_list(failures, 'elasticache', cluster['CacheClusterId'], cluster['CacheClusterId'] , self.region, msg)
                    if not cluster['AtRestEncryptionEnabled'] and  cluster['TransitEncryptionEnabled']:
                        msg = "At-Rest encryption not enabled for redis cluster."
                        failures = self.helper.append_item_to_list(failures, 'elasticache', cluster['CacheClusterId'], cluster['CacheClusterId'] , self.region, msg)
                    if cluster['AtRestEncryptionEnabled'] and not cluster['TransitEncryptionEnabled']:
                        msg = "In-Transit encryption not enabled for redis cluster."
                        failures = self.helper.append_item_to_list(failures, 'elasticache', cluster['CacheClusterId'], cluster['CacheClusterId'] , self.region, msg)

        return failures