import requests
class SharedCountApi:

    DOMAIN = 'sharedcount.com'

    def __init__(self, apiToken,subDomain = 'api'):
        self.apiToken = apiToken
        self.url = 'https://' + subDomain + '.' + SharedCountApi.DOMAIN + '/v1.0'

    def getApiToken(self):
        return self._apiToken

    def setApiToken(self, value):
        if not isinstance(value, str):
            raise ValueError('Api token must be a string')
        self._apiToken = value
        
    def getUrl(self):
        return self._url

    def setUrl(self, value):
        self._url = value
        
    def get(self, urlToCheck):
        if not isinstance(urlToCheck, str):
            raise ValueError('Url must be a string')
        response = requests.get(self._url+'?apikey=' + self._apiToken + '&url=' + urlToCheck)
        json = response.json()
        return json

    def quota(self):
        response = requests.get(self._url+'/quota?apikey=' + self._apiToken )
        json = response.json()
        return json

    def usage(self):
        response = requests.get(self._url+'/usage?apikey=' + self._apiToken )
        json = response.json()
        return json

    def getDomainWhiteList(self):
        response = requests.get(self._url+'/domain_whitelist?apikey=' + self._apiToken )
        json = response.json()
        return json

    def status(self):
        response = requests.get(self._url+'/status')
        json = response.json()
        return json

    def bulkPost(self, urlsToCheck):
        if not isinstance(urlsToCheck, list):
            raise ValueError('Array must be provided')
        urlsToCheck = '\n'.join([str(elem) for elem in urlsToCheck]) 
        response = requests.post(self._url+'/bulk?apikey=' + self._apiToken, data = urlsToCheck)
        json = response.json()
        return json
    
    def bulkGet(self, bulkId):
        if not isinstance(bulkId, str):
            raise ValueError('Bulk id must be a string')
        response = requests.get(self._url+'/bulk?apikey=' + self._apiToken + '&bulk_id=' + bulkId)
        json = response.json()
        return json

    apiToken = property(getApiToken, setApiToken)
    url = property(getUrl, setUrl)
    
			
			