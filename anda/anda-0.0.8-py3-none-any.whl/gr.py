
import json
import unicodedata
import re
import requests

### DATA (i.e. greek vocabulary)
try: # if possible, upload the data from the package
  morpheus_by_lemma = json.load(open("anda/data/morpheus_by_lemma.json"))
  morpheus_dict = json.load(open("anda/data/morpheus_dict.json"))
except: # if not, read them from sciencedata
  publicfolder = "8fe7d59de1eafe5f8eaebc0044534606"
  morpheus_by_lemma = json.loads(requests.get("https://sciencedata.dk/public/" + publicfolder + "/morpheus_by_lemma.json").content)
  morpheus_dict = json.loads(requests.get("https://sciencedata.dk/public/" + publicfolder + "/morpheus_dict.json").content)



### simple replacements
to_replace_dict={
    "ἓ":"ἕ",
    "ὸ" : "ό",
    "ὰ" : "ά",
    "ὲ" : "έ",
    "ὶ" : "ί",
    "ὴ" : "η",
    }

stopwords_string = "αὐτὸς αὐτός γε γὰρ γάρ δ' δαὶ δαὶς δαί δαίς διὰ διά δὲ δέ δὴ δή εἰ εἰμὶ εἰμί εἰς εἴμι κατὰ κατά καὶ καί μετὰ μετά μὲν μέν μὴ μή οἱ οὐ οὐδεὶς οὐδείς οὐδὲ οὐδέ οὐκ οὔτε οὕτως οὖν οὗτος παρὰ παρά περὶ περί πρὸς πρός σὸς σός σὺ σὺν σύ σύν τε τι τις τοιοῦτος τοὶ τοί τοὺς τούς τοῦ τὰ τά τὴν τήν τὶ τὶς τί τίς τὸ τὸν τό τόν τῆς τῇ τῶν τῷ ἀλλ' ἀλλὰ ἀλλά ἀπὸ ἀπό ἂν ἄλλος ἄν ἄρα ἐγὼ ἐγώ ἐκ ἐξ ἐμὸς ἐμός ἐν ἐπὶ ἐπί ἐὰν ἐάν ἑαυτοῦ ἔτι ἡ ἢ ἤ ὁ ὃδε ὃς ὅδε ὅς ὅστις ὅτι ὑμὸς ὑμός ὑπὲρ ὑπέρ ὑπὸ ὑπό ὡς ὥστε ὦ ξύν ξὺν σύν σὺν τοῖς τᾶς την α μην ἃ 𝔚 β δη δι δ᾿ δʼ δ τότ ἀλλʼ ὅσʼ ἐπʼ ιη △ζ ιβ τχ μη ; ὃ γ . ὅταν ποτέ οὐδʼ καθʼ ἀλλ᾿ την α μην ἃ 𝔚 β δη δι δ᾿ δʼ δ τότ ἀλλʼ ὅσʼ ἐπʼ ιη △ζ ιβ τχ μη ; ὃ γ ὅταν ποτέ οὐδʼ καθʼ ἀλλ᾿ την α μην ἃ 𝔚 β δη δι δ᾿ δʼ δ τότ ἀλλʼ ὅσʼ ἐπʼ ιη △ζ ιβ τχ μη ὃ γ ὅταν ποτέ οὐδʼ καθʼ ἀλλ᾿"
STOPS_LIST = stopwords_string.split()

def get_sentences(string):
  sentences = [s.strip() for s in re.split("\·|\.|\:|\;", unicodedata.normalize("NFC", string))]
  return sentences

def return_list_of_tokens(word, filter_by_postag=None, involve_unknown=False, preference="n"):
  word = unicodedata.normalize("NFC", word)
  try:
    list_of_tokens = morpheus_dict[word]
    if len(list_of_tokens) < 1:
      list_of_tokens = morpheus_dict[word.lower()]
      if len(list_of_tokens) < 1:
        list_of_tokens = [{"f":word, "i": "", "b":"", "l":word.lower(), "e":"", "p":"", "d":"", "s":"", "a":""}]
  except:
    list_of_tokens = [{"f":word, "i": "", "b":"", "l":word.lower(), "e":"", "p":"", "d":"", "s":"", "a":""}]

  if filter_by_postag != None:
    try:
      list_of_tokens_filtered = []
      for token in list_of_tokens:
        if token["p"][0] in filter_by_postag:
          list_of_tokens_filtered.append(token)
      list_of_tokens = list_of_tokens_filtered
    except:
      if involve_unknown == False:
        list_of_tokens = []
    try:
      # prefer adjectives and nouns over verbs
      token_letters = [token["p"][0] for token in list_of_tokens]
      if ("n" in token_letters) or ("a" in token_letters):
        if ("v" in token_letters):
          list_of_tokens = [token for token in list_of_tokens if token["p"][0] in ["a", "n"]]
        # prefer nouns over adjectives
      #if "a" and "n" in token_letters:
      #  list_of_tokens = [token for token in list_of_tokens if token["p"][0] == "n"]
    except:
      pass
  return list_of_tokens


def return_all_unique_lemmata(word, filter_by_postag=None, involve_unknown=False):
  list_of_tokens = return_list_of_tokens(word, filter_by_postag=filter_by_postag, involve_unknown=involve_unknown)
  lemmata = "/".join(set([token["l"] for token in list_of_tokens]))
  return lemmata

def return_all_unique_translations(word, filter_by_postag=None, involve_unknown=False):
  list_of_tokens = return_list_of_tokens(word, filter_by_postag=filter_by_postag, involve_unknown=involve_unknown)
  try:
    translations = " / ".join(set([token["s"] for token in list_of_tokens]))
  except:
    translations = ""
  return translations

def return_first_lemma(word, filter_by_postag=None, involve_unknown=False):
  list_of_tokens = return_list_of_tokens(word, filter_by_postag=filter_by_postag, involve_unknown=involve_unknown)
  try:
    first_lemma = list_of_tokens[0]["l"]
  except:
    first_lemma = ""
  return first_lemma

def morphological_analysis(string):
  first_tokens = []
  string_tokenized = tokenize_string(string)
  string_analyzed = [return_list_of_tokens(word)[0] for word in string_tokenized if word != ""]
  return string_analyzed

def lemma_translator(word):
  try:
    translations = []
    for option in word.split("/"):
      translations.append(" / ".join(set([token["s"] for token in morpheus_by_lemma[option]])))
    translations = " / ".join(translations)
  except:
    translations = ""
  return translations

def tokenize_string(string):
  string = re.sub(r'[A-Za-z0-9]+', "", string)
  string = re.sub(r'[-,\(\)=\\\?·‖\+;\.\:/\[\]\*—»«\§˘„”\|]+', "", string)
  string = re.sub(r'[^\w\s]','', string)
  for k,v in to_replace_dict.items():
    string = string.replace(k,v)
  string = unicodedata.normalize("NFC", string)
  string_tokenized = string.split()
  string_tokenized = [word for word in string_tokenized if len(word) > 1]
  return string_tokenized

def lemmatize_string(string, all_lemmata=False, filter_by_postag=None, involve_unknown=False):
  string_tokenized = tokenize_string(string)
  string_tokenized = [word for word in string_tokenized if word not in STOPS_LIST]
  if all_lemmata==True:
    string_lemmatized = [return_all_unique_lemmata(word, filter_by_postag=filter_by_postag, involve_unknown=involve_unknown) for word in string_tokenized if word != ""]
  else: 
    string_lemmatized = [return_first_lemma(word, filter_by_postag=filter_by_postag, involve_unknown=involve_unknown) for word in string_tokenized if word != ""]  
  string_lemmatized = [word for word in string_lemmatized if word != ""]
  string_lemmatized = [re.sub(r'\d', "", w) for w in string_lemmatized if w not in STOPS_LIST]
  return string_lemmatized

def get_lemmatized_sentences(string, all_lemmata=False, filter_by_postag=None, involve_unknown=False):
  sentences = get_sentences(string)
  lemmatized_sentences = []
  for sentence in sentences:
    lemmatized_sentence = lemmatize_string(sentence, all_lemmata=all_lemmata, filter_by_postag=filter_by_postag, involve_unknown=involve_unknown)
    if len(lemmatized_sentence) > 0:
      lemmatized_sentences.append(lemmatized_sentence)
  return lemmatized_sentences