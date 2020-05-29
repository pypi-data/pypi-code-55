import spacy
import neologdn
import re
import emoji
import mojimoji

class JapaneseCorpus:

    def __init__(self):
        self.nlp = spacy.load('ja_ginza')


    def preprocessing(self, text):
        text = re.sub(r'\n', "", text)
        text = re.sub(r'\r', "", text)
        text = re.sub(r'\s', "", text)
        text = text.lower()
        text = mojimoji.zen_to_han(text, kana=True)
        text = mojimoji.han_to_zen(text, digit=False, ascii=False)
        text = neologdn.normalize(text)
        text = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "" , text)
        text = re.sub(r"#(\w+)", "" , text)
        text = re.sub(r"@([A-Za-z0-9_]+) ", "" , text)
        text = ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)
        text = text.strip()

        return text


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



class EnglishCorpus(JapaneseCorpus):

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')


    def preprocessing(self, text):
        text = re.sub(r'\n', "", text)
        text = re.sub(r'\r', "", text)
        text = text.lower()
        text = mojimoji.han_to_zen(text, digit=False, ascii=False)
        text = mojimoji.zen_to_han(text, kana=True)
        text = neologdn.normalize(text)
        text = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "" , text)
        text = re.sub(r"#(\w+)", "" , text)
        text = re.sub(r"@([A-Za-z0-9_]+) ", "" , text)
        text = ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)
        text = text.strip()

        return text


    def make_corpus(self):
        corpus = []
        for s in self.ginza_sents_object:
            # 対象は名詞、副詞、形容詞、動詞のみ。ブレをなくすため基本形を抽出する。
            tokens = [str(t) for t in s]
            corpus.append(' '.join(tokens))

        return corpus
