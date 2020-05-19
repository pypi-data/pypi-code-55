from nltk.translate.bleu_score import sentence_bleu
import numpy as np
from nltk.util import ngrams
import math
# import tensorflow as tf


def BLEU(source, target):
    """

    Calculate the BLEU/BLEU-1/BLEU-2/BLEU-3/BLEU-4 score.

    BLEU (bilingual evaluation understudy) is an algorithm for evaluating the quality of
    text which has been machine-translated from one natural language to another, and is
    also adopted in dialog system.
    Quality is considered to be the correspondence between a machine's response and that of
    a human: "the closer a machine response is to a professional human response,
    the better it is" – this is the central idea behind BLEU.

    The essence of BLEU is to calculate the frequency of the co-occurrence n-gram of two
    sentences, but some techniques are used in the calculation process.

    The following is a simple example for uni-gram:

    candidate: the the the the the the the

    reference1: the cat is on the mat

    reference2: there is a cat on the mat

    The BLEU can be calculated as:

    :math:`BLEU = RefCount / Count`

    :math:`RefCount` is the number of uni-grams in candidate that appear in references.

    :math:`Count` is the number of uni-grams in candidate.

    In this case, BLEU = 7/7 = 1.

    But this result is unreasonable since there is only one uni-gram "the" in candidate
    that is stupid but with a high score. What causes the bad result is that we
    calculate the molecule incorrectly. The improvement is as follows:

    :math:`CountClip_i^j = min(Count_i, RefCount_i^j)`

    :math:`CountClip_i = max(CountClip_i^j), j=1,2,3......`

    :math:`BLEU = sum(CountClip_i)/Count, i=1,2,3......`

    :math:`Count_i` is the number of i-th uni-gram in candidate.

    :math:`CountClip_i^j` is the truncated number of i-th uni-gram in candidate that appears in j-th reference.

    :math:`CountClip_i` is the final truncated number of i-th uni-gram that appears in all references.

    In this case, BLEU = 2/7.

    In the above we have been talking about calculating for uni-gram, now we extend to n-gram in another example.

    candidate: the cat sat on the mat

    reference: the cat is on the mat

    :math:`BLEU-n = sum(CountClip_i(n-gram))/Count(n-gram)`

    In this case, we can get BLEU-1/2/3/4:

    BLEU-1 = 5/6

    BLEU-2 = 3/5

    BLEU-3 = 1/4

    BLEU-4 = 0/3

    However, there is still a problem that is a shorter candidate tend to have a
    higher BLEU score. So we have to introduce a penalty.

    :math:`BP = 1, if c > r`

    :math:`BP = exp(1-r/c), if c <= r`

    where c is the length of candidate, and r is the length of reference.

    The final expression of BLEU with penalty is:

    :math:`BLEU = BP * exp(sum(W_n * log(BLEU-n)))`

    where :math:`W_n` is the weights for n-gram.

    References :
        https://machinelearningmastery.com/calculate-bleu-score-for-text-python/
        https://www.aclweb.org/anthology/P02-1040.pdf

    Parameters
    ----------
    source : list
        the element is a String that is an utterance
    target : list
        the reference to source, the element is a String that is an utterance

    Returns
    -------
    (avg_bleu, avg_bleu_1, avg_bleu_2, avg_bleu_3, avg_bleu_4) : tuple
        a tuple consisting of 4 element: (BLEU-1, BLEU-2, BLEU-3, BLEU-4), the element is float
    """

    assert len(source) == len(target)

    avg_bleu_1 = 0
    avg_bleu_2 = 0
    avg_bleu_3 = 0
    avg_bleu_4 = 0
    avg_bleu = 0
    num_refs = len(target)
    for i in range(num_refs):
        reference = [target[i].lower().split()]
        candidate = source[i].lower().split()
        # todo weights
        bleu = sentence_bleu(reference, candidate, weights=(0.25, 0.25, 0.25, 0.25))
        bleu_1 = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0))
        bleu_2 = sentence_bleu(reference, candidate, weights=(0, 1, 0, 0))
        bleu_3 = sentence_bleu(reference, candidate, weights=(0, 0, 1, 0))
        bleu_4 = sentence_bleu(reference, candidate, weights=(0, 0, 0, 1))
        avg_bleu += bleu
        avg_bleu_1 += bleu_1
        avg_bleu_2 += bleu_2
        avg_bleu_3 += bleu_3
        avg_bleu_4 += bleu_4

    avg_bleu = avg_bleu / len(source)
    avg_bleu_1 = avg_bleu_1 / len(source)
    avg_bleu_2 = avg_bleu_2 / len(source)
    avg_bleu_3 = avg_bleu_3 / len(source)
    avg_bleu_4 = avg_bleu_4 / len(source)

    return avg_bleu, avg_bleu_1, avg_bleu_2, avg_bleu_3, avg_bleu_4


def embedding_average(source, target, word2vec):
    """
    Calculate the embedding_average score.

    Embedding_average reflects the similarity between two sentences by cosine similarity.

    Firstly, all words in two sentences are transformed from string to vectors. Then an average
    value is calculated in every dimension among words. Now two sentences have been
    transformed into two vectors that are finally used to calculated the cosine similarity.

    References :
        https://github.com/chenhongshen/HVMN/blob/master/model/Evaluation/embedding_metrics.py

    Parameters
    ----------
    source : list
        the element is a String that is an utterance
    target : list
        the reference to source, the element is a String that is an utterance
    word2vec : dict
        a dict mapping a word to a vector

    Returns
    -------
    (embedding_average_score, standard_deviation, 1.96*standard_deviation) : tuple
        a tuple consisting of 3 element:(embedding_average_score, standard_deviation, 1.96*standard_deviation)
    """
    assert len(source) == len(target)
    dim = 300
    for _, vec in word2vec.items():
        dim = len(vec)
        break
    scores = []
    for i in range(min(len(source), len(target))):
        tokens1 = source[i].strip().split()
        tokens2 = target[i].strip().split()
        X = np.zeros((dim,))
        for tok in tokens1:
            if tok in word2vec:
                X += word2vec[tok]
        Y = np.zeros((dim,))
        for tok in tokens2:
            if tok in word2vec:
                Y += word2vec[tok]

        # if none of the words have embeddings in source, count result as zero
        if np.linalg.norm(X) < 0.00000000001:
            scores.append(0)
            continue

        # if none of the words in target have embeddings, skip
        if np.linalg.norm(Y) < 0.00000000001:
            continue

        X = np.array(X) / np.linalg.norm(X)
        Y = np.array(Y) / np.linalg.norm(Y)
        o = np.dot(X, Y) / np.linalg.norm(X) / np.linalg.norm(Y)

        scores.append(o)

    scores = np.asarray(scores)
    return np.mean(scores), np.std(scores), 1.96 * np.std(scores)


def embedding_extreme(source, target, word2vec):
    """
    Calculate the embedding_extreme score.

    Embedding_extreme is another algorithm that reflects the similarity between two sentences by cosine similarity.

    Firstly, all words in two sentences are transformed from string to vectors. Then the
    maximum absolute value is selected in every dimension among words. Now two sentences have been
    transformed into two vectors that are finally used to calculated the cosine similarity.

    References :
        https://github.com/chenhongshen/HVMN/blob/master/model/Evaluation/embedding_metrics.py

    Parameters
    ----------
    source : list
        the element is a String that is an utterance
    target : list
        the reference to source, the element is a String that is an utterance
    word2vec : dict
        a dict mapping a word to a vector

    Returns
    -------
    (embedding_extreme_score, standard_deviation, 1.96*standard_deviation) : tuple
        a tuple consisting of 3 element:(embedding_extreme_score, standard_deviation, 1.96*standard_deviation)
    """
    # todo word2vec load
    assert len(source) == len(target)
    scores = []
    for i in range(min(len(source), len(target))):
        tokens1 = source[i].strip().split(" ")
        tokens2 = target[i].strip().split(" ")
        X = []
        for tok in tokens1:
            if tok in word2vec:
                X.append(word2vec[tok])
        Y = []
        for tok in tokens2:
            if tok in word2vec:
                Y.append(word2vec[tok])

        # if none of the words have embeddings in source, count result as zero
        if np.linalg.norm(X) < 0.00000000001:
            scores.append(0)
            continue

        # if none of the words in target have embeddings, skip
        if np.linalg.norm(Y) < 0.00000000001:
            continue

        xmax = np.max(X, 0)  # get positive max
        xmin = np.min(X, 0)  # get abs of min
        xtrema = []
        for i in range(len(xmax)):
            if np.abs(xmin[i]) > xmax[i]:
                xtrema.append(xmin[i])
            else:
                xtrema.append(xmax[i])
        X = np.array(xtrema)  # get extrema

        ymax = np.max(Y, 0)
        ymin = np.min(Y, 0)
        ytrema = []
        for i in range(len(ymax)):
            if np.abs(ymin[i]) > ymax[i]:
                ytrema.append(ymin[i])
            else:
                ytrema.append(ymax[i])
        Y = np.array(ytrema)

        o = np.dot(X, Y) / np.linalg.norm(X) / np.linalg.norm(Y)

        scores.append(o)

    scores = np.asarray(scores)
    return np.mean(scores), np.std(scores), 1.96 * np.std(scores)


def embedding_greedy(source, target, word2vec):
    """
    Calculate the embedding_greedy score.

    Embedding_greedy is another algorithm that reflects the similarity between two sentences by cosine similarity.

    Firstly, all words in two sentences are transformed from string to vectors. Secondly, for
    the i-th word in the first sentence, we calculate the maximum cosine similarity between
    it and all words in the second sentence. Now the first sentence has m cosine similarity
    (m is the length of the first sentence). Thirdly, an average value is calculated in these
    cosine similarity. Then we do the same operation for the second sentence. Now there are
    two cosine similarity and the mean of them is the final result.

    References :
        https://github.com/chenhongshen/HVMN/blob/master/model/Evaluation/embedding_metrics.py

    Parameters
    ----------
    source : list
        the element is a String that is an utterance
    target : list
        the reference to source, the element is a String that is an utterance
    word2vec : dict
        a dict mapping a word to a vector

    Returns
    -------
    (embedding_greedy_score, standard_deviation, 1.96*standard_deviation) : tuple
        a tuple consisting of 3 element:(embedding_greedy_score, standard_deviation, 1.96*standard_deviation)
    """
    assert len(source) == len(target)
    embedding_greedy_score = []
    for i in range(len(source)):
        sentence1 = source[i].strip().split()
        sentence2 = target[i].strip().split()

        greedy_1 = greedy_score(sentence1, sentence2, word2vec)
        greedy_2 = greedy_score(sentence2, sentence1, word2vec)

        embedding_greedy_score.append((greedy_1 + greedy_2) / 2)

    return np.mean(embedding_greedy_score), \
           np.std(embedding_greedy_score), \
           1.96 * np.std(embedding_greedy_score)


def greedy_score(source, target, word2vec):
    """
    The function to be called by embedding_greedy() function and actually executes
    the algorithm given two sentence. The embedding_greedy() function calculate the
    mean and variance score among a batch data.

    Parameters
    ----------
    source : list
        the element is a String that is a word
    target : list
        the reference to source, the element is a String that is a word
    word2vec : dict
        a dict mapping a word to a vector

    Returns
    -------
    greedy_score : float
        the greedy score
    """
    cosine_list = []
    word_count = 0

    Y = []
    for tok in target:
        if tok in word2vec:
            Y.append(word2vec[tok])
    if len(Y) == 0:
        return 0.0

    for tok in source:
        if tok in word2vec:
            i_vector = word2vec[tok]
        else:
            continue

        word_count += 1
        cosine_list.append(max_cosine(i_vector, Y))

    if word_count == 0:
        return 0.0

    score = sum(cosine_list) / word_count
    return score


def max_cosine(vector, vector_list):
    """
    The function to help to calculate the embedding_greedy. It executes the second
    operation described in embedding_greedy() function.

    Parameters
    ----------
    vector : list
        the element is a float
    vector_list : list
        With 2 dimension, the element in axis0 is a list, the element in axis1 is a float

    Returns
    -------
    max_cosine : float
        the max cosine
    """
    max_value = 1e-10
    for i in vector_list:
        cosine_similarity = np.dot(vector, i) / np.linalg.norm(vector) / np.linalg.norm(i)
        max_value = max(cosine_similarity, max_value)
    return max_value

def WER(source, target):
    """
    Calculate the word error rate.

    Word error rate (WER) is a common metric of the performance of a speech recognition
    or machine translation system, and is also adopted in dialog system. It actually is
    calculated as the edit distance divided by the length of reference.

    The edit distance is  edit distance is a way of quantifying how dissimilar two
    strings (e.g., words) are to one another by counting the minimum number of operations
    required to transform one string into the other. For WER, operations are removal,
    insertion, or substitution of a word in the sentence.


    References :
        https://blog.csdn.net/quheDiegooo/article/details/56834417
        https://www.csie.ntu.edu.tw/~b93076/Computation%20of%20Normalized%20Edit%20Distance%20and%20Applications.pdf

    Parameters
    ----------
    source : list
        the element is a String that is an utterance
    target : list
        the reference to source, the element is a String that is an utterance

    Returns
    -------
    (word_error_rate, standard_deviation, 1.96*standard_deviation) : tuple
    """
    assert len(source) == len(target)
    wer_list = []
    for i in range(len(source)):
        s = source[i].strip().split()
        t = target[i].strip().split()
        s_len = len(s)
        t_len = len(t)
        edit_dis = edit_distance(s, t)
        wer_list.append(float(edit_dis) / t_len)
        """
        not_equal = 0
        for j in range(t_len):
            if j < s_len:
                not_equal += 0 if s[j] == t[j] else 1
            else:
                not_equal += 1
        wer_list.append(float(not_equal) / t_len)
        """
    wers = np.asarray(wer_list)

    return np.mean(wers), np.std(wers), 1.96 * np.std(wers)


def edit_distance(source, target):
    """
    Calculate the edit distance between two lists or two Strings.

    The edit distance is  edit distance is a way of quantifying how dissimilar two
    strings (e.g., words) are to one another by counting the minimum number of operations
    required to transform one string into the other. For WER, operations are removal,
    insertion, or substitution of a word in the sentence.

    References :
        https://leetcode-cn.com/problems/edit-distance/solution/bian-ji-ju-chi-by-leetcode/

    Parameters
    ----------
    source : list or String
    target : list or String

    Returns
    -------
    edit_distance : int
    """
    n = len(source)
    m = len(target)

    # if one of the utterance is empty
    if n * m == 0:
        return n + m

    # array to store the convertion history
    d = [[0] * (m + 1) for _ in range(n + 1)]

    # init boundaries
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j

    # DP compute
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            left = d[i - 1][j] + 1
            down = d[i][j - 1] + 1
            left_down = d[i - 1][j - 1]
            if source[i - 1] != target[j - 1]:
                left_down += 1
            d[i][j] = min(left, down, left_down)

    return d[n][m]