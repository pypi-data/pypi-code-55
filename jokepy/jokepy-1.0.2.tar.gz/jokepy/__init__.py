#Api Documentation : https://sv443.net/jokeapi/v2


import requests
#api response is fetched using requests


#custom exceptions

class InvalidCategoryException(ValueError):
    pass

class InvalidFlagException(ValueError):
    pass

class InvalidTypeException(ValueError):
    pass

class InvalidIdRangeException(ValueError):
    pass

class Jokepy:
    
    #categories in sv443 Joke Api
    defCategories = ['Programming','Miscellaneous','Dark']
    
    #blacklist tags
    defBlackListTags = ['nsfw','religious','political','racist','sexist']

    #types
    defTypes = ['single','twopart']

    #parameters used to build request
    params = dict()

    #default url
    urlreq = 'https://sv443.net/jokeapi/v2/joke/'

    #initialising parameters for the api
    def __init__(self,categories=[],flags = [],idRange=[],type = None,searchstring =None):
        self.categories = categories
        self.flags = flags
        self.idRange = idRange
        self.type = type
        self.searchstring = searchstring
    
    def __repr__(self):
        return '{self.__class__.__name__}({self.categories},{self.flags},{self.idRange},{self.type},{self.searchstring})'.format(self=self)
    
    def __str__(self):
        return '({self.categories},{self.flags},{self.idRange},{self.type},{self.searchstring})'.format(self=self)



    #function to get joke
    def getjoke(self):

        #adding categories to request url
        if len(self.categories) == 0:
            self.urlreq += "Any"
        else:
            for category in self.categories:
                if category not in Jokepy.defCategories:

                    #raise exception if the category is not valid
                    error_message = 'Invalid Category : {} , Available Categories : {}'.format(category,Jokepy.defCategories)
                    raise InvalidCategoryException(error_message)
                else:
                    #building the url if the category is valid
                    self.urlreq += category + ","
            #removing the last comma
            self.urlreq = self.urlreq[:-1]

        #..... parameters ....(blackListflags)
        if len(self.flags) != 0:
            self.params['blacklistFlags'] = ""
            for flag in self.flags:
                
                if flag not in Jokepy.defBlackListTags:

                    #raise exception if flag is not valid
                    error_message = 'Invalid Flag : {} , Available Flags : {}'.format(flag,Jokepy.defBlackListTags)
                    raise InvalidFlagException(error_message)
                else:

                    self.params['blacklistFlags'] += flag + ","

            #removing the last comma
            self.params['blacklistFlags'] = self.params['blacklistFlags'][:-1]
        
        if self.type is not None:
            if self.type not in Jokepy.defTypes:

                error_message = 'Invalid Type : {} , Available Types : {}'.format(self.type,Jokepy.defTypes)
                raise InvalidTypeException(error_message)
            else:
                self.params['type'] = self.type

        
        #-----idrange----
        if len(self.idRange) != 0:

            if len(self.idRange) != 2:
                #minimum number of elements in the idRange list should be 2
                error_message = 'idRange should be a list with two numbers'
                raise InvalidIdRangeException(error_message)

            if self.idRange[0] < 0 or self.idRange[1] < 0 or self.idRange[1] < self.idRange[0]:

                error_message = 'idRange error . Please check if the value is negative or the first value is greater than the second'
                raise InvalidIdRangeException(error_message)
            else:
                self.params['idRange'] = ""
                for rng in self.idRange:
                    self.params['idRange'] += str(rng) + ","
                #removing the last comma
                self.params['idRange'] = self.params['idRange'][:-1]
        
        #-----searchstring---
        if self.searchstring is not None:
            self.params['contains'] = self.searchstring
        
        try:
            
            #request sv443 jokeapi url
            r = requests.get(self.urlreq , params=self.params)
            print(r.url)
        except Exception as e:
            #return error if the request 
            return {'error' : 'Request Failed','errorinfo': str(e)}

        #return json response
        return r.json()














        
                    
            


