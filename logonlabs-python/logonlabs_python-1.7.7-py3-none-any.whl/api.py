import requests


def ping(url):
    r = requests.get(url+'/ping')
    return r


def getProviders(url, params):
    r = requests.get(url+'/providers', params=params)
    return r


def startLogin(url, params):
    r = requests.post(url+'/start', params=params)
    return r


def validateLogin(url, params, headers):
    r = requests.post(url+'/validate', params=params, headers=headers)
    return r


def redirectLogin(url, params):
    r = requests.get(url+'/redirect', params=params, allow_redirects=False)
    return r


def createEvent(url, params, headers):
    r = requests.post(url+'/events', params=params, headers=headers)
    return r


def updateEvent(url, params, headers):
    r = requests.patch(url+'/events/'+params['event_id'], params=params, headers=headers)
    return r

def refreshToken(url, params, headers):
    r = requests.post(url+'/refresh', params=params, headers=headers)
    return r
		
def revokeToken(url, params, headers):
    r = requests.post(url+'/revoke', params=params, headers=headers)
    return r