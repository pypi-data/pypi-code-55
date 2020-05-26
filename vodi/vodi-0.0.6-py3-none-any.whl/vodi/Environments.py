from .Environment import Environment
import click
import os

_dev = Environment("dev", "https://openshift.dxl-pre.vodafone.com:8443", "beapp")
_test = Environment("test", "https://openshift.dxl-pre.vodafone.com:8443", "beapp-pre")
_iat = Environment("iat", "https://openshift.dxl-iat.vodafone.it:8443", "beapp")
_bs = Environment("bs", "https://openshift.dxl.vodafone.it:8443", "beapp-bs")
_prod = Environment("prod", "https://openshift.dxl.vodafone.it:8443", "beapp")
envs = {
    "dev" : _dev,
    "test" : _test, 
    "iat" : _iat,
    "bs" : _bs,
    "prod" : _prod
}


def printEnv(environment):
    click.echo('name: %s' % environment.name)
    click.echo('url: %s' % environment.url)
    click.echo('namespace: %s' % environment.namespace)
    click.echo('')
#   click.echo('deployments: %s' % environment.deployments) deployments parsing not implemented yet
    os.system('oc get dc -o custom-columns=DEPLOYMENT:.metadata.name,IMAGE:.spec.template.spec.containers[0].image -n %s' % environment.namespace)
    click.echo('---')

def printAllEnvs():
    click.echo('{:<10}\t{:<50}\t{:<10}'.format('NAME','URL','NAMESPACE'))
    for e in envs.values():
        click.echo("{:<10}\t{:<50}\t{:<10}".format(e.name, e.url, e.namespace))
