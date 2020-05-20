import requests
from bs4 import BeautifulSoup

class Search:

    def __init__(self):
        self.searchType = "general"
        self.searchOptions = {"e": "", "yearFrom": "", \
                            "yearTo": "", "language": "", \
                            "extension": "", "page":"1", \
                            "order":""}
        self.searchResults = "books"
        self.input = ""

    def nextPage(self):
        '''Goes to next page'''
        self.searchOptions["page"] = str(int(self.searchOptions["page"])+1)

    def previousPage(self):
        '''Goes to previous page'''
        if self.searchOptions["page"] != "1":
            self.searchOptions["page"] = str(int(self.searchOptions["page"])-1)
        else:
            return 1

    def updateSearchOptions(self):
        '''Depending on searchType and searchResults, updates appropriately
        searchOptions
        '''
        if self.searchType == "general":
            self.searchOptions.pop("matchPhrase", None)
        else: 
            self.searchOptions["matchPhrase"] = ""
    
        if self.searchResults == "books":
            self.searchOptions["language"] = ""
            self.searchOptions["extension"] = ""
        else:
            self.searchOptions.pop("language", None)
            self.searchOptions.pop("extension", None)
            
    def executeSearch(self):
        '''Executes get request and returns response'''
        if self.searchResults == "books":
            url = "http://b-ok.cc"
        else:
            url = "http://booksc.xyz"

        r = requests.get(url+"/s/"+self.input, params=self.searchOptions)
        return r


    def getResults(self):
        '''Fetches search results. Returns a list of books
        '''
        r = self.executeSearch()
        soup = BeautifulSoup(r.text, "html.parser")
        match = soup.find_all(class_="resItemBox")
        counter = 1
        results=[]
        for e in match:
            title = e.find(itemprop="name")
            author = e.find(class_="authors")
            year = e.find(class_="bookProperty property_year")
            language = e.find(class_="bookProperty property_language")
            fileInfo = e.find(class_="bookProperty property__file")
            link = e.find("a", href=True)
            link = link["href"]

            if self.searchResults == "books":
                fullLink = "https://b-ok.cc" + link
            else:
                fullLink = "booksc.xyz" + link
            
            title = isNone(title)
            author = isNone(author)
            year = isNone(year)
            language = isNone(language)
            fileInfo = isNone(fileInfo)
            
            book = Book(title,author,year,language,fileInfo,fullLink)
            results += [book]
        
        return results

    def reset(self):
        '''Clears the search and resets to default options'''
        self.searchType = "general"
        self.searchOptions = {"e": "", "yearFrom": "", \
                            "yearTo": "", "language": "", \
                            "extension": "", "page":"1", \
                            "order":""}
        self.searchResults = "books"
        self.input = ""
        

def isNone(e):
    if e != None:
        return "".join(e.text.splitlines())
    else:
        return ""

class Book:
    
    def __init__(self,title,author,year,language,size,link):
        self.title = title
        self.author = author
        self.year = year
        self.language = language
        self.size = size
        self.link = link
        self.dlLink = None

    def __str__(self):
        
        return " / ".join([self.title,self.author,self.year,\
                self.language,self.size])

    def getDetails(self):
        '''Returns more specific info about the book. The info is retrieved by the
        link attribute
        '''
        r = requests.get(self.link)

        soup = BeautifulSoup(r.text, "html.parser")
        # for some reason, bookProperty also shows properties from other books
        # the line below prevents this
        soup = soup.find(class_="row cardBooks")
        match = soup.find_all(class_="bookProperty")
        
        results = ""
        for e in match:
            results += "".join(e.text.splitlines())
            results += "\n"

        # this makes writing the category easier for some books
        results = results.replace("\\\\", " \\ ")
        return results
    

