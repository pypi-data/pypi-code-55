import click
from .Environment import Environment
from vodi import Environments

class EnvCommand:
    """a command to manage available environments of vodi"""
    
    __not_implemented = 'Not implemented yet'

    def get(self, envName):
        return Environments.envs[envName]

    def getAll(self):
        return Environments.envs.values()

    def printAll(self):
        Environments.printAllEnvs()

    def print(self, environment):
        Environments.printEnv(environment)
    
    def create(self, environment):
        click.echo(self.__not_implemented)

    def delete(self, environment):
        click.echo(self.__not_implemented)

    def deleteAll(self):
        click.echo(self.__not_implemented)