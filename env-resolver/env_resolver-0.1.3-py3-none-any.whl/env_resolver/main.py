import os, json
import boto3

def generate_parameter_map(env, prefix=None):
    result = {}
    for key, value in env.items():
        if prefix is not None:
            if value.startswith(prefix):
                result[value[len(prefix):]] = key
        else:
            result[value] = key
    return result

def translate_ssm_parameters(raw_parameters):
    client =boto3.client('ssm')
    parameters = generate_parameter_map(raw_parameters)
    values = client.get_parameters(
        Names=list(parameters),
        WithDecryption=True
    )['Parameters']

    result = {}
    for parameter in values:
        result[parameters[parameter['Name']]] = parameter['Value']

    return result

def translate_secretsmanager_secret(secret_id, version_id=None, json_value=True):
    client = boto3.client('secretsmanager')
    args = dict(SecretId=secret_id)

    if version_id is not None:
        args['VersionId'] = version_id

    value = client.get_secret_value(**args)['SecretString']

    if json_value:
        value = json.loads(value)
    
    return value

def resolve_parameters(parameter_type, parameter_value):
    if parameter_type == 'secretsmanager':
        return translate_secretsmanager_secret(**parameter_value)
    elif parameter_type == 'ssm':
        return translate_ssm_parameters(parameter_value)
    else:
        raise ValueError(f'{parameter_type} is not a supported parameter type')

def resolve(parameter_type, parameter_value, set_environment_variables=True):
    parameters = resolve_parameters(parameter_type, parameter_value)

    if set_environment_variables:
        if parameter_type == 'secretsmanager':
            if not parameter_value.get('json_value', True):
                return parameters

        for key, value in parameters.items():
            os.putenv(key, value)
    
    return parameters
