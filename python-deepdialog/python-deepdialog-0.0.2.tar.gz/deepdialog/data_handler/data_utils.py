import collections
import string
import re

__ALL__ = ['clean_sentence_fn', 'build_vocab_fn']


def clean_sentence_fn(inputs, lowercase=False, rep_num=False, rep_url=False, rm_punc=False):
    """
    The `clean_sentence_fn` is a function for cleaning texts,
    including transforming words into lowercase, replacing numbers with `<num>` token,
    replacing urls with `<url>` token, and removing punctuations.

    Parameters
    ----------
    inputs: a string or list of strings
        Each string represents a text sentence to be cleaned.
    lowercase: boolean
        If true, transform all words into lowercase. Default to be False.
    rep_num: boolean
        If true, replace numbers with `<num>` token. Default to be False.
    rep_url: boolean
        If true, replace urls with `<url>` token. Default to be False.
    rm_punc: boolean
        If true, remove all punctuation marks. Default to be False.

    Returns
    -------
    outputs: a string or list of strings
        The cleaned sentence/sentences.

    """

    # The sequential order is important.
    def clean_fn(sentence):
        if lowercase:
            sentence = sentence.strip().lower()
        # if rep_url:
        #     sentence = replace_url_fn(sentence)
        if rm_punc:
            remove_punctuation = str.maketrans("", "", string.punctuation)
            sentence = sentence.translate(remove_punctuation)
        if rep_num:
            sentence = replace_num_fn(sentence)
        return sentence

    def replace_num_fn(sentence):

        # This function checks whether a word is a digit.
        # 10: True
        # 3.21: True
        # 9:00: False
        # $10: False
        # 1e3: True
        # -1.37: True
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                pass
            try:
                import unicodedata
                unicodedata.numeric(s)
                return True
            except (TypeError, ValueError):
                pass
            return False

        # This function checks whether a word has digits.
        # All examples above are True.
        def has_number(s):
            return bool(re.search(r'\d', s))

        split = [word if has_number(word) is False else "<num>" for word in sentence.split()]
        return " ".join(split).strip()

    # def replace_url_fn(sentence):
    #     # to-do
    #     return sentence

    if isinstance(inputs, list):
        outputs = []
        for sent in inputs:
            outputs.append(clean_fn(sent))
    elif isinstance(inputs, str):
        outputs = clean_fn(inputs)
    else:
        raise TypeError("inputs should be a string or list of strings.")
    return outputs


def build_vocab_fn(value_list, max_vocab_size=-1, prev_list=[]):
    """
    The `build_vocab_fn` is a function for building vocabulary from data.
    It consists of all unique values of given dataset.

    Parameters
    ----------
    value_list: a list
        A list of values.
    max_vocab_size: an integer
        The maximum number of vocabulary. Default to be -1, which means no limits.
    prev_list: a list
        The prefix list of vocabulary. Usually they are manually-designated special tokens.
        Default to be an empty string.

    Returns
    -------
    word2id: a dict
        A vocabulary dict mapping from words to indexes.
    id2word: a dict
        A vocabulary dict mapping from indexes to words.

    """
    counter = collections.Counter(value_list).most_common()
    value_list, freq_list = zip(*counter)
    vocab_list = prev_list + list(value_list)

    if max_vocab_size != -1:
        vocab_list = vocab_list[:max_vocab_size]

    index_list = range(len(vocab_list))

    word2id = dict(zip(vocab_list, index_list))
    id2word = dict(zip(index_list, vocab_list))

    return word2id, id2word


def load_vocab_fn(vocab_file_path):
    """
    The `load_vocab_fn` loads existing vocabulary from `vocab_path`.

    Parameters
    ----------
    vocab_file_path: a string
        The path of existing vocabulary file ``vocab.txt``.

    Returns
    -------
    word2id: a dict
        A vocabulary dict mapping from words to indexes.
    id2word: a dict
        A vocabulary dict mapping from indexes to words.

    """
    with open(vocab_file_path, mode="r", encoding="utf-8") as file:
        vocab_list = file.read().split("\n")[:-1]

    index_list = range(len(vocab_list))
    word2id = dict(zip(vocab_list, index_list))
    id2word = dict(zip(index_list, vocab_list))

    return word2id, id2word