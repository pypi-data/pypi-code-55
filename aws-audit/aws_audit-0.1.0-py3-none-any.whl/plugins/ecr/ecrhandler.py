import json, os
from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class ecrhandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create ECR client
            self.ecr_client = session.client('ecr', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create ECR client', {'region': self.region})
        
        self.repositories = self.describe_repositories()

    def describe_repositories(self):
        repositories = []
        response = {}

        while True:

            try:
                if 'nextToken' in response:
                    response = self.ecr_client.describe_repositories(nextToken = response['NextToken'])
                else:
                    response = self.ecr_client.describe_repositories()

                repositories.extend(response['repositories'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call ECR describe_repositories', {'region': self.region})

            if 'nextToken' not in response:
                break

        return repositories
    
    def get_repository_policy(self, repository_name):
        
        response = {}        
        try:
            response = self.ecr_client.get_repository_policy(repositoryName=repository_name)
            
            return response

        except ClientError as e:
            if e.response["Error"]["Code"] == 'RepositoryPolicyNotFoundException':
                response['policyText'] = ''
                response['repositoryName'] = repository_name
                return response
            else:
                raise classify_error(self.logger, e, 'Failed to call ECR get_repository_policy', {'region': self.region})        

    def ecr_repository_exposed_to_everyone(self):
        failures = []
        for repository in self.repositories:
            try:
                repo_policy = self.get_repository_policy(repository['repositoryName'])                
                if repo_policy['policyText'] != '':
                    policy = json.loads(repo_policy['policyText'])
                    is_exposed = self.helper.is_policy_exposed_to_everyone(policy)
                    if is_exposed:
                        failures = self.helper.append_item_to_list(failures, 'ecr', repository['repositoryName'], repository['repositoryArn'] , self.region)
            except Exception as e:
                self.logger.error(f"Error while getting repository policy: {e}")

        return failures

    def ecr_cross_account_access_allowed(self):
        failures = []
        for repository in self.repositories:
            try:
                repo_policy = self.get_repository_policy(repository['repositoryName'])                
                if repo_policy['policyText'] != '':
                    policy = json.loads(repo_policy['policyText'])
                    is_caa_allowed = self.helper.is_policy_has_cross_account_access(policy)
                    if is_caa_allowed:
                        failures = self.helper.append_item_to_list(failures, 'ecr', repository['repositoryName'], repository['repositoryArn'] , self.region)
            except Exception as e:
                self.logger.error(f"Error while getting repository policy: {e}")

        return failures
