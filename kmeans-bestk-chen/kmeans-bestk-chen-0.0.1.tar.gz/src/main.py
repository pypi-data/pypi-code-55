#!/usr/bin/env python
# coding: utf-8

# this is for baylor code assignment. 
# K means 

import numpy as np

def init_clusters(k, points):
    return points[np.random.randint(points.shape[0], size=k)]

def cal_distances(centroid, points):
    return np.linalg.norm(points - centroid, axis=1)

def k_means(k, points, max_iter = 100):
    centroids = init_clusters(k, points)
    costs = np.zeros(max_iter, dtype=np.float64)
    classes = np.zeros(points.shape[0], dtype=np.float64)
    distances = np.zeros([points.shape[0], k], dtype=np.float64)
    for idx in range(max_iter):
        for i,c in enumerate(centroids):
            distances[:, i] = cal_distances(c, points)
        classes = np.nanargmin(distances, axis = 1)
        costs[idx] = np.sum(np.nanmin(distances, axis = 1) , dtype=np.float64) / points.shape[0]
        for c in range(k):
            centroids[c] = np.mean(points[classes == c], axis = 0)
    return classes, costs[-1], centroids, classes

def find_bestK(X, min_k = 2, max_k = 31):
    pre_improve = None
    pre_cost = None
    cur_cost = None
    improve = None
    costs = []
    ks = []
    for k in range(min_k, max_k):
        classes, cur_cost, centroids, classes = k_means(k, X, 10)
        ks.append(k)
        costs.append(cur_cost)
    return k, cur_cost, ks,costs

def shortest_distance(point, coef):    
    return abs((coef[0]*point[0])-point[1]+coef[1])/ ((coef[0]*coef[0])+1)**0.5

def load_file(X):
    return np.loadtxt(X)

def set_data_dir(X):
    global data_dir
    data_dir = X if X.endswith('/') else X + '\\'
    
def set_file_name(X):
    global file_name
    file_name = X

def gen_new_file(X,k):
    tmp = X.split('.')
    name = tmp[0]
    out_file = name + '_' + str(k) + '.' + tmp[1]
    np.save(out_file, k)
    
def run(data_dir, file):
    cs = []
    ks = []
    full_file = data_dir + file
    data = load_file(full_file)
    k, c, ks, cs = find_bestK(data)
    co = np.polyfit((ks[0],ks[-1]),(cs[0],cs[-1]),1)
    best_k = None
    long_dis = float('-inf')
    for k,c in zip(ks,cs):
        d = shortest_distance((k,c),co)
        if d > long_dis:
            long_dis = d
            best_k = k
    print("Best k:" + str(best_k))
    gen_new_file(file,best_k)

data_dir = '.'
file_name = None
set_data_dir("../datasets/")
set_file_name("0.txt")
run(data_dir, file_name)

