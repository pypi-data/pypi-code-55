from atlassian import Bitbucket
import click

def printProject(project):
    bitbucket = __connect()
    p = bitbucket.project(project)
    click.echo('name: %s' % p['key'])
    click.echo('description: %s' % p.get('description', ''))
    click.echo('url: %s' % p['links']['self'][0]['href'])
    click.echo('')
    __printRepos(bitbucket, project)

def printAllProjects():
    bitbucket = __connect()
    click.echo('{:<10}\t{:<40}\t{:<50}'.format('NAME','DESCRIPTION','URL'))
    project_list = bitbucket.project_list()
    for p in project_list:
        click.echo("{:<10}\t{:<40}\t{:<50}".format(p['key'],p.get('description', ''), p['links']['self'][0]['href']))
  
def __printRepos(bitbucket , project):
    click.echo('{:<30}\t{:<10}\t{:<10}'.format('NAME','STATE','URL'))
    for r in bitbucket.repo_list(project):
        url = ''
        for l in r['links']['clone']:
            if l['name'] == "http":
                url = l['href']
        click.echo("{:<30}\t{:<10}\t{:<100}".format( r['slug'], r['state'], url))

def __connect():
    username = click.prompt('Enter your bitbucket username')
    password = click.prompt('Enter your bitbucket password', hide_input=True)
    bitbucket = Bitbucket(url="http://it1900yr.it.sedc.internal.vodafone.com:8443", username=username, password=password)
    return bitbucket