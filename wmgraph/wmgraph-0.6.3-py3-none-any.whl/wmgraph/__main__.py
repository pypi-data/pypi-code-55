import os

from .api import MgraphApi
from .api.deltaiterator import GenericDeltaIterator

HOME = os.environ.get('HOME')
CFGDIR = os.path.join(HOME, '.config/wmssync')
STATEDIR = os.path.join(HOME, '.local/share/wmssync')

def main():
    print(f'testing {MgraphApi} {GenericDeltaIterator}')
    paramsfile = os.path.join(CFGDIR, 'config.json')
    api = MgraphApi(params=paramsfile)
    # url = 'https://graph.microsoft.com/v1.0/groups/delta?$select=displayName,description,members'
    url = 'https://graph.microsoft.com/v1.0/users/delta?$select=displayName,userPrincipalName'
    iterator = api.get_deltaiterator(url, deltalink=None)
    for item in iterator:
        print(item)
    print(f"next iteration: {iterator.get_next_url()}")
    # for user in api.list_users():
    #     print(user)

if __name__=='__main__':
    main()