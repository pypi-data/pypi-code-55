import boto3


class GatewayHandler:
    """This class provides a low-level API Gateway interface via boto3 with no user-processing"""
    def __init__(self, aws_config):
        self.aws = aws_config
        self.client = boto3.client('apigateway',
                                   region_name=self.aws['region'],
                                   aws_access_key_id=self.aws['access_key'],
                                   aws_secret_access_key=self.aws['secret_key'])

        self.lambda_client = boto3.client('lambda',
                                          region_name=self.aws['region'],
                                          aws_access_key_id=self.aws['access_key'],
                                          aws_secret_access_key=self.aws['secret_key'])

    # def create_api(self, name):
    #     response = self.client.create_rest_api(
    #         name=name,
    #         endpointConfiguration={
    #             'types': [
    #                 'REGIONAL'
    #             ]
    #         }
    #     )
    #
    #     if response['ResponseMetadata']['HTTPStatusCode'] != 201:
    #         raise RuntimeError

    def deploy(self, stage):
        response = self.client.create_deployment(
            restApiId=self.aws['api_id'],
            stageName=stage
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 201:
            raise RuntimeError

        return response

    def create_resource(self, parent, path):
        response = self.client.create_resource(
            restApiId=self.aws['api_id'],
            parentId=parent,
            pathPart=path
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 201:
            raise RuntimeError

        return response

    def create_method(self, resource_id, method, request_parameters={}):
        response = self.client.put_method(
            restApiId=self.aws['api_id'],
            resourceId=resource_id,
            httpMethod=method,
            authorizationType='NONE',
            requestParameters=request_parameters
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 201:
            raise RuntimeError

        return response

    def create_lambda_integration(self, resource_id, method, function_name, template):
        unique_permission_id = 'apigateway-exec-{0}-{1}-{2}-{3}'.format(self.aws['region'], self.aws['account_id'], self.aws['api_id'], method)

        try:
            response = self.lambda_client.add_permission(
                FunctionName=function_name,
                StatementId=unique_permission_id,
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn='arn:aws:execute-api:{0}:{1}:{2}/*/{3}/*'.format(self.aws['region'], self.aws['account_id'], self.aws['api_id'], method)
            )

            if response['ResponseMetadata']['HTTPStatusCode'] != 201:
                raise RuntimeError

        except Exception as e:  # can't reference actual boto exception here
            if str(type(e)) == '<class \'botocore.errorfactory.ResourceConflictException\'>':
                pass
            else:
                raise e

        # create the integration with the lambda
        uri = 'arn:aws:apigateway:{0}:lambda:path/2015-03-31/functions/arn:aws:lambda:{0}:{1}:function:{2}/invocations'.format(self.aws['region'], self.aws['account_id'], function_name)
        response = self.client.put_integration(
            restApiId=self.aws['api_id'],
            resourceId=resource_id,
            httpMethod=method,
            type='AWS',
            integrationHttpMethod='POST',
            passthroughBehavior='NEVER',
            uri=uri,
            requestTemplates={
                'application/json': template
            },
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 201:
            raise RuntimeError

        return response

    def create_mock_integration(self, resource_id, method):
        response = self.client.put_integration(
            restApiId=self.aws['api_id'],
            resourceId=resource_id,
            httpMethod=method,
            type='MOCK',
            requestTemplates={
                'application/json': '{"statusCode": 200}'
            },
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 201:
            raise RuntimeError

        return response

    def create_integration_response(self, resource_id, method, status_code, parameters, regex_pattern, template):
        response = self.client.put_integration_response(
            restApiId=self.aws['api_id'],
            resourceId=resource_id,
            httpMethod=method,
            statusCode=status_code,
            selectionPattern=regex_pattern,
            responseParameters=parameters,
            responseTemplates={
                'application/json': template
            }
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 201:
            raise RuntimeError

        return response

    def create_method_response(self, resource_id, method, status_code, parameters):
        # only need the keys from the response parameters
        response_parameters = {}
        for parameter in parameters.keys():
            response_parameters[parameter] = True

        # this AWS method is not idempotent
        response = self.client.put_method_response(
            restApiId=self.aws['api_id'],
            resourceId=resource_id,
            httpMethod=method,
            statusCode=status_code,
            responseParameters=response_parameters,
            responseModels={
                'application/json': 'Empty'
            }
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 201:
            raise RuntimeError

        return response

    def create_gateway_response(self, response_type, parameters):
        response = self.client.put_gateway_response(
            restApiId=self.aws['api_id'],
            responseType=response_type,
            responseParameters=parameters,
            responseTemplates={
                'application/json': '{"message":$context.error.messageString}'
            }
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 201:
            raise RuntimeError

        return response

    def delete_gateway_response(self, response_type):
        try:
            response = self.client.delete_gateway_response(
                restApiId=self.aws['api_id'],
                responseType=response_type
            )

            if not 200 < response['ResponseMetadata']['HTTPStatusCode'] < 299:
                raise RuntimeError

            return response
        except self.client.exceptions.NotFoundException:
            return None

    def has_method(self, resource_id, method):
        try:
            response = self.client.get_method(
                restApiId=self.aws['api_id'],
                resourceId=resource_id,
                httpMethod=method
            )

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True
            else:
                raise RuntimeError
        except self.client.exceptions.NotFoundException:
            return False

    def delete_method(self, resource_id, method):
        response = self.client.delete_method(
            restApiId=self.aws['api_id'],
            resourceId=resource_id,
            httpMethod=method
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 204:
            raise RuntimeError

    def get_resources(self):
        response = self.client.get_resources(restApiId=self.aws['api_id'], limit=500)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise RuntimeError

        return response['items']
