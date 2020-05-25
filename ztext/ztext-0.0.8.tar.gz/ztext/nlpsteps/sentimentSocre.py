from textblob import TextBlob

import warnings

warnings.filterwarnings('ignore')

def sentimentSocre(text):
  blob = TextBlob(text)
  return blob.sentiment.polarity