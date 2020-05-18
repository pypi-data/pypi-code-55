#pip install IPython bokeh pandas xlrd gensim spacy textacy textblob pyvis pyLDAvis
# python -m spacy download en_core_web_sm
import pyLDAvis.gensim
import spacy, re,textacy,pyvis, IPython
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20
from bokeh.transform import factor_cmap
import warnings
from textblob import TextBlob
warnings.filterwarnings('ignore')
# nlp = spacy.load('en_core_web_sm')
try:
  nlp = spacy.load('en_core_web_sm')
except:
  print('Install spacy model first by running\npython -m spacy download en_core_web_sm')
pyLDAvis.enable_notebook()


#Step 1 add sentiment column
def sentimentSocre(text):
  blob = TextBlob(text)
  return blob.sentiment.polarity

# Step 2 text clean
def text_clean(text, custom_stopwrods=[], toLower=True):
  if toLower:
    text=text.lower()
  doc = nlp(text)
  return ' '.join([d.lemma_ for d in doc if \
    all([2<len(d.text)<20,d.is_alpha, not d.is_stop, d.lemma_ not in custom_stopwrods])])

# Step3 Topic Analysis

def topic_analysis(cleanCol, nTopics=5):
  cleandata = df['cleaned_text'].apply(lambda x: x.split(' '))
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
  ldaVis = pyLDAvis.gensim.prepare(model, tokens, dictionary=model.id2word)
  doctopics= doctopics.merge(topicDescribe[['KeyTopic','TopicKeywords']], on='KeyTopic', how='left')
  return doctopics, topicDescribe, ldaVis

# Step 3.2 
def plot_topics(topicDescribe):
  output_notebook()
  source = ColumnDataSource(topicDescribe)
  tooltips = [('KeyTopic','@KeyTopic'),('keywords','@TopicKeywords'),('DocCount','@DocCount')]
  p = figure(x_range=list(topicDescribe['KeyTopic']), plot_height=400, plot_width=800,
            title="Topic Counts", toolbar_location=None, 
            tools="pan,wheel_zoom,box_zoom,reset,hover, save", 
            tooltips=tooltips)
  p.vbar(x = 'KeyTopic', top='DocCount',width=0.9, source=source,
   color=factor_cmap('KeyTopic', palette=Category20[20], factors=list(topicDescribe['KeyTopic'])))
  show(p)

  plot_topics(topicDescribe)

# Step 4 SVO
def SVO(text, sentiment=False): # return SVO table from given text
  if not text: 
    print('no text found') # empty text warning
    return
  doc = nlp(text) 
  out = [] # prepare an empty list to receive result
  for sent in doc.sents: # loop each sentence in the text
    '''
    todo filter sent by ent
    '''
    elements = list(textacy.extract.subject_verb_object_triples(sent))
    # generate svo list
    if sentiment: # check whether need return sentiments
      score = TextBlob(' '.join([d.text for d in sent])).sentiment.polarity
      # return sentment score for the sentence
      elements = [(e[0],e[1],e[2], score) for e in elements]
      # reoganize the sentence analysis result
    out += elements # add sentence result to the output list 
  columns=['Subject','Verb','Object'] # define the structure of output table
  if sentiment:
    columns.append('Sentiment') # add sentiment column if selected
  svodf= pd.DataFrame(out, columns=columns) # sent result to dataframe
  svodf['SubjectType'] =svodf.Subject.apply(lambda x: [y.label_ for y in x.ents] \
    if [y.label_ for y in x.ents] else None)
  svodf['ObjectType'] =svodf.Object.apply(lambda x: [y.label_ for y in x.ents] \
    if [y.label_ for y in x.ents] else None)
  svodf.Subject =svodf.Subject.apply(lambda x: x.text)
  svodf.Object =svodf.Object.apply(lambda x: x.text)
  svodf.Verb =svodf.Verb.apply(lambda x: x.text)
  newCols = ['Subject', 'SubjectType', 'Verb', 'Object','ObjectType']
  if sentiment:
    newCols.append('Sentiment') # add sentiment column if selected
  svodf= svodf[newCols]
  return svodf

def visSVO(svodf, filename='', options='entity'): # option could be "entity", "person", "any"
  filename = f'network_{filename}.html'
  if options in ["entity","person"]: # check options
    svodf=svodf.dropna(subset=['SubjectType']).reset_index(drop=True) # remove non Type subjects
    if options == "person": # check options
      svodf=svodf.loc[svodf.SubjectType.apply(lambda x: 'PERSON' in x),:] 
      # select only person as subject relations
  nodeS = list(set(svodf.Subject)) # create subject nodes
  nodeO = list(set(svodf.Object)) # create object nodes
  nodeAll = list(set(nodeS+nodeO)) # merge and uniq all nodes
  nodes = range(len(nodeAll)) # create node for the visualization (must be numbers)
  colors = ['maroon' if n in nodeS else 'TEAL' for n in nodeAll] 
  # set subject at color "maroon" and object as "teal" if both as "maroon"
  net = pyvis.network.Network(height='500px', width='1000px',) 
  # create a empty chart net
  net.add_nodes(nodes, label=nodeAll, color=colors, title=nodeAll) 
  # add nodes to network graph
  for i in svodf.index: # add relationships(Verbs) to the graph
    net.add_edge(nodeAll.index(svodf.loc[i,'Subject']),nodeAll.index(svodf.loc[i,'Object']),
     label=svodf.loc[i,'Verb'], title=str(i))
  net.show(filename) # save the graph to file "network.html"
  return filename

def docSVO(df, textCol='KeyTopic'):
  topicSVOs = {}
  for topic in df[textCol].unique():
    text = '\n'.join(df.loc[df[textCol]==topic,'content'])
    topicSVO = SVO(text)
    topicSVO.to_csv(f'svo_{topic}.csv', index=0)
    topicSVOs[topic] = topicSVO


if __name__ == '__main__':
  df = pd.read_excel('sampleData.xlsx')
  # df = df.sample(500).reset_index()
  textCol = 'content'
  nTopics = 5


  df['sentimentScore'] = df[textCol].apply(sentimentSocre)

  df['cleaned_text'] = df[textCol].apply(text_clean)

  doctopics, topicDescribe, ldaVis = topic_analysis(df['cleaned_text'], nTopics)
  df = df.merge(doctopics, left_index=True, right_index=True)

  topicSVOs = docSVO(df)

  visfile = visSVO(topicSVOs['topic2'],'topic2')
  IPython.display.HTML(visfile)

  plot_topics(topicDescribe)