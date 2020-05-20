import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs

from ml.baryclust.StreamBarycentric import BaryStream, invproj

### Stream Barycentric

nbdata = 500
Nclust = 5

data, Y = make_blobs(nbdata * 2, 10, Nclust)
vectime = np.random.randint(0, 5000, nbdata * 2)

urls = np.random.random(nbdata * 2)
sup = data[:10]

vectimeind = np.argsort(vectime)
data = data[vectimeind]
vectime = vectime[vectimeind]

test = BaryStream(support=sup, radius=4, max_timestamp=2000, histo=50)
test.train(data, vectime, urls)

nodedatdenaissance = np.array([[n.data.number, n.data.dateNaissance] for n in test.graph.nodes])

plt.figure()
xlab = "neuron numbers"
ylab = "birth moments (s)"
title = "illustration of neuron birth"
plt.xlabel(xlab)
plt.ylabel(ylab)
plt.title(title)
plt.plot(nodedatdenaissance[:, 1], nodedatdenaissance[:, 0])
plt.grid()
plt.show()

test.Macroclustering(Nclust)
plt.figure()
plt.scatter(data[:, 0], data[:, 1], c='k', s=1)
nodes = test.get_nodes_position()
nodeseuclid = invproj(nodes, sup)
plt.scatter(nodeseuclid[:, 0], nodeseuclid[:, 1], c=test.macro_clusters)









