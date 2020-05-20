# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 15:52:52 2017

"""
import warnings

warnings.filterwarnings("ignore")

import mdp
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
from numpy.linalg import pinv
from mdp import graph
import matplotlib.pyplot as plt
from copy import deepcopy
from scipy.cluster.hierarchy import fcluster
from matplotlib.ticker import MaxNLocator
from scipy.cluster.hierarchy import linkage


def invproj(B, sup):
    r = []
    for i in B:
        t = sup[0] * 0
        c = 0
        for j in sup:
            t += j * i[c]
            c += 1
        r.append(t)
    return np.array(r)


'''ts = time stamp for each data, max_timestamp = la fenetre temperele (le temps qui'il met à oublier les information 
'''
"""n0 = neuron plus proche """


class BaryStream(mdp.nodes.GrowingNeuralGasNode):

    def __init__(self, eps_b=0.2, max_timestamp=50, histo=3600, support=[], simmeasure=euclidean_distances, radius=1):
        """

        :param eps_b:
        :param max_timestamp:
        :param histo:
        :param support:
        :param simmeasure:
        :param radius:
        """
        self.graph = graph.Graph()
        self.support = support
        self.simmeasure = simmeasure
        self.eps_b = eps_b

        super(mdp.nodes.GrowingNeuralGasNode, self).__init__(None, None, None)
        self.max_timestamp = max_timestamp
        self.radius = radius

        self.S = self.simmeasure(self.support, self.support) ** 2
        self.A = self.MatA()
        self.graph.compteur = 0  # nmbr de neuron ajouté
        self.graph.compteursupprime = 0  # nmbr de neuron supprimé
        self.graph.compteurtotal = 0  # nmbr de neuron total crée
        self.graph.hist_compteur = 0
        self.histo = histo
        self.evolutiondugraph = []
        self.creation = 0
        self.lastTimestamp = 0

    def _insert_new_node(self, pos, ts, url):
        """Insert a new node in the graph when no cluster(node) can absorb the new data"""
        new_node = self._add_node(pos)  # on crée un nuveau node à tel position
        new_node.data.age = 0  # age defini pour chaque data
        new_node.data.nbr_absorb = 1  # nbr absorbé par chaque neuron
        new_node.data.labels = [(deepcopy(pos), ts, url)]  #
        new_node.data.number = self.graph.compteur  #
        self.graph.compteur += 1  # depui depart combien de neuron on ajoute à graph
        self.graph.compteurtotal += 1
        self.evolutiondugraph.append([ts, self.graph.compteur, self.graph.compteursupprime, self.graph.compteurtotal])
        new_node.data.schema = []
        new_node.data.dateNaissance = ts  # create une liste de date de naissance pour chaque neuron
        new_node.data.dateDead = 'toujours actif'  #

    def nearest_url(self, n):
        vecDeLabels = [i[0] for i in n.data.labels]  # vectors des 5 plus proches
        distnodeurl = euclidean_distances(vecDeLabels,
                                          [n.data.pos])  # calculer la distance entre la neuron et les 5 plus proches
        LaPlusProcheUrlindex = np.argmin(distnodeurl)
        LaPlusProcheUrl = n.data.labels[LaPlusProcheUrlindex][2]
        return (LaPlusProcheUrl)

    def savefig(self, name):
        """

        :param name:
        :return:
        """
        timefinal = (self.lastTimestamp - self.creation) / 86400
        for h in self.graph.nodes:
            schema0 = np.array(h.data.schema)
            t = (schema0[:, 1] - self.creation) / 86400
            ax = plt.figure().gca()
            nearurl = self.nearest_url(h)
            xlab = "Time(days)"
            ylab = "data number"
            title = "change detection pour le neuron " + str(h.data.number) + ": " + nearurl
            plt.xlabel(xlab)
            plt.ylabel(ylab)
            plt.title(title)
            plt.xlim(0, timefinal)
            plt.plot(t, schema0[:, 0])
            plt.grid()
            # plt.show()
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            plt.savefig(name + "_change_cluster_detection_" + str(h.data.number) + ".png", format='png')
            plt.clf()  # Clear the figure for the next loop

    def changedetectionfig(self, name):
        M = np.array(self.evolutiondugraph)
        plt.figure()
        xlab = "Time(days)"
        ylab = "Added neuron numbers"
        title = "Added neurons during time"
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        t = (M[:, 0] - self.creation) / 86400
        plt.plot(t, M[:, 1])
        plt.grid()
        plt.show()
        plt.savefig(name + "_Added_neurons_during_time.png", format='png')
        # plt.clf()  # Clear the figure for the next loop

        plt.figure()
        xlab = "Time(days)"
        ylab = "Removed neuron numbers"
        title = "Removed neurons during time"
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        plt.plot(t, M[:, 2])
        plt.grid()
        plt.show()
        plt.savefig(name + "_removed_neurons_during_time.png", format='png')
        # plt.clf()  # Clear the figure for the next loop

        plt.figure()
        xlab = "Time(days)"
        ylab = "Total neuron numbers"
        title = "Total neurons during time"
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        plt.plot(t, M[:, 3])
        plt.grid()
        plt.show()
        plt.savefig(name + "_Total_neurons_during_time.png", format='png')
        # plt.clf()  # Clear the figure for the next loop

    def _train(self, data, timestamp, urls):
        g = self.graph
        # d = self.d
        dataproj = self.projectionData(data)  # projection de data dans l'espace Barycentric
        # self.bary_dim = dataproj.shape[1] #dimension dans l'espace barycentric (nmbre de representatnt)

        # loop on single data points        
        for x, ts, url in zip(dataproj, timestamp, urls):
            self.lastTimestamp = ts
            if len(g.nodes) == 0:  # si il y a pas de neuron, on crée une neuron (inserter un neuron)
                self._insert_new_node(x, ts, url)
                self.creation = ts
                self.times_old = ts  # time_old c'est time de donnée avant, si c'est le new neuron, on initialize à ts
            else:
                # step 1 - find the nearest nodes
                # dists are the squared distances of x from n0, n1
                n0, dist = self._get_nearest_nodes(
                    x)  # il re envoie deux valeurs, neuron plus proche et la distance entre new data et nearest neuron
                alpha = 1 - (ts - self.times_old) / self.max_timestamp  # alpha est l'importance qu'on donne aux neurons
                # step 2 - add a new node if distance est > radius
                if np.sqrt(dist) > self.radius:
                    self._insert_new_node(x, ts, url)

                # step 3 - mettre à jours des prototypes
                else:  # n0 abosorb une donnée
                    n0.data.nbr_absorb = alpha * n0.data.nbr_absorb  # mettre à jour de 1ere neuron, multiplie par alpha et plus 1
                    n0.data.nbr_absorb += 1

                    self._move_node(n0, x, self.eps_b)  # mettre à jours la position
                    self.top_urls(n0, x, ts, url, dist)  # rouver les top 5 urls plus proche de chaque neuron
                    n0.data.age = 0  # à chaque fois qu'il absorb une data l'age devient à zero

                # step 4 - removing a neuron and update all others neurons

                for j in g.nodes:  # pour toute les neurons
                    if j != n0:  # si la neuron n'est pas la neuron plus proche:
                        if j.data.age > self.max_timestamp:  # si la neuron est plus agé que une semaine:
                            g.remove_node(j)  # on enleve la neuron
                            self.graph.compteursupprime += 1  # nmbr de neuron supprimé
                            self.graph.compteurtotal -= 1  # nmbr neuron total creé
                            self.evolutiondugraph.append(
                                [ts, self.graph.compteur, self.graph.compteursupprime, self.graph.compteurtotal])
                        j.data.nbr_absorb = alpha * j.data.nbr_absorb  # on multiplie toute les neurons par alpha
                        j.data.age = j.data.age + (
                                    ts - self.times_old)  # on eugmenet l'age de neuron depuis la dernier fois que la gragh a recu une donnée

                self.graph.hist_compteur += ts - self.times_old  # on augement compteur à la difference
                if self.graph.hist_compteur >= self.histo:
                    for j in g.nodes:
                        j.data.schema.append([j.data.nbr_absorb, ts])

                    self.graph.hist_compteur = 0

                self.times_old = ts  # à la fin, time stamp de new data devient old time stamp pour la prochaine data

    # pour ajouter les tp 5 plus proche urls à chaque neuron
    # si dans la liste on a moin que 5 urls, on ajoute cette urls dans la liste
    # sinon la new urls prend la place de url plus loin de de neurn
    def top_urls(self, n0, x, ts, url, dist):
        url_n0 = np.array([k[2] for k in n0.data.labels])
        if url not in url_n0:
            if len(n0.data.labels) < 5:
                n0.data.labels.append((x, ts, url))
            else:
                m = np.array([k[0] for k in n0.data.labels])
                distances = self.distBary([n0.data.pos], m)[0]
                max_ind = np.argmax(distances)
                if distances[max_ind] > dist:
                    n0.data.labels[max_ind] = (x, ts, url)

    def _get_nearest_nodes(self, x):
        """Return the two nodes in the graph that are nearest to x and their
        squared distances. (Return ([node1, node2], [dist1, dist2])"""
        # distance function
        g = self.graph
        # distances of all nodes from x
        nodepos = [n.data.pos for n in g.nodes]  # position pour chaque neuron
        distances = self.distBary([x], nodepos)[0]
        ids = distances.argsort()[:1]
        # nearest = [g.nodes[idx] for idx in ids]
        # return nearest, distances[ids]
        return g.nodes[ids[0]], distances[ids]

    def Macroclustering(self, k):
        """

        :param k:
        :return:
        """
        nodespos = self.get_nodes_position()
        distmatrice = np.sqrt(self.distBary(nodespos, nodespos))
        Zed = linkage(distmatrice, 'ward')

        self.macro_clusters = fcluster(Zed, k, criterion='maxclust')

        nodes = np.array(self.graph.nodes)  # on cree une array à partir des nodes
        results = []
        for i in set(self.macro_clusters):
            nodesclusters = nodes[self.macro_clusters == i]  # il sort des nodes des clusters
            # print("nodesclusters: ",nodesclusters)

            posclusters = np.array([n.data.pos for n in nodesclusters])
            mean_pos_clusters = np.mean(posclusters, axis=0)
            # print("mean_pos_clusters : ",mean_pos_clusters)#le barycentre de macro cluster

            nmbrabsorbedclusters = [n.data.nbr_absorb for n in nodesclusters]
            sum_nmbr_absorbed_clusters = np.sum(nmbrabsorbedclusters)
            # print("sum_nmbr_absorbed_clusters : ",sum_nmbr_absorbed_clusters)

            dateNaissanceclusters = [n.data.dateNaissance for n in nodesclusters]
            mean_dateNaissance_clusters = np.mean(dateNaissanceclusters)
            # print("mean_dateNaissance_clusters : ",mean_dateNaissance_clusters)

            result = [i] + [sum_nmbr_absorbed_clusters] + [mean_dateNaissance_clusters] + list(mean_pos_clusters)
            # print("result : ",result)
            results.append(result)

        self.macro_cluster_data = np.array(results)

    # calcul de la matrice de A
    def MatA(self):
        d = self.S
        l = len(self.support)
        Aplus = np.concatenate((np.tile(d[0], (l - 1, 1)), np.ones((1, l))), axis=0)
        Amoins = np.concatenate((d[1:], np.zeros((1, l))), axis=0)
        return Aplus - Amoins

    # calcul de la matric J
    def MatJ(self, data):
        d = self.simmeasure(self.support, data) ** 2
        ls = len(self.support)
        ld = len(data)
        Jplus = np.concatenate((np.tile(d[0], (ls - 1, 1)), np.ones((1, ld))), axis=0)
        Jmoins = np.concatenate((d[1:], np.zeros((1, ld))), axis=0)
        return Jplus - Jmoins

    # projection des data
    def projectionData(self, data):
        A = self.A
        J = self.MatJ(data)
        return np.dot(pinv(A), J).T

    # fonction qui calcule la matrice de similarite entre deux listes
    def distBary(self, Beta1, Beta2):  # en entree il faut liste des coordinate de Beta
        distancebarMatrice = np.zeros((len(Beta1), len(Beta2)))
        for i in range(len(Beta1)):
            for j in range(len(Beta2)):
                distancebarycentric = np.dot(np.dot(-1 / 2 * (Beta1[i] - Beta2[j]).T, self.S), (Beta1[i] - Beta2[j]))
                distancebarMatrice[i, j] = distancebarycentric
        return distancebarMatrice  # this is the distance**2
