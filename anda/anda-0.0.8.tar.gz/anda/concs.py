def concordance_freq_dist_df(data_frame, term):
  """build dataframe of most common words in concordance rows"""
    concordance = concordance_generator(data_frame, term)
    freq_dist = concordance_freq_dist(concordance, term)
    return most_common_df(freq_dist, 1000)

def concordance_generator(data_frame, term):
  """build concordance rows from data"""
    concordance_list = []
    for author_name in data_frame["author"].unique().tolist():
        for list_element in data_frame[data_frame["author"]==author_name]["lemmata"].tolist()[0]:
            concordance_list.extend(word_concordance(list_element, term, 7))
    return concordance_list
### based on https://stackoverflow.com/questions/22118136/nltk-find-contexts-of-size-2k-for-a-word

from nltk import ConcordanceIndex
class ConcordanceIndex2(ConcordanceIndex):
    def create_concordance(self, word, width):
        "Returns a list of contexts for @word with a context <= @token_width"
        half_width = width // 2
        contexts = []
        for i, token in enumerate(self._tokens):
            if token == word:
                start = i - half_width if i >= half_width else 0
                context = self._tokens[start:i + half_width + 1]
                contexts.append(context)
        return contexts
    def create_concordance_raw_words(self, word, width):
        "Returns a list of contexts for @word with a context <= @token_width"
        half_width = width // 2
        contexts = []
        for i, token in enumerate(self._tokens):
            if token == word:
                start = i - half_width if i >= half_width else 0
                context = self._tokens[start:i + half_width + 1]
                contexts.extend(context[:half_width] + context[half_width + 1:])
        return contexts

def word_concordance(text, word, width):
    c = ConcordanceIndex2(text.split())
    return c.create_concordance(word, width)

def conc_from_list(text, word, width):
    c = ConcordanceIndex2(text)
    return c.create_concordance(word, width)

def conc_words_from_list(text, word, width):
    c = ConcordanceIndex2(text)
    return c.create_concordance_raw_words(word, width)

def concordance_freq_dist(input_concordance, term_to_remove):
  """count frequency distributions in concordance-rows data"""
    output = " ".join([" ".join(entry) for entry in input_concordance])
    output_list = list(filter(lambda x: x!= term_to_remove, output.split()))
    freq_dist = nltk.FreqDist([word for word in output_list])
    for word in freq_dist:
        freq_dist[word] / float(len(output_list))
    return freq_dist

def most_common_df(freq_dist_dict, number):
  """form a dataframe of most frequent terms in concordance data"""
     return pd.DataFrame(freq_dist_dict.most_common(number), columns=["term", "norm_freq"])

def conc_words_from_dataframe(dataframe, column, term):
  concordance_list = []
  for list_element in dataframe[column].tolist():
    concordance_list.extend(conc_words_from_list(list_element, term, 7))
  return concordance_list

def most_common_words_in_conc(dataframe, column, term, number):
  """generate dataframe of most frequent words from a list"""
  list_of_lists = dataframe[column].tolist()
  one_merged_list = []
  for list_element in list_of_lists:
    one_merged_list.extend(list_element)
  conc_words_list = conc_words_from_dataframe(dataframe, column, term)
  most_common_words = nltk.FreqDist(conc_words_list).most_common()
  most_common_words_data = []
  for tup in most_common_words:
    conc_TF = tup[1] / len(conc_words_list)
    doc_count = one_merged_list.count(tup[0])
    doc_TF = doc_count /  len(one_merged_list)
    conc_doc_TF = conc_TF / doc_TF
    most_common_words_data.append([tup[0], list_of_meanings(tup[0]), tup[1], np.round(conc_TF, 7), doc_count, np.round(doc_TF, 7), np.round(conc_doc_TF, 7)])
  most_common_words_df = pd.DataFrame(most_common_words_data)
  most_common_words_df.columns = ["lemma", "translation", "conccount", "concTF", "doccount", "docTF", "conc_vs_doc_TF"]
  most_common_words_df.sort_values("conc_vs_doc_TF", ascending=False, inplace=True)
  return most_common_words_df

def most_common_conc_from_row(row, column, term, width):
  """returns list of sorted by MI"""
  doc_text_list = row[column]
  doc_conc_list = conc_words_from_list(doc_text_list, term, width)
  most_common_words = nltk.FreqDist(doc_conc_list).most_common()
  N = len(doc_text_list) ### number of words in the subcorpus
  x_count = doc_text_list.count(term)
  try: Px = x_count / N ### rel.freq. of the key term
  except: Px = 0
  most_common_words_data = []
  for tup in most_common_words:
    TFconc = tup[1] / len(doc_conc_list) ### term frequency (TF)
    y_count = doc_text_list.count(tup[0])
    TFdoc = y_count / N
    MI = TFconc / TFdoc

    most_common_words_data.append([tup[0], list_of_meanings(tup[0]), tup[1], y_count, np.round(TFconc, 7) , np.round(TFdoc, 7), MI])
  return sorted(tuple(most_common_words_data), key=lambda element: element[6], reverse=True)

def extract_sentences_with_term(row, column, term):
  doc_text_list = row["lemmata"]
  sentence_words_list = []
  for sentence in [sentence for sentence in row["sentences"] if term in sentence]:
    sentence_words_list.extend(sentence)
  most_common_words = nltk.FreqDist(sentence_words_list).most_common()
  N = len(doc_text_list) ### number of words in the subcorpus
  x_count = doc_text_list.count(term)
  try: Px = x_count / N ### rel.freq. of the key term
  except: Px = 0
  most_common_words_data = []
  for tup in most_common_words:
    TFconc = tup[1] / len(sentence_words_list) ### term frequency (TF)
    y_count = doc_text_list.count(tup[0])
    TFdoc = y_count / N
    MI = TFconc / TFdoc
    most_common_words_data.append([tup[0], list_of_meanings(tup[0]), tup[1], y_count, np.round(TFconc, 7) , np.round(TFdoc, 7), MI])
  return sorted(tuple(most_common_words_data), key=lambda element: element[6], reverse=True)
