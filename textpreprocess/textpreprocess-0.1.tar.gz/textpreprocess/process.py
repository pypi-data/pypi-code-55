from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

class process:

    def remove_punctuation(self,sentence_as_a_list):
        '''
        Remove Punctuation from the sentence
        '''
        sentence_as_a_list = [''.join(c for c in s if c not in string.punctuation) for s in sentence_as_a_list]
        sentence_as_a_list = [s for s in sentence_as_a_list if s]
        return sentence_as_a_list

    def simpleForm(self,list_of_sentences,removeStopwords=True,removePunctuation=True,language='english'):
        '''
        simpleForm of sentence is all words lemmatized , stopwords
        removed and punctuation based on user.
        '''
        new_list=[]
        stop_words=set()
        lemmatizer = WordNetLemmatizer()
        try:
            stop_words = set(stopwords.words(language))
        except Exception as e:
            stop_words = set(stopwords.words('english'))
        if removeStopwords==False:
            stop_words=set()
        for sentence in list_of_sentences:
            sentence = sentence.lower()
            sentence = sentence.strip()
            word_tokens = word_tokenize(sentence)
            new_word_tokens = []
            for word in word_tokens:
                new_word_tokens.append(lemmatizer.lemmatize(word))

            filtered_sentence = [w for w in new_word_tokens if not w in stop_words]
            new_list.append(filtered_sentence)

        if removePunctuation==True:
            return_list=[]
            for li in new_list:
                return_list.append(self.remove_punctuation(li))
            new_list = return_list
        return new_list

    def getVocab(self,list_of_list_of_words):
        vocab=[]
        for list_of_words in list_of_list_of_words:
            for word in list_of_words:
                if word not in vocab:
                    vocab.append(word)
        vocab.sort()
        return vocab

    def getSentenceasVectors(self,list_of_list_of_words,vocab):
        list_of_vectors=[[j.count(vocab[i]) for i in range(len(vocab))] for j in list_of_list_of_words]
        return list_of_vectors
