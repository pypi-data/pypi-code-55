import boto3

class EventsClient:

    def __init__(self, region):
        self.client = boto3.client('events',region_name=region)

    def list_targets_by_rule(self,rule):
        response = self.client.list_targets_by_rule(
            Rule=rule
        )
        return response

    def putTargets(self,id,cluster_arn, cloudwatch_rule, task_definition_arn, roleArn, useFargate, subnets=[], securityGroups=[]):
        ecsParameters = {
            'TaskDefinitionArn': task_definition_arn,
            'TaskCount': 1
        }
        if useFargate:
            fargateParameters = {
                'NetworkConfiguration' : {
                    'awsvpcConfiguration': {
                        'Subnets': subnets,
                        'SecurityGroups': securityGroups,
                        'AssignPublicIp': 'ENABLED'
                    }
                },
                'LaunchType':  'FARGATE'

            }
            ecsParameters.update(fargateParameters)
        response = self.client.put_targets(
            Rule=cloudwatch_rule,
            Targets=[
                {
                    'Id': "{}-event-target".format(id),
                    "Arn": cluster_arn,
                    "RoleArn": roleArn,
                    'EcsParameters': ecsParameters
                }
            ]
        )
        return response
