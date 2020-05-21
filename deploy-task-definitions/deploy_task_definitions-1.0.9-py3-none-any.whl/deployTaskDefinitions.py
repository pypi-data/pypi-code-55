import sys, argparse
from .configManager import load_configs
from .ECSClient import ECSClient
from .EventsClient import EventsClient
from .taskDefinition import get_task_definition


def deploy(configs):
    for config in configs:
        print('Deploying: {}'.format(config['FAMILY']))
        ecs = ECSClient(config['REGION'])

        use_fargate = ("TASK_EXECUTION_MODE" in config and config["TASK_EXECUTION_MODE"] == "FARGATE")
        task = get_task_definition(config,use_fargate)
        task_definition_arn = ecs.register_task_definition(config, task, use_fargate)

        cluster_arn = ecs.get_cluster_arn(config['CLUSTER_NAME'])

        print('Task definition created: {} in cluster: {}'.format(task_definition_arn,cluster_arn))

        if 'CLOUDWATCH_RULE' in config:
            update_targets(config,cluster_arn,task_definition_arn,use_fargate)

        if 'SERVICE_NAME' in config:
            print('Updating ECS service: {}'.format(config['SERVICE_NAME']))
            ecs.update_service(config['CLUSTER_NAME'], config['SERVICE_NAME'],task_definition_arn)

        task_definitions_deleted = ecs.delete_old_task_definitions(config)
        print('Old task definition deleted: {}'.format(task_definitions_deleted))


def update_targets(config,cluster_arn,task_definition_arn, use_fargate):
    events_client = EventsClient(config['REGION'])
    subnets =  eval(config['TASK_SUBNETS']) if use_fargate else []
    securityGroups = eval(config['TASK_SECURITY_GROUPS']) if use_fargate else []

    update =  events_client.putTargets(config['FAMILY'],cluster_arn,config['CLOUDWATCH_RULE'], task_definition_arn, config['CLOUDWATCH_ROLE'], use_fargate, subnets, securityGroups)
    if update['FailedEntryCount']:
        sys.exit('Error updating cloudwatch event target')
    print('Cloudwatch event target updated')


def parse_args():
    parser = argparse.ArgumentParser(description='Deploy task definition to ECS')
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        help='config directory or file',
        required=True
    )
    return parser.parse_args()

def main():
    args = parse_args()
    configs = load_configs(args.config)
    deploy(configs)
