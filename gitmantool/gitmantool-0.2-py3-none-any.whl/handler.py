import sys

from .version import get_version
from .settings import SettingsFile
from .github import GithubClient


def get_client():
    # check settings file and create if not exist
    config = SettingsFile()
    if not config.exist:
        config.create()
    # devuelve cliente del server que toca
    if config.server == "github.com":
        return GithubClient(config)
    else:
        sys.exit("Server not implemented")


def run_handler(args):
    client = get_client()

    if args['--version']:
        print(f"[i] Current version: {get_version()}")
    
    elif args['--list']:
        client.list_issues()
    
    elif args['--new']:
        client.new_issue([])
    
    elif args['--bug']:
        client.new_issue(['bug'])
     
    elif args['--show'] and args['<id>'] is not None:
        client.show_issue(args['<id>'])

    elif args['--close'] and args['<id>'] is not None:
        client.close_issue(args['<id>'])