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
import requests
from urllib import request
from bs4 import BeautifulSoup






class Playground:

    def __init__(self, language="en"):
        self.format = format

    def get_word_meaning(self,word, c = "definition"):

        """
            Args:
                1. word - str

            Returns:
                Word meaning if it is available in the Dictionary
        """
        word = word.lower()

        try:

            full_def = list(requests.get('https://api.dictionaryapi.dev/api/v1/entries/en/{}'.format(word)).json()[0]['meaning'].values())[0][0][c]
            return full_def
        
        except:
            return "Word not found !"

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

        apostrophe_slangs = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", 
                "couldn't": "could not", "didn't": "did not",  "doesn't": "does not", "don't": "do not", "hadn't": "had not", 
                "hasn't": "has not", "haven't": "have not", "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", 
                "how'd'y": "how do you", "how'll": "how will", "how's": "how is",  "I'd": "I would", "I'd've": "I would have", 
                "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would", "i'd've": "i would have",
                "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would", 
                "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have","it's": "it is", "let's": "let us", 
                "ma'am": "madam", "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have",
                "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", 
                "needn't've": "need not have","o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have", 
                "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would", 
                "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is", 
                "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have",
                "so's": "so as", "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is",
                "there'd": "there would", "there'd've": "there would have", "there's": "there is", "here's": "here is",
                "they'd": "they would", "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have",
                "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we would", 
                "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are", "we've": "we have","weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",  
                "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", 
                "where's": "where is", "where've": "where have", "who'll": "who will", "who'll've": "who will have", 
                "who's": "who is", "who've": "who have", "why's": "why is", "why've": "why have", "will've": "will have", 
                "won't": "will not", "won't've": "will not have", "would've": "would have", "wouldn't": "would not", 
                "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would","y'all'd've": "you all would have",
                 "you'll": "you will", "you'll've": "you will have", "you're": "you are", "you've": "you have"}

        standardized_word = []
        for word in text.lower().split():
            if word in apostrophe_slangs.keys():
                standardized_word.append(apostrophe_slangs[word])
            else:
                standardized_word.append(word)
        return " ".join(standardized_word)
        

word = Playground()

print(word.standardize_apostrophe("I'll make it here"))