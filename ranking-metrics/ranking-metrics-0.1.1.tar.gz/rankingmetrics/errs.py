# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/5/15 14:51
"""

from collections import Iterable

import numpy as np


def err_with_sorted(y_true_sorted, max_score):
    err_ = 0.
    prob_pre_step = 1.
    ERRS = []
    for idx, rel in enumerate(y_true_sorted):
        idx += 1
        utility = (np.power(2, rel) - 1) / np.power(2, max_score)
        err_ += prob_pre_step * utility / idx
        prob_pre_step *= 1 - utility
        ERRS.append(err_)
    return ERRS


def get_keys(ks, prefix='ndcg@', suffix=''):
    return [prefix + str(k) + suffix for k in ks]


def err_one_query(y_true, y_pred, ks, max_score):
    max_k = ks[-1]
    indices = np.argsort(y_pred)[::-1][:max_k]
    y_true = y_true[indices]
    ERRS = err_with_sorted(y_true, max_score)
    return [ERRS[k - 1] for k in ks]


def err_with_array(y_true, y_pred, max_score, ks_err):
    res_err = [err_one_query(y_true[i], y_pred[i], ks_err, max_score) for i in
               range(len(y_true))]
    res_err = np.mean(res_err, axis=0)
    ndcgs = dict(zip(get_keys(ks_err), res_err))
    return ndcgs


def err_with_groups(y_true, y_pred, max_score, groups, ks_errs):
    right = 0
    res = []
    for group in groups:
        left = right
        right = left + group
        y_true_, y_pred_ = y_true[left:right], y_pred[left:right]
        res.append([err_one_query(y_true_, y_pred_, k, max_score) for k in ks_errs])
    errs_values = np.mean(res, axis=0)
    errs = dict(zip(get_keys(ks_errs), errs_values))
    return errs


def errs(y_true, y_pred, max_score, groups=None, ks_errs=None):
    if ks_errs is None:
        ks_errs = [1, 3, 5, 10]
    if not isinstance(ks_errs, Iterable):
        ks_errs = list([ks_errs])

    if groups is None:
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        assert len(y_true.shape) == 2
        assert y_true.shape == y_pred.shape
        return err_with_array(y_true, y_pred, max_score, ks_errs)
    else:
        y_true = np.squeeze(y_true)
        y_pred = np.squeeze(y_pred)
        assert len(y_true) == np.sum(groups)
        assert len(y_true) == len(y_pred)
        return err_with_groups(y_true, y_pred, max_score, groups, ks_errs)
