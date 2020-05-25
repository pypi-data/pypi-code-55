from gensim import corpora
from gensim.models import LdaModel
import pandas as pd
import re

from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20
from bokeh.transform import factor_cmap

import warnings

warnings.filterwarnings('ignore')

def topic_analysis(df, nTopics=5, cleanTextCol='cleaned_text'):
  df[cleanTextCol]=df[cleanTextCol].fillna('')
  cleandata = df[cleanTextCol].fillna('').apply(lambda x: x.split(' '))
  dictionary = corpora.Dictionary(cleandata)
  tokens = [dictionary.doc2bow(d) for d in cleandata]
  model = LdaModel(tokens, num_topics=nTopics, id2word=dictionary, 
                update_every=1, chunksize=50, passes=10,
                per_word_topics=True, alpha='auto')
  docweights = [model.get_document_topics(t, minimum_probability=0) for t in tokens]
  doctopics = pd.DataFrame(docweights).apply(lambda x: x.apply(lambda y: y[-1] if y else 0))
  doctopics.columns = [f'topic{n+1}' for n in doctopics.columns]
  doctopics['KeyTopic']=doctopics.apply(lambda y:doctopics.columns[y==y.max()][0], axis=1)

  # create topicdescribe
  topics = model.show_topics(num_words=6)
  keywords = [re.findall(r'\*"(.*?)"',d[1]) for d in topics]
  weights = [re.findall(r'([\d\.]+)\*', d[1]) for d in topics]
  kwdf= pd.DataFrame(keywords, columns=[f'keyword_{n}' for n in range(len(keywords[0]))])
  wtdf= pd.DataFrame(weights, columns=[f'weight_{n}' for n in range(len(weights[0]))])
  topicDescribe =  kwdf.merge(wtdf,left_index=True, right_index=True)
  topicDescribe[sorted(topicDescribe.columns, key=lambda x:x.split('_')[-1])]
  topicDescribe['KeyTopic'] = [f'topic{n+1}' for n in range(len(topics))]
  topicDescribe['TopicKeywords'] = [' '.join(k) for k in keywords]
  topicDescribe['DocCount'] = doctopics['KeyTopic'].value_counts().sort_index().values
  topicDescribe = topicDescribe[['KeyTopic']+[col for col in topicDescribe.columns if \
    col != 'KeyTopic']]
  
  doctopics= doctopics.merge(topicDescribe[['KeyTopic','TopicKeywords']], on='KeyTopic', how='left')
  return doctopics, topicDescribe, model, tokens, dictionary


def getldaVis(model, tokens):
  import pyLDAvis.gensim
  try:
    pyLDAvis.enable_notebook()
  except:
    print('LDAvisualization should run in Jupyter notebook or Google colab')
  return pyLDAvis.gensim.prepare(model, tokens, dictionary=model.id2word)

def plot_topics(topicDescribe):
  try:
    output_notebook()
  except:
    print('LDAvisualization should run in Jupyter notebook or Google colab')
  source = ColumnDataSource(topicDescribe)
  tooltips = [('KeyTopic','@KeyTopic'),('keywords','@TopicKeywords'),('DocCount','@DocCount')]
  p = figure(x_range=list(topicDescribe['KeyTopic']), plot_height=400, plot_width=800,
            title="Topic Counts", toolbar_location=None, 
            tools="pan,wheel_zoom,box_zoom,reset,hover, save", 
            tooltips=tooltips)
  p.vbar(x = 'KeyTopic', top='DocCount',width=0.9, source=source,
   color=factor_cmap('KeyTopic', palette=Category20[20], factors=list(topicDescribe['KeyTopic'])))
  show(p)
