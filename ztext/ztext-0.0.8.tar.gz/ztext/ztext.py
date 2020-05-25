#pip install IPython bokeh pandas xlrd gensim spacy textacy textblob pyvis pyLDAvis
# python -m spacy download en_core_web_sm

# from ztext.nlpsteps import text_clean, sentimentSocre, topic_analysis,plot_topics,svo

# import pandas as pd
import warnings,IPython, spacy
from tqdm import tqdm
import pandas as pd


warnings.filterwarnings('ignore')

def sampledata():
    import pandas as pd
    return pd.read_excel('https://github.com/ZackAnalysis/ztext/blob/master/ztext/sampleData.xlsx?raw=true')

    
class Ztext:
    def __init__(self,df=None,textCol='',nTopics=5,custom_stopwrods=[], samplesize=None):
        try:
            nlp = spacy.load('en_core_web_sm')
        except:
            print('Please make sure spacy model is loaded.\n\
                    Install spacy model first by running\n\
                    python -m spacy download en_core_web_sm')
            return
        if samplesize:
            print('')
            df = df.sample(samplesize)
        self.df = df.astype('str').reset_index()
        self.textCol = textCol
        self.nTopics = nTopics
        self.custom_stopwrods = custom_stopwrods
        self.doctopics = None
        self.topicDescribe = None
        self.dictionary = None
        self.model = None
        self.tokens = None
        self.ldaVis = None
        self.svodfs = {}
    
    def loadfile(self, filename,textCol='',nTopics=5,custom_stopwrods=[], samplesize=None):
        if filename.endswith("?raw=true"):
            filename = filename.replace("?raw=true",'')
        filetype = filename.split('.')[-1]
        if textCol:
            self.textCol = textCol
        if filetype not in ['csv','xlsx','json']:
            print(f'filetype .{filetype} not supported')
            return
        if filetype == 'csv':
            self.df = pd.read_csv(filename)
        if filetype == 'xlsx':
            self.df = pd.read_excel(filename)
        if filetype == 'json':
            self.df = pd.read_json(filename)
        if samplesize:
            self.df = self.df.sample(samplesize)
    
    def loaddf(self, df,textCol=None):
        if textCol:
            self.textCol = textCol
        if isinstance(df,pd.DataFrame):
            self.df = df
        else:
            print('Please load a pandas dataframe.')
    
    def setcol(self,textCol):
        self.textCol = textCol

    def setNtopics(self,n):
        self.ntopics = n

    def checkdf(self):
        if self.df is None:
            print('loadfile or dataframe first')
            return False
        if self.textCol is None or not self.textCol:
            print('set the textColname first, by using Ztext.setcol("Colname")')
            return False

    def sentiment(self):
        if self.checkdf() == False:
            return
        print('sentment analyzing ...')
        from ztext.nlpsteps.sentimentSocre import sentimentSocre
        self.df['sentimentScore'] = self.df[self.textCol].apply(sentimentSocre)
        return self.df

    def clean(self):
        if self.checkdf() == False:
            return
        print('cleaning text ...')
        self.df[self.textCol] = self.df[self.textCol].fillna('')
        from ztext.nlpsteps.text_clean import text_clean
        for n in tqdm(self.df.index):
            self.df.loc[n,'cleaned_text'] = text_clean(self.df.astype('str').loc[n,self.textCol], \
                                                       custom_stopwrods=self.custom_stopwrods)
        # self.df['cleaned_text'] = self.df[self.textCol].apply(text_clean, custom_stopwrods=self.custom_stopwrods)
        return self.df

    def get_topics(self, nTopics=None):
        if self.checkdf() == False:
            return
        if not nTopics:
            nTopics = self.nTopics
        from ztext.nlpsteps.topicAnalysis import topic_analysis
        if 'cleaned_text' not in self.df:
            print('data need to be cleaned first, cleaning the data')
            self.clean()
        print('getting topics ...')
        self.doctopics, self.topicDescribe, self.model, self.tokens, self.dictionary= topic_analysis(self.df, nTopics,'cleaned_text')
        self.df = self.df.merge(self.doctopics, left_index=True, right_index=True)
        return self.df

    def getldaVis(self):
        if self.checkdf() == False:
            return
        from ztext.nlpsteps.topicAnalysis import getldaVis
        
        if self.model is None or self.tokens is None:
            print('applying LDA analysis first')
            self.get_topics()
        self.ldaVis = getldaVis(self.model, self.tokens)
        return self.ldaVis

    def topicCount(self):
        if self.checkdf() == False:
            return
        from ztext.nlpsteps.topicAnalysis import plot_topics
        if self.topicDescribe is None:
            print('applying LDA analysis first')
            self.get_topics()
        plot_topics(self.topic_analysis)
        # to do add none notebook here


    def getSVO(self, topicN='topic1',clean=False):
        if self.checkdf() == False:
            return
        from ztext.nlpsteps.svo import SVO  
        if 'KeyTopic' not in self.df:
            print('Topic analysis must run first. ')
            self.get_topics()
        print('getting SVO for ', topicN)
        text = '\n'.join(self.df.loc[self.df['KeyTopic']==topicN,self.textCol])
        svodf = SVO(text)
        self.svodfs[topicN] = svodf
        return svodf
         
    
    def SVOall(self, topicCol='KeyTopic',clean=False):
        if self.checkdf() == False:
            return
        if clean:
            self.svodfs = {}
        from ztext.nlpsteps.svo import SVO  
        if 'KeyTopic' not in self.df:
            print('Topic analysis must run first. ')
            self.get_topics()
        print('Starting SVO extraction for all topics...')
        for topic in self.df[topicCol].unique():
            if topic in self.svodfs:
                print('SVO dateframe for ', topic, 'already exists, next.')
                continue
            print('analyzing ', topic, '...')
            self.getSVO(topic)
        return self.svodfs
    
    def getSVOvis(self, topic='topic1',options='entity'): # option could be "entity", "person", "any"
        if self.checkdf() == False:
            return
        from ztext.nlpsteps.svo import visSVO
        if topic not in self.svodfs:
            print('Must run SVO extraction first')
            self.getSVO(topic)
        if self.svodfs[topic] is None or len(self.svodfs[topic]) == 0:
            print('no entity detected in the corpus, try another topic')
            return
        print('creating SVO Visualization file')
        visSVO(self.svodfs[topic],topic)
        return

    def getAllentities(self):
        if self.checkdf() == False:
            return
        import pandas as pd
        SVOall()
        return pd.concat([svodfs.values()])


# if __name__ == '__main__':


    # import pandas as pd
    # df = pd.read_excel('ztext/ztext/sampleData.xlsx')
    # nlpdf = Nlpdf(df,'content',samplesize=300)
    # nlpdf.get_top

