from awsdeployer.__util import *
import boto3


class IamHandler:
    def __init__(self, aws_config):
        self.aws = aws_config
        self.iam_client = boto3.client('iam',
                                       region_name=self.aws['region'],
                                       aws_access_key_id=self.aws['access_key'],
                                       aws_secret_access_key=self.aws['secret_key'])

        self.iam_resource = boto3.resource('iam',
                                           region_name=self.aws['region'],
                                           aws_access_key_id=self.aws['access_key'],
                                           aws_secret_access_key=self.aws['secret_key'])

    def create_lambda_role(self, function_name):
        role_policy = '''{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Principal": {
                "Service": "lambda.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
            }
          ]
        }'''

        execution_policy = '''{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                        "logs:DescribeLogStreams"
                    ],
                    "Resource": [
                        "arn:aws:logs:*:*:*"
                    ]
                }
            ]
        }'''

        execution_role_name = 'execution-role-lambda-' + function_name + '-' + random_string(8)
        execution_policy_name = 'execution-policy-lambda-' + function_name + '-' + random_string(8)

        role = self.iam_client.create_role(
            RoleName=execution_role_name,
            AssumeRolePolicyDocument=role_policy
        )

        policy = self.iam_client.create_policy(
            PolicyName=execution_policy_name,
            PolicyDocument=execution_policy
        )

        result = self.iam_resource.Role(execution_role_name).attach_policy(PolicyArn=policy['Policy']['Arn'])

        return role['Role']['Arn']
