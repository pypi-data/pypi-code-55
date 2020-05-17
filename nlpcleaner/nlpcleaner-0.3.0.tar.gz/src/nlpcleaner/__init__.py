import os
import regex as re,string
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import cld3
import logging

log = logging.getLogger(__name__)
module_path = os.path.dirname(__file__)

# Set nltk folder
nltk.data.path.append(module_path + "/data/nltk")

supported_lang = { 'ar': { 'name': 'arabic', 'stemmer': False, 'stopwords': True },
                   'az': { 'name': 'azerbaijani', 'stemmer': False, 'stopwords': True },
                   'da': { 'name': 'danish', 'stemmer': True, 'stopwords': True },
                   'nl': { 'name': 'dutch', 'stemmer': True, 'stopwords': True },
                   'en': { 'name': 'english', 'stemmer': True, 'stopwords': True },
                   'fi': { 'name': 'finnish', 'stemmer': True, 'stopwords': True },
                   'fr': { 'name': 'french', 'stemmer': True, 'stopwords': True },
                   'de': { 'name': 'german', 'stemmer': True, 'stopwords': True },
                   'el': { 'name': 'greek', 'stemmer': False, 'stopwords': True },
                   'hu': { 'name': 'hungarian', 'stemmer': True, 'stopwords': True},
                   'id': { 'name': 'indonesian', 'stemmer': False, 'stopwords': True },
                   'it': { 'name': 'italian', 'stemmer': True, 'stopwords': True },
                   'kk': { 'name': 'kazakh', 'stemmer': False, 'stopwords': True },
                   'ne': { 'name': 'nepali', 'stemmer': False, 'stopwords': True },
                   'nn': { 'name': 'norwegian', 'stemmer': True, 'stopwords': True },
                   'pt': { 'name': 'portuguese', 'stemmer': True, 'stopwords': True },
                   'ro': { 'name': 'romanian', 'stemmer': True, 'stopwords': True },
                   'ru': { 'name': 'russian', 'stemmer': True, 'stopwords': True },
                   'sl': { 'name': 'slovene', 'stemmer': False, 'stopwords': True },
                   'es': { 'name': 'spanish', 'stemmer': True, 'stopwords': True },
                   'sv': { 'name': 'swedish', 'stemmer': True, 'stopwords': True },
                   'tg': { 'name': 'tajik', 'stemmer': False, 'stopwords': True },
                   'tr': { 'name': 'turkish', 'stemmer': False, 'stopwords': True } }

lemmatizer = WordNetLemmatizer()
stop_words = {}
stemmers = {}

for key in supported_lang:
    if supported_lang[key]['stopwords'] == True: stop_words[key] = set(stopwords.words(supported_lang[key]['name']))
    if supported_lang[key]['stemmer'] == True: stemmers[key] = SnowballStemmer(supported_lang[key]['name'])

class TextCleaner:
    def __init__(self, corpus, language = None):
      self.corpus = corpus
      if language is None:
        self.language = cld3.get_language(self.corpus).language
        log.debug("Detected language: %s" % self.language)
      else:
         self.language = language

    def clean(self):
      cleaned = self.__lower_all()\
                    .__clear_blank_lines()\
                    .__strip_all()\
                    .__remove_urls()\
                    .__strip_html_tags()\
                    .__remove_script()\
                    .__remove_numbers()\
                    .__remove_symbols()\
                    .__remove_stopwords()\
                    .__lemming_or_stemming()\
                    .__formatting().corpus
      return cleaned

    def tokenized(self):
        words = filter(lambda x: len(x)>0, self.corpus.split(' '))
        return words

    def lower_all(self):
        return self.__lower_all()\
                   .__formatting().corpus

    def clear_blank_lines(self):
        return self.__clear_blank_lines()\
                   .__formatting().corpus

    def strip_all(self):
        return self.__strip_all()\
                   .__formatting().corpus

    def remove_numbers(self):
        return self.__remove_numbers()\
                   .__formatting().corpus

    def remove_symbols(self):
        return self.__remove_symbols()\
                   .__formatting().corpus

    def remove_urls(self):
        return self.__remove_urls()\
                   .__formatting().corpus

    def strip_html_tags(self):
        return self.__strip_html_tags()\
                   .__formatting().corpus

    def remove_script(self):
        return self.__remove_script()\
                   .__formatting().corpus

    def remove_stopwords(self):
        return self.__remove_stopwords()\
                   .__formatting().corpus

    def stemming(self):
        return self.__stemming()\
                   .__formatting().corpus

    def lemming(self):
        return self.__lemming()\
                   .__formatting().corpus

    # converts each character to lowercase
    def __lower_all(self):
        self.corpus = ''.join([each.lower() for each in self.corpus])
        return self

    # removes all the blank line from the text file
    def __clear_blank_lines(self):
        self.corpus = re.sub(r'\r\n', ' ', self.corpus)
        return self

    # it removes ".\n" from every element by default
    # can be used to strip by second argument
    def __strip_all(self):
        self.corpus = re.sub(r'\n', ' ', self.corpus)
        return self

    # removes numbers detected anywhere in the data
    def __remove_numbers(self):
        self.corpus = re.sub(r'[0-9]+',' ',self.corpus)
        return self

    # removes punctuations detected anywhere in the data
    def __remove_symbols(self):
        self.corpus = re.sub(r'[^\w\s]|_',' ',self.corpus)
        return self

    # removes stop words if detected language is supported
    def __remove_stopwords(self):
        log.debug(supported_lang.get(self.language))
        if type(supported_lang.get(self.language)) != type(None):
            log.debug("stopwords present for %s" % self.language)
            self.corpus = ' '.join([w for w in self.corpus.split() if not w in stop_words[self.language]])
        else:
            log.debug("stopwords not present for %s" % self.language)
        return self

    # removes urls and return a list of list of words
    def __remove_urls(self):
        self.corpus = re.sub(r'\b(?:(?:https?|ftp)://)?\w[\w-]*(?:\.[\w-]+)+\S*', ' ', self.corpus)
        return self

    # strip html tags
    def __strip_html_tags(self):
        self.corpus = re.sub(r'<[^>]+>', ' ', self.corpus)
        return self

    # removes script blocks
    def __remove_script(self):
        self.corpus = re.sub(r'<script(.*)</script>', '', self.corpus)
        return self

    # apply lemming if content is in english otherwise apply stemming
    def __lemming_or_stemming(self):
        if self.language == 'en':
            self.lemming()
        else:
            log.debug("lemming is not available for %s but we don't apply stemming!" % self.language)
        return self

    # reduces each word to its stem work like, dogs to dog
    def __stemming(self):
        if supported_lang.get(self.language) != None and supported_lang.get(self.language)['stemmer']:
            words = self.tokenized()
            stem_sentence=[]
            for word in words:
                stem_sentence.append(stemmers[self.language].stem(word))
                stem_sentence.append(' ')
            self.corpus = ''.join(stem_sentence)
        else:
            log.debug("stemming not available for %s" % self.language)
        return self

    # gets the root word for each word
    def __lemming(self):
        words = self.tokenized()
        lem_sentence=[]
        for word in words:
            lem_sentence.append(lemmatizer.lemmatize(word))
            lem_sentence.append(' ')
        self.corpus = ''.join(lem_sentence)
        return self

    # apply common format to all responses
    # - remove double spaces
    def __formatting(self):
        self.corpus = re.sub(r'\s\s+',' ',self.corpus).strip()
        return self
