from nltk.translate.bleu_score import sentence_bleu
import numpy as np
from nltk.util import ngrams
import math
import tensorflow as tf


def Hw(source, token_prob, ngram):
    """
    Calculate the average trigram word entropy.

    This measurement is to evaluate the informativeness of the response (contrast with
    the general dull and ’safe’ responses).

    In particular, for a word :math:`w_n` in a response :math:`U` , the trigram word
    entropy is defined as:

    :math:`H(w_n) = -p(w_n|w_n-2, w_n-1)log(p(w_n|w_n-2, w_n-1))`

    References:
        https://dl.acm.org/doi/10.1145/3178876.3186077
        https://github.com/chenhongshen/HVMN/blob/master/model/Evaluation/entutil.py

    Parameters
    ----------
    source : list
        the element is a String that is an utterance and ends with "<eos>"
    token_prob : dict
        probabilities of unigram or bigram or trigram
    ngram : int
        1 for unigram, 2 for bigram, 3 fro trigram

    Returns
    -------
    average_word_entropy : float
    """
    word_entropy = []
    for line in source:
        if ngram == 1:
            word_list = line.split()
        elif ngram == 2:
            word_list = ["<sos>"] + line.split()
        elif ngram == 3:
            word_list = ["<sos>", "<sos>"] + line.split()
        else:
            assert ValueError("invalid ngram")

        if ngram == 1:
            ngram_list = word_list
        else:
            ngram_list = [" ".join(ngram_tuple) for ngram_tuple in ngrams(word_list, ngram)]
        for ngram_token in ngram_list:
            if ngram_token in token_prob:
                prob = token_prob[ngram_token]
            else:
                prob = token_prob["<new>"]
            word_entropy.append(-prob * math.log(prob, 2))
    return np.mean(word_entropy)


def perplexity(source_prob, target, target_mask, vocab_size):
    """
    Calculate the perplexity.

    In information theory, perplexity is a measurement of how well a probability
    distribution or probability model predicts a sample. It may be used to compare
    probability models. A low perplexity indicates the probability distribution is good
    at predicting the sample.

    The perplexity of a discrete probability distribution p is defined as:

    :math:`PPL = exp(-sum(p(x) * log(p(x))))`

    References:
        https://en.wikipedia.org/wiki/Perplexity

    Parameters
    ----------
    source_prob : tf.tensor
        probabilities of word generated from decoder, the shape is (batch_size * sequence_length * vocab_size)
    target : tf.tensor
        the tokenized response, the shape is (batch_size * sequence_length)
    target_mask : tf.tensor
        it implys the real length of target, the element is 0 or 1, 0 means no word, 1 means a word
    vocab_size : int
        the size of vocabulary

    Returns
    -------
    perplexity : tf.tensor
    """
    onehot_target = tf.one_hot(target, vocab_size)
    cross_entropy = -tf.reduce_sum(onehot_target * tf.log(source_prob), axis=-1)
    target_mask = tf.cast(target_mask, dtype=tf.float32)
    total_words = tf.reduce_sum(target_mask) + tf.constant(1e-10)
    avg_cross_entropy = tf.reduce_sum(cross_entropy * target_mask) / total_words
    return tf.exp(avg_cross_entropy)


def BERTScore(source, target):
    """
    Calculate the BERT score.

    BERTScore computes a similarity score for each token in the candidate sentence
    with each token in the reference sentence using contextual embeddings gotten from
    BERT model.

    References:
        https://arxiv.org/abs/1904.09675

    Parameters
    ----------
    source : list or String
    target : list or String

    Returns
    -------
    BERT_score : float
    """
    pass