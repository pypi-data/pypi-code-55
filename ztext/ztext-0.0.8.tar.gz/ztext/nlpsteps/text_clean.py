import spacy,warnings


warnings.filterwarnings('ignore')
try:
  nlp = spacy.load('en_core_web_sm')
except:
  print('Install spacy model first by running\npython -m spacy download en_core_web_sm')

def text_clean(text, custom_stopwrods=[], toLower=True):
  if not isinstance(text,str):
    print('type error not string type in the data please remove first\n',text)
    return
  if toLower:
    text=text.lower()
  doc = nlp(text)
  return ' '.join([d.lemma_ for d in doc if \
    all([2<len(d.text)<20,d.is_alpha, not d.is_stop, d.lemma_ \
      not in custom_stopwrods])])
