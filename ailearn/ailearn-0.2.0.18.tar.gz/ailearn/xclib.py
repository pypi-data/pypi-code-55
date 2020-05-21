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

import random
import numpy as np
import torch
from torch import nn
import torch.utils.data
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix, lil_matrix, coo_matrix
from xclib.evaluation.xc_metrics import precision, ndcg
from sklearn.preprocessing import normalize
import os
from .utils import data_iter


# set random seeds
def set_seed(seed=0):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class SparseKNeighborsRegressor:
    def __init__(self, n_neighbors=5, weights='distance', metric='cosine', n_jobs=-1):
        self.neighbors_model = NearestNeighbors(n_neighbors=n_neighbors, metric=metric, n_jobs=n_jobs)
        self.weights = weights

    def fit(self, x_train, y_train):
        self.neighbors_model.fit(x_train, y_train)
        self.y_train = y_train

    def predict(self, x_test):
        neigh_dist, neigh_ind = self.neighbors_model.kneighbors(x_test)
        weights = self._get_weights(neigh_dist, self.weights)
        y_pred = lil_matrix((x_test.shape[0], self.y_train.shape[1]))
        denom = np.sum(weights, axis=1)
        for j in range(self.y_train.shape[1]):
            num = np.sum(self.y_train[neigh_ind, j].toarray().reshape(weights.shape) * weights, axis=1)
            y_pred[:, j] = lil_matrix((num / denom).reshape(-1, 1))
        y_pred = csr_matrix(y_pred)
        return y_pred

    def _get_weights(self, dist, weights):
        if weights in (None, 'uniform'):
            return None
        elif weights == 'distance':
            if dist.dtype is np.dtype(object):
                for point_dist_i, point_dist in enumerate(dist):
                    if hasattr(point_dist, '__contains__') and 0. in point_dist:
                        dist[point_dist_i] = point_dist == 0.
                    else:
                        dist[point_dist_i] = 1. / point_dist
            else:
                with np.errstate(divide='ignore'):
                    dist = 1. / dist
                inf_mask = np.isinf(dist)
                inf_row = np.any(inf_mask, axis=1)
                dist[inf_row] = inf_mask[inf_row]
            return dist
        elif callable(weights):
            return weights(dist)
        else:
            raise ValueError("weights not recognized: should be 'uniform', "
                             "'distance', or a callable function")


class Dataset(torch.utils.data.Dataset):
    def __init__(self, feature_matrix, class_matrix=None, use_gpu=False):
        self.num_data_points = feature_matrix.shape[0]
        self.input_dims = feature_matrix.shape[1]
        self.output_dims = feature_matrix.shape[1]
        self.features = feature_matrix
        self.classes = class_matrix
        self.num_workers = 0
        self.use_gpu = use_gpu

    def __len__(self):
        return self.num_data_points

    def __getitem__(self, idx):
        if self.classes is None:
            if type(self.features) != np.ndarray:
                features = torch.from_numpy(self.features[idx].todense()).float().view(-1)
            else:
                features = torch.from_numpy(self.features[idx]).float().view(-1)
            if self.use_gpu:
                return features.cuda()
            else:
                return features
        else:
            if type(self.features) != np.ndarray:
                features = torch.from_numpy(self.features[idx].todense()).float().view(-1)
            else:
                features = torch.from_numpy(self.features[idx]).float().view(-1)
            if type(self.classes) != np.ndarray:
                classes = torch.from_numpy(self.classes[idx].todense()).float().view(-1)
            else:
                classes = torch.from_numpy(self.classes[idx]).float().view(-1)
            if self.use_gpu:
                return features.cuda(), classes.cuda()
            else:
                return features, classes


def get_data_loader(feature_matrix, class_matrix=None, batch_size=None, shuffle=False, use_gpu=False):
    dataset = Dataset(feature_matrix, class_matrix, use_gpu)
    if batch_size is None:
        batch_size = feature_matrix.shape[0]
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    return data_loader


def to_sparse_tensor(matrix):
    matrix = coo_matrix(matrix)
    return torch.sparse.FloatTensor(torch.LongTensor(np.vstack((matrix.row, matrix.col))),
                                    torch.FloatTensor(matrix.data), matrix.shape)


def _single_precision(pred, true, k=5):
    index = pred.argsort()[::-1][:k]
    score = 0
    for i in range(k):
        score += true[index[i]] / k
    return score


def _single_dcg(pred, true, k=5):
    index = pred.argsort()[::-1][:k]
    score = 0
    for i in range(k):
        score += true[index[i]] / np.log2(i + 2) / k
    return score


def _single_ndcg(pred, true, k=5):
    idcg = 0
    for i in range(int(np.minimum(np.sum(true), k))):
        idcg += 1 / np.log2(i + 2) / k
    return _single_dcg(pred, true, k) / idcg


def precision_at_k(pred_label, true_label, ks=(1, 3, 5), average=True):
    if type(pred_label) == csr_matrix:
        pred_label = pred_label.toarray()
    if type(true_label) == csr_matrix:
        true_label = true_label.toarray()
    pred_label, true_label = np.array(pred_label), np.array(true_label)
    scores = {}
    for k in ks:
        scores[k] = 0
        for pred, true in zip(pred_label, true_label):
            scores[k] += _single_precision(pred, true, k)
        if average:
            scores[k] = scores[k] / pred_label.shape[0]
    return scores


def dcg_at_k(pred_label, true_label, ks=(1, 3, 5), average=True):
    if type(pred_label) == csr_matrix:
        pred_label = pred_label.toarray()
    if type(true_label) == csr_matrix:
        true_label = true_label.toarray()
    pred_label, true_label = np.array(pred_label), np.array(true_label)
    scores = {}
    for k in ks:
        scores[k] = 0
        for pred, true in zip(pred_label, true_label):
            scores[k] += _single_dcg(pred, true, k)
        if average:
            scores[k] = scores[k] / pred_label.shape[0]
    return scores


def ndcg_at_k(pred_label, true_label, ks=(1, 3, 5), average=True):
    if type(pred_label) == csr_matrix:
        pred_label = pred_label.toarray()
    if type(true_label) == csr_matrix:
        true_label = true_label.toarray()
    pred_label, true_label = np.array(pred_label), np.array(true_label)
    scores = {}
    for k in ks:
        scores[k] = 0
        for pred, true in zip(pred_label, true_label):
            scores[k] += _single_ndcg(pred, true, k)
        if average:
            scores[k] = scores[k] / pred_label.shape[0]
    return scores
