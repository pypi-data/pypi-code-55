# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/5/15 14:50
"""

from collections import Iterable

import numpy as np

DISCOUNTS = np.log2(np.arange(1000) + 2)

def dcg_score(y_true, y_score, k=10, gains="exponential"):
    if not isinstance(y_true, np.ndarray):
        y_true = np.array(y_true)
        y_score = np.array(y_score)

    order = np.argsort(y_score)[::-1]
    y_true = np.take(y_true, order[:k])

    if gains == "exponential":
        gains = 2 ** y_true - 1
    elif gains == "linear":
        gains = y_true
    else:
        raise ValueError("Invalid gains option.")

    # highest rank is 1 so +2 instead of +1
    if len(y_true) < 1000:
        discounts = DISCOUNTS[:len(y_true)]
    else:
        discounts = np.log2(np.arange(len(y_true)) + 2)
    return np.sum(gains / discounts)


def ndcg_score(y_true, y_score, k=10, gains="exponential"):
    """
    calculate ndcg for one query with top k
    """
    indices_real = y_true >= 0
    y_true = y_true[indices_real]
    y_score = y_score[indices_real]
    best = dcg_score(y_true, y_true, k, gains)
    actual = dcg_score(y_true, y_score, k, gains)
    return actual / best if best != 0 else 0


def get_keys(ks, prefix='ndcg@', suffix=''):
    return [prefix + str(k) + suffix for k in ks]


def ndcg_with_array(y_true, y_pred, ks_ndcg):
    res = []
    for k in ks_ndcg:
        res_ndcg = [ndcg_score(y_true[i], y_pred[i], k) for i in
                    range(len(y_true))]
        res.append(np.mean(res_ndcg))
    ndcgs = dict(zip(get_keys(ks_ndcg), res))
    return ndcgs


def ndcg_with_groups(y_true, y_pred, groups, ks_ndcg):
    right = 0
    res = []
    for group in groups:
        left = right
        right = left + group
        y_true_, y_pred_ = y_true[left:right], y_pred[left:right]
        res.append([ndcg_score(y_true_, y_pred_, k) for k in ks_ndcg])
    ndcgs_values = np.mean(res, axis=0)
    ndcgs = dict(zip(get_keys(ks_ndcg), ndcgs_values))
    return ndcgs


def ndcgs(y_true, y_pred, groups=None, ks_ndcg=None):
    """
    Calculate the ndcgs for ranking task.
    :param y_true:
    :param y_pred:
    :param groups: if y_true and y_pred are one dimensional arrays,  groups should be provided.
        groups is an array of the size of the documents for each query.
    :param ks_ndcg: optional, int or Iterable of int, default [1,3,5,10]
    :return: dict of ndcgs like {'ndcg@10':0.5}
    """
    if ks_ndcg is None:
        ks_ndcg = [1, 3, 5, 10]
    if not isinstance(ks_ndcg, Iterable):
        ks_ndcg = list([ks_ndcg])

    if groups is None:
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        assert len(y_true.shape) == 2
        assert y_true.shape == y_pred.shape
        return ndcg_with_array(y_true, y_pred, ks_ndcg)
    else:
        y_true = np.squeeze(y_true)
        y_pred = np.squeeze(y_pred)
        assert len(y_true) == np.sum(groups)
        assert len(y_true) == len(y_pred)
        return ndcg_with_groups(y_true, y_pred, groups, ks_ndcg)


class NdcgWithGroup():
    """
    To save the ideal dcg score for multiple evaluations.
    """
    def __init__(self, y_true, groups, ks_ndcg=None, gains="exponential"):
        if ks_ndcg is None: ks_ndcg = [1, 3, 5, 10]
        if not isinstance(ks_ndcg, Iterable): ks_ndcg = [ks_ndcg]
        self.y_true = y_true
        self.groups = groups
        self.ks_ndcg = ks_ndcg
        self.gains = gains
        self.best = {}
        self.best = self.cal_dcgs(self.y_true)

    def cal_dcgs(self, cur_labels):
        right = 0
        dcgs = {}
        for group in self.groups:
            left = right
            right = left + group
            y_true_ = cur_labels[left:right]
            for k in self.ks_ndcg:
                it = dcgs.setdefault(k, [])
                it += [dcg_score(self.y_true[left:right], y_true_, k, gains=self.gains)]
        return dcgs

    def _get_ndcgs(self, dcg_best, dcg_pred):
        ndcg = np.mean([dcg_pred[i] / dcg_best[i] if dcg_best[i] != 0 else 0 for i in range(len(dcg_best))])
        return ndcg

    def ndcg_score(self, y_pred):
        assert len(self.y_true) == len(y_pred)
        actual = self.cal_dcgs(y_pred)
        ndcgs_values = []
        for k in self.ks_ndcg:
            ndcgs_values += [self._get_ndcgs(self.best[k], actual[k])]
        ndcgs = dict(zip(get_keys(self.ks_ndcg), ndcgs_values))
        return ndcgs
