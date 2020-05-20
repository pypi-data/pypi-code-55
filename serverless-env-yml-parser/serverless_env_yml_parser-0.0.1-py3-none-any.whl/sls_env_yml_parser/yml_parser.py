import re
import os


def exclude(variable, omissions):
    if variable in omissions:
        return True
    return False


yml_regex = re.compile(r"""^([^\s:]+):(?:[\s"']*)(.+?)(?:[\s"']*)$""")


def parse_env_yml(yml_file, omissions=[]):
    """ 
    param yml_file:
    a path to serverless.env.yml

    param omissions:
    a list of keys to exclude from adding to environmental variables, 
    by default it includes "default", "<<"
    
    """
    variables = {}
    with open(yml_file) as ins:
        for line in ins:
            match = yml_regex.match(line.lstrip())
            if match is not None:
                variables[match.group(1)] = match.group(2)

    for variable in variables:
        if not exclude(variable, ["default", "<<"] + omissions):
            os.environ[variable] = variables[variable]
