#pip install IPython bokeh pandas xlrd gensim spacy textacy textblob pyvis pyLDAvis
# python -m spacy download en_core_web_sm

# from ztext.nlpsteps import text_clean, sentimentSocre, topic_analysis,plot_topics,svo

# import pandas as pd
import warnings,IPython
# from tqdm import tqdm

warnings.filterwarnings('ignore')

def sampledata():
    import pandas as pd
    return pd.read_excel('https://github.com/ZackAnalysis/ztext/blob/master/ztext/sampleData.xlsx?raw=true')

    
class Ztext:
    def __init__(self,df,textCol,nTopics=5, samplesize=None):
        if samplesize:
            print('')
            df = df.sample(samplesize)
        self.df = df
        self.textCol = textCol
        self.nTopics = nTopics
        self.doctopics = None
        self.topicDescribe = None
        self.model = None
        self.tokens = None
        self.ldaVis = None
        self.svodfs = None
    
    def sentiment(self):
        print('sentment analyzing ...')
        from ztext.nlpsteps.sentimentSocre import sentimentSocre
        self.df['sentimentScore'] = self.df[self.textCol].apply(sentimentSocre)
        return self.df

    def clean(self):
        print('cleaning text ...')
        from ztext.nlpsteps.text_clean import text_clean
        self.df['cleaned_text'] = self.df[self.textCol].apply(text_clean)
        return self.df

    def get_topics(self, nTopics=None):
        
        if not nTopics:
            nTopics = self.nTopics
        from ztext.nlpsteps.topicAnalysis import topic_analysis
        if 'cleaned_text' not in self.df:
            print('data need to be cleaned first, cleaning the data')
            self.clean()
        print('getting topics ...')
        self.doctopics, self.topicDescribe, self.model, self.tokens= topic_analysis(self.df, nTopics,'cleaned_text')
        self.df = self.df.merge(self.doctopics, left_index=True, right_index=True)
        return self.df

    def getldaVis(self):
        from ztext.nlpsteps.topicAnalysis import getldaVis
        
        if self.model is None or self.tokens is None:
            print('applying LDA analysis first')
            self.topic_analysis()
        self.ldaVis = getldaVis(self.model, self.tokens)
        return self.ldaVis

    def topicCount(self):
        from ztext.nlpsteps.topicAnalysis import plot_topics
        if self.topicDescribe is None:
            print('applying LDA analysis first')
            self.topic_analysis()
        plot_topics(self.topic_analysis)
        # to do add none notebook here


    def getSVO(self, topicN='topic1'):
        if 'KeyTopic' not in self.df:
            print('topic analysis must run first. quit')
            return
        text = '\n'.join(self.df.loc[self.df['KeyTopic']==topicN,self.textCol])
        from ztext.nlpsteps.svo import SVO    
        return SVO(text)
         
    
    def SVOall(topicCol='KeyTopic'):
        if 'KeyTopic' not in self.df:
            print('topic analysis must run first. quit')
            return
        self.svodfs = {}
        for topic in self.df[topicCol].unique():
            print('analyzing ', topic, '...')
            self.svodfs[topic] = self.getSVO(topic)
        return self.svodfs


# if __name__ == '__main__':


    # import pandas as pd
    # df = pd.read_excel('ztext/ztext/sampleData.xlsx')
    # nlpdf = Nlpdf(df,'content',samplesize=300)
    # nlpdf.get_top

