import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from VizTools import helpers


def kmeans_fit(x, n_clusts, iters=300):
    km = KMeans(
        n_clusters=n_clusts, init='random',
        n_init=30, max_iter=iters,
        tol=1e-04
    )
    y_km = km.fit_predict(x)
    return y_km, km



def plot_kmeans(df, k, n_clusts, title,
                col_names=('Principal Component 1', 'Principal Component 2')):
    """

    Args:
        df:
        k:
        col_names:

    Returns:

    """
    # markers = ['o', 'v', 's', 'd', 'P', '+', '8', '*', "X", 'x', "D", 'd', 7, 6,
    #            "$:)$", "$:($", "$=$", "$?$",
    #            "$!$"]
    markers, colors = helpers.construct_point(n_clusts)
    # colors = [colors]
    for n in range(n_clusts):
        k_f = k == n, 0
        k_t = k == n, 1
        pc1 = df.loc[k_t[0], col_names[0]]
        pc2 = df.loc[k_t[0], col_names[1]]
        plt.scatter(
            pc1, pc2,
            # c=[colors[n]], marker=markers[n],
            edgecolor='black',
            label='Cluster {}'.format(n)
        )
        this_clust = df[k_t[0]]
        print(this_clust.iloc[:, :2],'\n')
        plt.legend()
        label_count = 0
        indices = pc1.index.to_list()
        for x, y in zip(pc1, pc2):
            plt.annotate(indices[label_count],  # this is the text
                         (x, y),  # this is the point to label
                         textcoords="offset points",  # how to position the text
                         xytext=(0, 10),  # distance from text to points (x,y)
                         ha='center',
                         size=6)  # horizontal alignment can be left, right or center
            label_count +=1
        plt.savefig('/Users/coltongarelli/Desktop/laura\'s LPP stuff/kmeans_{}_plot.pdf'.format(title))

def elbow_plot(km):
    '''plot to visualize distortion as clusters increase...aim for the elbow (where curve loses deceleration'''
    distortions = []
    for i in range(1, 11):
        distortions.append(km.inertia_)
    plt.plot(range(1, 11), distortions, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()