# Copyright 2018 Zhao Xingyu & An Yuexuan. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import random
from scipy import stats


# print with warn format
def warn(msg):
    print('\033[1;31m%s\033[0m' % msg)


# data iteration
def data_iter(data, label=None, batch_size=32, shuffle=False):
    n_samples = data.shape[0]
    idx = list(range(n_samples))
    if shuffle:
        random.shuffle(idx)
    if label is None:
        for i in range(0, n_samples, batch_size):
            j = np.array(idx[i:min(i + batch_size, n_samples)])
            if type(data) is not np.ndarray:
                yield data[j].toarray()
            else:
                yield data[j]
    else:
        for i in range(0, n_samples, batch_size):
            j = np.array(idx[i:min(i + batch_size, n_samples)])
            if type(data) is not np.ndarray:
                yield data[j].toarray(), label[j]
            else:
                yield data[j], label[j]


# digital labels to one-hot encoder
def to_categorical(label, num_classes=None):
    label = np.array(label, dtype='int')
    if num_classes is not None:
        assert num_classes > label.max()  # wrong number of labels
    else:
        num_classes = label.max() + 1
    if len(label.shape) == 1:
        y = np.eye(num_classes, dtype='int64')[label]
        return y
    elif len(label.shape) == 2 and label.shape[1] == 1:
        y = np.eye(num_classes, dtype='int64')[label.squeeze()]
        return y
    else:
        warn('Warning: one_hot_to_label do not work')
        return label


# one-hot encoder to digital labels
def one_hot_to_label(y):
    y = np.array(y)
    if len(y.shape) == 2 and y.max() == 1 and y.sum(1).mean() == 1:
        return y.argmax(1)
    else:
        warn('Warning: one_hot_to_label do not work')
        return y


# Friedman test
def Friedman_test(x, alpha=0.05, ranked=False, use_f_distribution=False, verbose=False):
    '''
    :param x: Score or sort of each algorithm on different data sets, [number of data sets, number of algorithms]
    :param alpha: Significance level
    :param ranked: Whether the input data is sorting
    :param use_f_distribution: Whether to use improved Friedman detection
    :param verbose: Print sorting results when the input data is score
    :return: Sorting of algorithms
    '''
    x = np.array(x) + 0.
    n_datasets, n_algorithms = x.shape[0], x.shape[1]
    if not ranked:  # Enter as score
        for i in range(n_datasets):  # For the ith dataset
            rank_list = np.zeros([n_algorithms])  # Ranking of different algorithms
            score = x[i].copy()
            chuli = 0
            while chuli != n_algorithms:
                M = np.max(score)
                score_equal = []
                for j in range(n_algorithms):
                    if score[j] == M:
                        score_equal.append(j)
                rank_list[score_equal] = np.sum(np.arange(chuli + 1, chuli + 1 + len(score_equal))) / len(score_equal)
                score[score_equal] = -np.inf
                x[i] = rank_list.copy()
                chuli += len(score_equal)
        if verbose:
            print('Enter the score ranking as: ')
            print(x)
    R = np.mean(x, axis=0)
    Tao = 12 * n_datasets / n_algorithms / (n_algorithms + 1) * np.sum(np.square(R - (n_algorithms + 1) / 2))
    if use_f_distribution:  # Using improved Friedman detection
        F = stats.f.isf(q=alpha, dfn=(n_algorithms - 1), dfd=int(n_algorithms - 1) * (n_datasets - 1))
        Tao = (n_datasets - 1) * Tao / (n_datasets * (n_algorithms - 1) - Tao)
        if Tao > F:
            print(
                'Tao value is %.4f, F distribution value of significance level %.4f is %.4f, there is significant difference' % (
                    Tao, alpha, F))
        else:
            print(
                'Tao value is %.4f, F distribution value of significance level %.4f is %.4f, there is no significant difference' % (
                    Tao, alpha, F))
    else:  # Using traditional Friedman detection
        Chi2 = stats.chi2.isf(q=alpha, df=n_algorithms - 1)
        if Tao > Chi2:
            print(
                'Tao value is %.4f, Chi2 distribution value of significance level %.4f is %.4f, there is significant difference' % (
                    Tao, alpha, Chi2))
        else:
            print(
                'Tao value is %.4f, Chi2 distribution value of significance level %.4f is %.4f, there is no significant difference' % (
                    Tao, alpha, Chi2))
    return x


# t-test
def t_test(x1=None, x2=None, alpha=0.05, from_stats=False, mean1=None, std1=None, nobs1=None, mean2=None, std2=None,
           nobs2=None):
    '''
    :param x1: Group 1 Accuracy,list or numpy.array
    :param x2: Group 2 Accuracy,list or numpy.array
    :param alpha: Significance level
    :param from_stats: Whether the input parameter is a statistical parameter
    :param mean1: Mean value of the first group of samples
    :param std1: Variance of the first set of samples
    :param nobs1: Number of samples in the first group
    :param mean2: Mean value of the second group of samples
    :param std2: Variance of the second group of samples
    :param nobs2: Number of samples in the second group
    :return: Significance value
    '''
    if from_stats:
        std1, std2 = np.sqrt(nobs1 / (nobs1 - 1)) * std1, np.sqrt(nobs2 / (nobs2 - 1)) * std2
        statistic, pvalue = stats.ttest_ind_from_stats(mean1=mean1, std1=std1, nobs1=nobs1, mean2=mean2, std2=std2,
                                                       nobs2=nobs2)
    else:
        x1, x2 = np.array(x1), np.array(x2)
        statistic, pvalue = stats.levene(x1, x2)
        print(pvalue)
        if pvalue > 0.05:
            equal_val = True
        else:
            equal_val = False
        statistic, pvalue = stats.ttest_ind(x1, x2, equal_var=equal_val)
    if pvalue > alpha:
        print('pvalue is %.4f, significance level is %.4f, there is no significant difference' % (pvalue, alpha))
    else:
        print('pvalue is %.4f, significance level is %.4f, there is significant difference' % (pvalue, alpha))
    return pvalue
