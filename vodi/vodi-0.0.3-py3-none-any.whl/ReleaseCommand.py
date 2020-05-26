import click

class ReleaseCommand:
    """a command to release vodafone digital services to openshift"""
    
    __not_implemented = 'Not implemented yet'
    
    def doRelease(self):
        click.echo(self.__not_implemented)
    
    def doRollback(self):
        click.echo(self.__not_implemented)

    def get(self, release):
        click.echo(self.__not_implemented)

    def getAll(self):
        click.echo(self.__not_implemented)
