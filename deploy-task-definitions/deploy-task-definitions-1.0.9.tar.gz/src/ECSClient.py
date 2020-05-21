import boto3

class ECSClient:

    def __init__(self, region):
        self.client = boto3.client('ecs',region_name=region)

    def get_task_definitions(self,family):
        response = self.client.list_task_definitions(
            familyPrefix = family,
            sort = "DESC"
        )
        return response['taskDefinitionArns']

    def register_task_definition(self, config, task_definition, useFargate):
        placementConstraints = []
        if 'INSTANCE_CONSTRAINTS' in  config:
            placementConstraints = [{
                "expression": "attribute:ecs.instance-type in {}".format(config['INSTANCE_CONSTRAINTS']),
                "type": "memberOf"
            }]


        if useFargate:
            response = self.client.register_task_definition(
                family = config['FAMILY'],
                taskRoleArn = config['TASK_ROLE_ARN'],
                containerDefinitions = task_definition,
                placementConstraints = placementConstraints,
                executionRoleArn = config['TASK_EXECUTION_ROLE_ARN'],
                networkMode =  'awsvpc',
                requiresCompatibilities =  ["FARGATE"],
                cpu = config["TASK_CPU"],
                memory = config["TASK_MEMORY"],
            )
        else:
            response = self.client.register_task_definition(
                family = config['FAMILY'],
                taskRoleArn = config['TASK_ROLE_ARN'],
                containerDefinitions = task_definition,
                placementConstraints = placementConstraints,
                executionRoleArn = config['TASK_EXECUTION_ROLE_ARN'],
            )


        return response['taskDefinition']['taskDefinitionArn']

    def delete_old_task_definitions(self,config,task_to_keep=3):
        task_definitions = self.get_task_definitions(config['FAMILY'])
        task_definitions_to_delete = task_definitions[task_to_keep:]
        deleted_arns = []
        for task in task_definitions_to_delete:
            response =  self.client.deregister_task_definition(taskDefinition=task)
            deleted_arns.append(response['taskDefinition']['taskDefinitionArn'])
        return deleted_arns

    def update_service(self,cluster_name, service_name, task_definition_arn):
        return self.client.update_service(
            cluster=cluster_name,
            service=service_name,
            taskDefinition=task_definition_arn
        )

    def get_cluster_arn(self,cluster_name):
        return self.client.describe_clusters(
            clusters=[
                cluster_name
            ]
        )['clusters'][0]['clusterArn']
