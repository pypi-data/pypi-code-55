# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 15:52:52 2017

"""

from sklearn import datasets
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.datasets import make_blobs
import SimpSOM as sps
import matplotlib.pyplot as plt

### DS2L-SOM

from ml.densityclust.DS2L_SOM import Rel_den_clust

## Gaussian data

# chargement des données
X, y = make_blobs(n_samples=1000, centers=3, n_features=5)

# Entrainenment de la SOM
net = sps.somNet(4, 6, X, PCI=1)
net.train()
P = [l.weights for l in net.nodeList]
D = euclidean_distances(X, P)

# DS2L-SOM
R = Rel_den_clust(D)
C = R.dataclust
Cr = R.dataclustref

# Affichage des résultats
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))
fig.suptitle('Gaussian data')

ax1.scatter(X[:, 0], X[:, 1], c=y)
ax1.set_title('Labels Réels')

ax2.scatter(X[:, 0], X[:, 1], c=C)
ax2.set_title('Clusters')

ax3.scatter(X[:, 0], X[:, 1], c=Cr)
ax3.set_title('Clusters corrigés')

print()
print()
print()

### Iris dataset

# chargement des données
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Entrainenment de la SOM
net = sps.somNet(4, 6, X)
net.train()
P = [l.weights for l in net.nodeList]
D = euclidean_distances(X, P)

# DS2L-SOM
R = Rel_den_clust(D)
C = R.dataclust
Cr = R.dataclustref

# Affichage des résultats
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))
fig.suptitle('Iris data')

ax1.scatter(X[:, 0], X[:, 1], c=y)
ax1.set_title('Labels Réels')

ax2.scatter(X[:, 0], X[:, 1], c=C)
ax2.set_title('Clusters')

ax3.scatter(X[:, 0], X[:, 1], c=Cr)
ax3.set_title('Clusters corrigés')
