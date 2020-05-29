from awsdeployer.__apigateway.ApiErrorResponses import *
from awsdeployer.__apigateway.GatewayHandler import GatewayHandler
from awsdeployer.__apigateway.Templater import *
from awsdeployer.__util import build_path


class ApiWrapper:
    """This class provides higher-level primitives for API Gateway actions"""
    def __init__(self, aws_config, full_responses, extended_responses):
        self.aws = aws_config
        self.full_responses = full_responses
        self.extended_responses = extended_responses

        self.gateway_handler = GatewayHandler(self.aws)

    def create_method(self, path, method, configs):
        # get resource id to operate on
        resource_id = self.get_resource_id(path)

        # if method already exists, delete it to be able to replace everything
        if resource_id and self.gateway_handler.has_method(resource_id, method):
            print('Deleting pre-existing method...')
            self.gateway_handler.delete_method(resource_id, method)

        # create resource if needed
        if not resource_id:
            self.create_resource(path)
            resource_id = self.get_resource_id(path)

        print('Creating method {0} at resource {1}'.format(method, resource_id))

        # get necessary configs
        lambda_function = configs['function']

        # create request objects based on templates
        request_parameters = create_request_parameters(configs)
        request_body = configs['request_body'] if 'request_body' in configs else []
        request_template = create_request_template(request_parameters, path_parameters=get_path_parameters(path), request_body=request_body)

        # create response objects based on templates
        response_parameters = create_response_parameters(configs, 'cors' in configs and configs['cors'])

        # create method and integration with lambda
        self.gateway_handler.create_method(resource_id, method, request_parameters)
        self.gateway_handler.create_lambda_integration(resource_id, method, lambda_function, request_template)

        # create responses for sucess, all programmed errors, and catchall
        # (works for any non-empty error string; empty would match 200 too)
        self.gateway_handler.create_method_response(resource_id, method, '200', response_parameters)
        self.gateway_handler.create_integration_response(resource_id, method, '200', response_parameters, '', get_success_response_template())

        for response in responses_common.keys():
            self.__create_response(resource_id, method, response, str(responses_common[response]), response_parameters)

        if self.full_responses:
            for response in responses_full.keys():
                self.__create_response(resource_id, method, response, str(responses_full[response]), response_parameters)

        if self.extended_responses:
            for response in responses_extended.keys():
                self.__create_response(resource_id, method, response, str(responses_extended[response]), response_parameters)

        # catchall (Bad Gateway, should catch Lambda errors such as timeout or syntax errors)
        self.gateway_handler.create_method_response(resource_id, method, '502', response_parameters)
        self.gateway_handler.create_integration_response(resource_id, method, '502', response_parameters, '\s*.+\s*', get_error_catchall_response_template())

        if 'cors' in configs and configs['cors']:
            print('Adding CORS to resource')

            # if OPTIONS already exists, delete it to be able to replace everything
            if self.gateway_handler.has_method(resource_id, 'OPTIONS'):
                self.gateway_handler.delete_method(resource_id, 'OPTIONS')

            cors_response_params = {
                'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
                'method.response.header.Access-Control-Allow-Methods': '\'HEAD,GET,POST,PUT,PATCH,DELETE,ANY,OPTIONS\'',
                'method.response.header.Access-Control-Allow-Origin': '\'*\''
            }

            # create OPTIONS method
            self.gateway_handler.create_method(resource_id, 'OPTIONS')
            self.gateway_handler.create_mock_integration(resource_id, 'OPTIONS')
            self.gateway_handler.create_method_response(resource_id, 'OPTIONS', '200', cors_response_params)
            self.gateway_handler.create_integration_response(resource_id, 'OPTIONS', '200', cors_response_params, '', '')

            # put CORS in gateway responses
            gateway_response_params = {
                'gatewayresponse.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
                'gatewayresponse.header.Access-Control-Allow-Methods': '\'HEAD,GET,POST,PUT,PATCH,DELETE,ANY,OPTIONS\'',
                'gatewayresponse.header.Access-Control-Allow-Origin': '\'*\''
            }
            self.gateway_handler.delete_gateway_response('DEFAULT_4XX')
            self.gateway_handler.delete_gateway_response('DEFAULT_5XX')
            self.gateway_handler.create_gateway_response('DEFAULT_4XX', gateway_response_params)
            self.gateway_handler.create_gateway_response('DEFAULT_5XX', gateway_response_params)

    def __create_response(self, resource_id, method, response_code, status_code, response_parameters):
        error_regex = '^\\{{ "gatewayResponse": true, "status": "error", "type": "{0}", "userMessage": " " }}$'
        regex = error_regex.format(response_code).replace(' ', '(.|\\s)*')

        self.gateway_handler.create_method_response(resource_id, method, status_code, response_parameters)
        self.gateway_handler.create_integration_response(resource_id, method, status_code, response_parameters, regex, get_error_response_template())

    def create_resource(self, path):
        if self.get_resource_id(path):
            return

        # get tree of resources
        parts = path.split('/')[1:]

        parent_resource_id = self.get_resource_id('/')
        for i in range(len(parts) + 1):
            path_to_check = build_path(parts[:i])
            resource_id = self.get_resource_id(path_to_check)

            if not resource_id:
                parent_resource_id = self.gateway_handler.create_resource(parent_resource_id, parts[i-1])['id']
            else:
                parent_resource_id = resource_id

    def get_resource_id(self, path):
        resources = self.gateway_handler.get_resources()

        for r in resources:
            if r['path'] == path:
                return r['id']

        return None

    def deploy_api(self):
        self.gateway_handler.deploy(self.aws['stage'])
