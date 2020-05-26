######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: htmldoc.py
### Description: Formatting of HTML documents
### Last Modified: 24 May 2020
######################################################################

### import modules

import sys
import textwrap

if sys.version_info[0]==2:
    from HTMLParser import HTMLParser

elif sys.version_info[0]==3:
    from html.parser import HTMLParser

else:
    raise Exception('Unsupported version of Python')



######################################################################
### Class: HTMLText - Convert HTML to text
######################################################################

class HTMLText(HTMLParser):

    ### __init__

    def __init__(self):
        HTMLParser.__init__(self)
        self.tags=['doc']
        self.currentpar=''
        self.result=''
        self.indentation=4

    ### handle_starttag - trap starttag

    def handle_starttag(self,tag,attrs):
        self.tags.append(tag)


    ### handle_endtag - trap endtag

    def handle_endtag(self,tag):

        if tag!=self.tags[-1]:
            print('tag error')
            return

        self.tags.pop()

        if 'body' in self.tags:

            if tag=='h1':
                self.currentpar=self.currentpar.strip().replace('\n',' ')
                self.currentpar+='\n'+'='*len(self.currentpar)
                self.result+='\n%s\n' %self.currentpar
                self.currentpar=''

            if tag=='h2':
                self.currentpar=self.currentpar.strip().replace('\n',' ').upper()
                self.result+='\n%s\n' %self.currentpar
                self.currentpar=''

            elif tag=='p':
                self.currentpar=textwrap.fill(self.currentpar.strip().replace('\n',' '),75)
                self.result+='\n%s\n' %self.indent(self.currentpar)
                self.currentpar=''

            elif tag=='pre':
                self.currentpar=self.currentpar.strip()
                self.result+='\n%s\n' %self.indent(self.currentpar)
                self.currentpar=''
                

    ### handle_data - capture data

    def handle_data(self,data):
        if 'body' in self.tags:
            self.currentpar+=data


    ### handle_entityref

    def handle_entityref(self,name):
        if 'body' in self.tags and 'pre' in self.tags:
            self.currentpar+='&'+name


    ### indent

    def indent(self,s):
        return '\n'.join([' '*self.indentation+x for x in s.split('\n')])


    
