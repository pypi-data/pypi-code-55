from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
# algorithms
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.reduction import ReductionSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer

from .modules.preprocessing import preprocessing
from .modules.corpus import Corpus


algorithm_dic = {"lex": LexRankSummarizer(), "tex": TextRankSummarizer(), "lsa": LsaSummarizer(),\
                 "kl": KLSummarizer(), "luhn": LuhnSummarizer(), "redu": ReductionSummarizer(),\
                 "sum": SumBasicSummarizer()}


def summarize_sentences(sentences, sentences_count=3, algorithm="lex"):
    corpus_maker = Corpus()

    preprocessed_sentences = preprocessing(sentences)
    preprocessed_sentence_list = corpus_maker.make_sentence_list(preprocessed_sentences)

    corpus = corpus_maker.make_corpus()

    parser = PlaintextParser.from_string(''.join(corpus), Tokenizer('japanese'))

    # アルゴリズム選択
    try:
        summarizer = algorithm_dic[algorithm]
    except KeyError:
        print("algorithm name:'{}'is not found.".format(algorithm))

    summarizer.stop_words = [' ']

    summary = summarizer(document=parser.document, sentences_count=sentences_count)

    return "".join([str(preprocessed_sentence_list[corpus.index(sentence.__str__())]) for sentence in summary])
