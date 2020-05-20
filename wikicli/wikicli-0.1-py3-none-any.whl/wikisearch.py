import argparse
import requests
from bs4 import BeautifulSoup


class Wiki:

    DE_SEARCH = 'https://de.wikipedia.org/wiki/'
    EN_SEARCH = 'https://en.wikipedia.org/wiki/'
    FR_SEARCH = 'https://fr.wikipedia.org/wiki/'

    def __init__(self, search, language='EN'):

        self.search = search
        self.language = language
        self.paragraphs = []
        self.article = ''

    def search_meaning(self):

        if  self.language == 'EN':
            link = Wiki.EN_SEARCH

        elif self.language == 'DE':
            link = Wiki.DE_SEARCH

        elif self.language == 'FR':
            link = Wiki.FR_SEARCH

        if self.search == None:
            print('[!] I don\'t know whar you are looking for.\n')
        else:
            r = requests.get(link + self.search)
            html = BeautifulSoup(r.text, 'html.parser')

            title = html.select('#firstHeading')[0].text
            self.paragraphs = html.select('p')

    def print_important(self):

        ''' Print out the short
            explanation which is
            always on top of wiki
            articles;
        '''

        pass

    def print_all(self):

        for p in self.paragraphs:
            print(p.text)

        return


if __name__ == '__main__':

    pass
