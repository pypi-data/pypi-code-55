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
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
from .utilities import warn


# K-fold cross validation
def cross_val_score(estimator, x, y, k=10, verbose=True, random_state=None, **kwargs):
    '''
    :param estimator: Model to be evaluated
    :param x: Features Matrix
    :param y: Labels Matrix
    :param k: K value in K-fold cross validation
    :param verbose: Show validation process or not
    :param random_state: Random number seed of data set segmentation
    :param kwargs: parameters of estimator.fit()
    :return: numpy.ndarray of k-test accuracy
    '''
    x, y = np.array(x), np.array(y)
    if random_state is None:
        folder = StratifiedKFold(k, True)
    else:
        folder = StratifiedKFold(k, True, random_state)
    scores = []
    for i, (train_index, test_index) in enumerate(folder.split(x, y)):
        estimator.fit(x[train_index], y[train_index], **kwargs)
        score = estimator.score(x[test_index], y[test_index])
        scores.append(score)
        if verbose:
            print('Cross validation iteration %d was completed with a score of %.4f' % (i + 1, score))
    scores = np.array(scores)
    return scores


# P-RETENTION method
def leave_p_score(estimator, x, y, p=1, verbose=True, **kwargs):
    '''
    :param estimator: Model to be evaluated
    :param x: Features Matrix
    :param y: Labels Matrix
    :param p: P value in the cross validation of P-RETENTION method
    :param verbose: Show validation process or not
    :param kwargs: parameters of estimator.fit()
    :return: numpy.ndarray, accuracies of shape (len(x)//p,)
    '''
    x, y = np.array(x), np.array(y)
    if x.shape[0] < p:
        warn('Cross validation parameter error, no operation has done!')
        return None
    epoch = x.shape[0] // p
    index = np.arange(x.shape[0])
    np.random.shuffle(index)
    scores = []
    for i in range(epoch):
        test_index = slice(i * p, (i + 1) * p)
        train_index = np.delete(index, test_index)
        estimator.fit(x[train_index], y[train_index], **kwargs)
        score = estimator.score(x[test_index], y[test_index])
        scores.append(score)
        if verbose:
            print('Cross validation iteration %d was completed with a score of %.4f' % (i + 1, score))
    scores = np.array(scores)
    return scores


# Hold out test
def hold_out_score(estimator, x, y, test_size=0.25, shuffle=True, stratify=None, random_state=0, **kwargs):
    '''
    :param estimator: Model to be evaluated
    :param x: Features Matrix
    :param y: Labels Matrix
    :param test_size: Test data ratio
    :param shuffle: Whether or not to shuffle the data before splitting
    :param stratify: Stratified sampling or not (general input y)
    :param random_state: Random number seed of data set segmentation
    :param kwargs: parameters of estimator.fit()
    :return: accuracy
    '''
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, shuffle=shuffle, stratify=stratify,
                                                        random_state=random_state)
    estimator.fit(x_train, y_train, **kwargs)
    return estimator.score(x_test, y_test)


# Classification Report
def class_report(y_pred, y_true, method='weighted'):
    '''
    :param y_pred: true label
    :param y_true: prediction label
    :param method: Reporting method, ['weighted', 'micro', 'macro']
    :return: Classification report dictionary
    '''
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    accuracy = np.mean(y_true == y_pred)
    cm = confusion_matrix(y_true, y_pred)  # Confusion matrix
    _, _, _, num = precision_recall_fscore_support(y_true, y_pred)  # Num is a list of samples of each class
    n_classes = len(num)
    n_samples = len(y_true)
    TP, FN, FP, TN = np.zeros([n_classes], int), np.zeros([n_classes], int), np.zeros([n_classes], int), np.zeros(
        [n_classes], int)  # TP, FN, FP, TN of each label
    precision, recall, recall_, F1_score, G_mean = np.zeros([n_classes]), np.zeros([n_classes]), np.zeros(
        [n_classes]), np.zeros([n_classes]), np.zeros(
        [n_classes])  # precision, recall rate, negative recall rate, F1 value, g-mean value of each label
    # Micro average
    if method == 'micro':
        for i in range(n_classes):
            TP[i] = cm[i][i]
            FP[i] = np.sum(cm[:, i]) - TP[i]
            FN[i] = np.sum(cm[i]) - TP[i]
            TN[i] = n_samples - TP[i] - FP[i] - FN[i]
        TP, FP, FN, TN = np.mean(TP), np.mean(FP), np.mean(FN), np.mean(TN)
        if TP == 0 and FP == 0:
            precision = 0
        else:
            precision = TP / (TP + FP)
        if TP == 0 and FN == 0:
            recall = 0
        else:
            recall = TP / (TP + FN)
        if TN == 0 and FP == 0:
            recall_ = 0
        else:
            recall_ = TN / (TN + FP)
        if recall == 0 and precision == 0:
            F1_score = 0
        else:
            F1_score = 2 * precision * recall / (precision + recall)
        if recall == 0 and recall_ == 0:
            G_mean = 0
        else:
            G_mean = np.sqrt(recall * recall_)
        return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'F1_score': F1_score, 'G_mean': G_mean}

    # Macro average or weighted average
    elif method == 'macro' or method == 'weighted':
        for i in range(n_classes):
            TP[i] = cm[i][i]
            FP[i] = np.sum(cm[:, i]) - TP[i]
            FN[i] = np.sum(cm[i]) - TP[i]
            TN[i] = n_samples - TP[i] - FP[i] - FN[i]
            if TP[i] == 0 and FP[i] == 0:
                precision[i] = 0
            else:
                precision[i] = TP[i] / (TP[i] + FP[i])
            if TP[i] == 0 and FN[i] == 0:
                recall[i] = 0
            else:
                recall[i] = TP[i] / (TP[i] + FN[i])
            if TN[i] == 0 and FP[i] == 0:
                recall_[i] = 0
            else:
                recall_[i] = TN[i] / (TN[i] + FP[i])
            if recall[i] == 0 and precision[i] == 0:
                F1_score[i] = 0
            else:
                F1_score[i] = 2 * precision[i] * recall[i] / (precision[i] + recall[i])
            if recall[i] == 0 and recall_[i] == 0:
                G_mean[i] = 0
            else:
                G_mean[i] = np.sqrt(recall[i] * recall_[i])
        if method == 'macro':
            precision = np.mean(precision)
            recall = np.mean(recall)
            F1_score = np.mean(F1_score)
            G_mean = np.mean(G_mean)
            return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'F1_score': F1_score,
                    'G_mean': G_mean}
        else:
            precision = np.sum(precision * num) / n_samples
            recall = np.sum(recall * num) / n_samples
            F1_score = np.sum(F1_score * num) / n_samples
            G_mean = np.sum(G_mean * num) / n_samples
            return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'F1_score': F1_score,
                    'G_mean': G_mean}

    else:
        print('Classification report type error!')
