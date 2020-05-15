import sklearn.datasets
import sklearn.cluster
import matplotlib.pyplot as plot

def clustering(N,k):
	"""
	K-means clustering algorithm 
	(c) Marko Niemelä, May 15, 2020
	Inputs:
	- N: Number of data samples
	- k: Number of clusters
	Ouputs:
	- Plotted clustering result
	"""
	
	# Generate fake data
	X, L = sklearn.datasets.make_blobs(n_samples=N, n_features=2, centers=k)

	# Perform clustering
	kmeans = sklearn.cluster.KMeans(k, max_iter=100)
	kmeans.fit(X)
	means = kmeans.cluster_centers_

	# Show results
	plot.scatter(X[:, 0], X[:, 1], c=L)
	plot.scatter(means[:, 0], means[:, 1], linewidths=2)
	plot.show()


