import json
from pathlib import Path
import PyPDF2
import re
import nltk
import heapq
import networkx as nx
from nltk.cluster.util import cosine_distance
from nltk.corpus import stopwords
from difflib import get_close_matches 
import numpy as np
from urllib import request
from bs4 import BeautifulSoup


dictionary_words = json.load(open("dictionary_compact.json"))
apostrophe_slangs = json.load(open("apostrophe_slangs.json"))

class Playground:

    def __init__(self, language="en"):
        self.format = format

    def get_word_meaning(self,word):

        """
            Args:
                1. word - str

            Returns:
                Word meaning if it is available in the Dictionary
        """
        word = word.lower()

        try:
            if word in dictionary_words.keys():
                return dictionary_words[word]

            elif word.upper() in dictionary_words.keys():
                return dictionary_words[word.upper()]
            
            elif word.title() in dictionary_words.keys():
                return dictionary_words[word.title()]

            elif len(get_close_matches(word, dictionary_words.keys())) > 0:

                similar_words_list = list(get_close_matches(word, dictionary_words))

                return "Did you mean {} instead ?".format(similar_words_list)
        
        except AssertionError as e:
            raise e

    def sentence_similarity(self,sentence1, sentence2, stopwords):
        if stopwords == None:
            stopwords = []
        
        sent1 = [word.lower() for word in sentence1.split(" ")]
        sent2 = [word.lower() for word in sentence2.split(" ")]
        
        all_words = list(set(sent1+sent2))
        vect_array1 = np.zeros(len(all_words))
        vect_array2 = np.zeros(len(all_words))
        
        for word in sent1:
            if word in stopwords:
                continue
            else:
                vect_array1[all_words.index(word)] += 1
                
        for word in sent2:
            if word in stopwords:
                continue
            else:
                vect_array2[all_words.index(word)] += 1
                
        return 1 - cosine_distance(vect_array1, vect_array2)
    

    def build_similarity_matrix(self,sentences, stop_words):

        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2: #ignore if both are same sentences
                    continue 
                similarity_matrix[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

        return similarity_matrix

    def normalize(self, text):
        sentence = []
        for i in text.split():
            if i == "\n":
                continue
            else: sentence.append(i.replace("[^a-zA-Z]", ""))
        sentence = " ".join(sentence)
        sentence = re.sub(r'\[[0-9]*\]', ' ', sentence)
        return sentence

    def get_word_frequencies(self, text):

        text = self.normalize(text)
        word_frequencies = {}
        
        for word in nltk.word_tokenize(self.normalize(text)):
            if word not in stopwords.words('english'):
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        return word_frequencies

    def get_sentence_scores(self, text):

        text = self.normalize(text)
        sentence_scores = {}
        sentence_list = nltk.sent_tokenize(text)

        word_frequencies = self.get_word_frequencies(text)

        maximum_frequency = max(word_frequencies.values())

        try:

            for word in word_frequencies.keys():
                word_frequencies[word] = (word_frequencies[word]/maximum_frequency)
            
            for sent in sentence_list:
                for word in nltk.word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                        if len(sent.split(' ')) < 30:
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequencies[word]
                            else:
                                sentence_scores[sent] += word_frequencies[word]

        except AssertionError as e:
            raise

        return sentence_scores

    def fetch_from_url(self, url):

        try:

            page = request.urlopen(url)
            soup = BeautifulSoup(page, 'lxml')
            fetched_text = ' '.join(map(lambda p:p.text, soup.findAll('p')))
            return fetched_text
        
        except:
            raise ValueError("Cannot fetch text from this URL")


    def summarize(self, sentence_length, format="text",text =None, url=None):
        try:
            if format.lower() == "text":
                raw_text =  text

            elif format.lower() == "url":
                raw_text = self.fetch_from_url(url)

            else:
                raise ValueError("Please input a valid format from url, text")

            if len(raw_text) > 50:
                sentence_scores = self.get_sentence_scores(raw_text)
                summary_sentences = heapq.nlargest(sentence_length, sentence_scores, key=sentence_scores.get)
                summary = ' '.join(summary_sentences)

                return summary

            else:
                raise AssertionError("Minimum text length is 50 characters")

        except AssertionError as e:
            raise


    def get_keywords(self, text, n=5):

        text = re.sub(r'[^\w\s]','',text)
        word_frequencies = self.get_word_frequencies(text)
        keywords = [word for word in list(dict(sorted(word_frequencies.items(), key= lambda x:x[1], reverse=True)).keys()) if word.lower() not in stopwords.words('english')][:n]
        return keywords

    
    def standardize_apostrophe(self,text):

        standardized_word = []
        for word in text.lower().split():
            if word in apostrophe_slangs.keys():
                standardized_word.append(apostrophe_slangs[word])
            else:
                standardized_word.append(word)
        return " ".join(standardized_word)
        









word = Playground()

print(word.standardize_apostrophe("i'll make it in life, i'd"))