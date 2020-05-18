import nltk, string
import requests
import pandas as pd
import os.path
from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

class CosineSimilarityFinder:
    
    def __init__(self,dataset=None, datasetIndex=0):
        self.vectorizer = TfidfVectorizer(tokenizer=self.normalize)
        pass

    def stem_tokens(self,tokens):
        return [stemmer.stem(item) for item in tokens]
    
    def normalize(self,text):
        return self.stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

    def load_dataset(self,dataset=None, datasetIndex=0):
        if dataset == None:
            return None
        else:
            extension = os.path.splitext(dataset)[1]

            if extension == '.html':
                html = requests.get(dataset, verify=False)
                self.df = pd.read_html(html.text)[datasetIndex]
                return self.df
            elif extension == '.csv':
                self.df = pd.read_csv(dataset)
                return self.df
            elif extension == '.xls' or extension == '.xlsx':
                self.df = pd.read_excel(dataset, index_col=0)
                return self.df
            else:
                if 'http' in dataset or 'https' in dataset:
                    html = requests.get(dataset, verify=False)
                    self.df = pd.read_html(html.text)[datasetIndex]
                    return self.df
                else:
                    return None

    
    def find_similarity(self,text1, text2):
        tfidf = self.vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0, 1]





            