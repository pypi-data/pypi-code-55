
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.datasets import make_blobs

### BC Clustering

from ml.baryclust.BC_Clust import BC_clustering_batch, BC_clustering_stoch
from sklearn.metrics.pairwise import euclidean_distances
from random import sample

## Gaussian data

# Chargement des données
data, y = make_blobs(n_samples=1000, centers=3, n_features=5)

M = euclidean_distances(data)  # avec data la matrice de données, ici c'est des vecteurs
X = range(len(M))
L = sample(X, 10)  # pour 10 points de supports
XS = M[:, L]

# Learning et Clustering
K = 3  # nombre de clusters à trouver
Rb = BC_clustering_batch(XS, L, K)
Rs = BC_clustering_stoch(XS, L, K)

# Affichage des résultats
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))
fig.suptitle('Gaussian data')

ax1.scatter(data[:, 0], data[:, 1], c=y)
ax1.set_title('Labels Réels')

ax2.scatter(data[:, 0], data[:, 1], c=Rb.Cl)
ax2.set_title('Clusters Batch')

ax3.scatter(data[:, 0], data[:, 1], c=Rs.Cl)
ax3.set_title('Clusters Stoch')

print()
print()
print()

### Iris dataset

# chargement des données
iris = datasets.load_iris()
data = iris.data
y = iris.target

M = euclidean_distances(data)  # avec data ta matrice de données, si c'est des vecteurs
X = range(len(M))
L = sample(X, 10)  # pour 10 points de supports
XS = M[:, L]

K = 3  # nombre de clusters à trouver
Rb = BC_clustering_batch(XS, L, K)
Rs = BC_clustering_stoch(XS, L, K)

# Affichage des résultats
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))
fig.suptitle('Iris data')

ax1.scatter(data[:, 0], data[:, 1], c=y)
ax1.set_title('Labels Réels')

ax2.scatter(data[:, 0], data[:, 1], c=Rb.Cl)
ax2.set_title('Clusters Batch')

ax3.scatter(data[:, 0], data[:, 1], c=Rs.Cl)
ax3.set_title('Clusters Stoch')
