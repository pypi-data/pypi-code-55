from nltk.translate.bleu_score import sentence_bleu
import numpy as np
from nltk.util import ngrams
import math
# import tensorflow as tf


def average_length(source):
    """
    Calculate the average length among utterances.

    Parameters
    ----------
    source : list
        the element is a String that is an utterance

    Returns
    -------
    average_length : float
    """
    avg_len = float(sum([len(utt.strip().split()) for utt in source])) / len(source)
    return avg_len


def distinct_1(source):
    """
    Calculate the distinct-1 score.

    Distinct-1 means the quotient of the number of unique uni-gram divided by the number of
    all uni-gram. It illustrated the language diversity of the given text.

    Parameters
    ----------
    source : list
        the element is a String that is an utterance

    Returns
    -------
    distinct-1 : float
    """
    words = " ".join(source).split()
    num_distinct_words = len(set(words))
    return float(num_distinct_words) / len(words)


def distinct_2(source):
    """
    Calculate the distinct-2score.

    Distinct-1 means the quotient of the number of unique bi-gram divided by the number of
    all bi-gram. It illustrated the language diversity of the given text.

    Parameters
    ----------
    source : list
        the element is a String that is an utterance

    Returns
    -------
    distinct-2 : float
    """
    all_bigrams = []

    for line in source:
        line_list = line.split()
        bigrams = list(zip(line_list, line_list[1:]))
        all_bigrams.extend(list(bigrams))

    return len(set(all_bigrams)) / float(len(all_bigrams))