
import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class transferhandler : 
    
    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create Transfer client
            self.transfer_client = session.client('transfer', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Transfer client', {'region': self.region})

        self.servers = self.list_servers()

    def list_servers(self):
        servers = []
        response = {}

        while True:

            try:
                if 'NextToken' in response:
                    response = self.transfer_client.list_servers(NextToken=response['NextToken'])
                else:
                    response = self.transfer_client.list_servers()

                servers.extend(response['Servers'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Transfer list_servers', {'region': self.region})

            if 'NextToken' not in response:
                break

        return servers

    def transfer_logging_not_enabled(self):

        failures = []

        for server in self.servers:
            if not server.get('LoggingRole'):
                failures = self.helper.append_item_to_list(failures, 'transfer', server['ServerId'], server['Arn'] , self.region)

        return failures

    def transfer_not_using_privatelink_for_endpoints(self):

        failures = []

        for server in self.servers:
            if server['EndpointType'] == 'PUBLIC':
                failures = self.helper.append_item_to_list(failures, 'transfer', server['ServerId'], server['Arn'] , self.region)

        return failures