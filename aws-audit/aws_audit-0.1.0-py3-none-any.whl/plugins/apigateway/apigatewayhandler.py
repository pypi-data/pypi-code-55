import json, os
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error
from datetime import datetime, timedelta
from pytz import timezone
import pytz

class apigatewayhandler : 
    
    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create APIGateway client
            self.apigateway_client = session.client('apigateway', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create APIGateway client', {'region': self.region})        
        
        self.rest_apis = self.get_rest_apis()
        self.api_stages = {}

    def get_rest_apis(self):
        apis = []
        response = {}
        while True:
            try:
                if 'position' in response:
                    response = self.apigateway_client.get_rest_apis(position=response['position'])
                else:
                    response = self.apigateway_client.get_rest_apis()
            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call apigateway get_rest_apis', {'region': self.region})

            apis.extend(response['items'])

            if 'position' not in response:
                break
        
        return apis

    def get_stages(self, api_id):
        try:
            response = self.apigateway_client.get_stages(restApiId=api_id)
            self.api_stages[api_id] = response
            return response
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call apigateway get_stages', {'region': self.region})
        
    def api_gateway_not_integrated_with_waf(self):
        failures = []

        for api in self.rest_apis:
            try:
                if api['id'] not in self.api_stages:
                    result = self.get_stages(api['id'])
                else:
                    result = self.api_stages[api['id']]
                if 'item' in result:
                    for item in result['item']:
                        if item['stageName'] == 'Production' and not item['webAclArn']:
                            failures = self.helper.append_item_to_list(failures, 'apigateway', api['id'], api['name'], self.region)
                            break
            except Exception as e:
                self.logger.error(f"Error while getting acm apigateway stage details - {api['id']} : {e}")

        return failures
    
    def api_gateway_client_ssl_certificate_not_enabled(self):
        failures = []

        for api in self.rest_apis:
            try:
                if api['id'] not in self.api_stages:
                    result = self.get_stages(api['id'])
                else:
                    result = self.api_stages[api['id']]
                if 'item' in result:
                    for item in result['item']:
                        if (item['stageName'] == 'Staging' or item['stageName'] == 'Production') and not item['clientCertificateId']:
                            failures = self.helper.append_item_to_list(failures, 'apigateway', api['id'], api['name'], self.region)
                            break
            except Exception as e:
                self.logger.error(f"Error while getting acm apigateway stage details - {api['id']} : {e}")

        return failures
        
    def api_gateway_api_publicly_accessible(self):
        failures = []

        for api in self.rest_apis:
            if 'endpointConfiguration' in api:
                types = api['endpointConfiguration']['types']
                if 'REGIONAL' not in types or 'EDGE' not in types:
                    failures = self.helper.append_item_to_list(failures, 'apigateway', api['id'], api['name'], self.region)

        return failures