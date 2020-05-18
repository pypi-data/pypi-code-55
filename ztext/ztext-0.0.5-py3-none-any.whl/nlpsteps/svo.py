import spacy, textacy, pyvis
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

nlp = spacy.load('en_core_web_sm')
try:
  nlp = spacy.load('en_core_web_sm')
except:
  print('Install spacy model first by running\npython -m spacy download en_core_web_sm')

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

def SVOall(df, textCol='KeyTopic'):
  topicSVOs = {}
  for topic in df[textCol].unique():
    text = '\n'.join(df.loc[df[textCol]==topic,'content'])
    topicSVO = SVO(text)
    # topicSVO.to_csv(f'svo_{topic}.csv', index=0)
    topicSVOs[topic] = topicSVO
  return topicSVOs
