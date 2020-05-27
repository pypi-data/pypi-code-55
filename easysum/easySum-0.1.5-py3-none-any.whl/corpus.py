# from __future__ import absolute_import
import spacy

class Corpus:

    def __init__(self):
        self.nlp = spacy.load('ja_ginza')


    def make_sentence_list(self, sentences):
        doc = self.nlp(sentences)
        self.ginza_sents_object = doc.sents
        sentence_list = [s for s in doc.sents]

        return sentence_list


    def make_corpus(self):
        corpus = []
        for s in self.ginza_sents_object:
            # 対象は名詞、副詞、形容詞、動詞のみ。ブレをなくすため基本形を抽出する。
            tokens = [t.lemma_ for t in s if t.pos_ in ('NOUN', 'ADV', 'ADJ', 'VERB')]
            corpus.append(' '.join(tokens) + '。')

        return corpus
