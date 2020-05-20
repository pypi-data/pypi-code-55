
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import manifold

__all__ = [
    "boxplot",
    "kdeplot",
    "vector_cluster_scatter",
    "percent_stack_bar",
    "gantt_bar"
]

def boxplot(value_matrix, labels, save_file):
    """
    show and save a boxplot to compare a measurement among models

    Parameters
    ----------
    value_matrix : list
        the element is a list that is the measurement values of a model
    labels : list
        the element is a String that is the name of model
    save_file : String
        the name of the file to be saved

    Returns
    -------
    boxplot : plt.Figure
    """
    values = np.transpose(np.array(value_matrix))
    values = pd.DataFrame(values, columns=labels)
    values.boxplot()
    fig = plt.gcf()
    plt.savefig(save_file)
    plt.show()
    plt.close()
    return fig


def kdeplot(value_matrix, labels, save_file):
    """
    show and save a boxplot to compare a measurement among models

    Parameters
    ----------
    value_matrix : list
        the element is a list that is the measurement values of a model
    labels : list
        the element is a String that is the name of model
    save_file : String
        the name of the file to be saved

    Returns
    -------
    kdeplot : plt.Figure
    """
    for i in range(len(value_matrix)):
        value = np.array(value_matrix[i])
        sns.kdeplot(value, bw=.2, label=labels[i])
    fig = plt.gcf()
    plt.savefig(save_file)
    plt.show()
    plt.close()
    return fig


def vector_cluster_scatter(vector_list, label_list, save_file):
    """
    show and save a scatter that shows the cluster of vectors

    Parameters
    ----------
    vector_list : list
        the element is a list that is a vector
    label_list : list
        the element is a String that is a label of a vector
    save_file : String
        the name of the file to be saved

    Returns
    -------
    scatter : plt.Figure
    """
    vector_list = np.array(vector_list)
    # standardization
    mu = np.mean(vector_list, axis=0)
    sigma = np.std(vector_list, axis=0)
    vector_list = (vector_list - mu) / sigma

    # tsne
    tsne = manifold.TSNE(n_components=2, init='pca', perplexity=5, random_state=0)
    tsne_vectors = tsne.fit_transform(vector_list)

    # DBSCAN
    # todo 调整参数
    # dbscan_vectors = DBSCAN(eps=5, min_samples=10).fit(tsne_vectors)
    # dbscan_labels = dbscan_vectors.labels_
    # print(dbscan_labels)
    # print(sum([1 for i in dbscan_labels if i == -1]))

    data_dict = dict()
    for i in range(len(label_list)):
        # if dbscan_labels[i] == -1:
        #     continue
        vector = tsne_vectors[i]
        label = label_list[i]
        if label in data_dict:
            data_dict[label].append(vector)
        else:
            data_dict[label] = [vector]
    for label, vectors in data_dict.items():
        vectors = np.array(vectors)
        plt.scatter(vectors[:, 0], vectors[:, 1], label=label)
    fig = plt.gcf()
    plt.savefig(save_file)
    plt.show()
    plt.close()
    return fig


def percent_stack_bar(vector_list, label_list, models_name, save_file):
    """
    show and save percent stack bar to compare some measurements among models

    Parameters
    ----------
    vector_list : list
        the element is a list that is scores of some measurement of a model
    label_list : list
        the element is a String that is the name of a measurement, len(label_list) == vector_list.shape[1]
    models_name : list
        the element is a String that is the name of a model, len(label_list) == vector_list.shape[0]
    save_file : String
        the name of the file to be saved

    Returns
    -------
    bar : plt.Figure
    """
    vectors = np.array(vector_list)
    m, n = vectors.shape
    percent = vectors / np.reshape(np.sum(vectors, axis=-1), [m, 1])
    accumulate = np.zeros(m)
    for i in range(n):
        plt.barh(y=models_name, width=percent[:, i], left=accumulate, label=label_list[i])
        accumulate += percent[:, i]
    ax = plt.gca()
    ax.set_xlim(0, 1)

    fig = plt.gcf()
    plt.savefig(save_file)
    plt.show()
    plt.close()
    return fig


def gantt_bar(vector_list, label_list, models_name, save_file):
    """
    show and save percent stack bar to compare some measurements among models

    Parameters
    ----------
    vector_list : list
        the element is a list that is scores of some measurement of a model
    label_list : list
        the element is a String that is the name of a measurement, len(label_list) == vector_list.shape[1]
    models_name : list
        the element is a String that is the name of a model, len(label_list) == vector_list.shape[0]
    save_file : String
        the name of the file to be saved

    Returns
    -------
    bar : plt.Figure

    """
    vectors = np.array(vector_list)
    m, n = vectors.shape
    percent = vectors / np.reshape(np.sum(vectors, axis=-1), [m, 1])
    middle_measurement_index = int(n / 2)
    middle_measurement_value = np.zeros(m)
    for i in range(middle_measurement_index):
        middle_measurement_value += percent[:, i]
    middle_measurement_value += percent[:, middle_measurement_index] / 2

    max_middle_value = max(middle_measurement_value)
    accumulate = max_middle_value - middle_measurement_value
    for i in range(n):
        plt.barh(y=models_name, width=percent[:, i], left=accumulate, label=label_list[i])
        accumulate += percent[:, i]
    fig = plt.gcf()
    plt.savefig(save_file)
    plt.show()
    plt.close()
    return fig


def knowledge_graph():
    # https: // zhuanlan.zhihu.com / p / 36700425
    pass


def self_attention_heatmap():
    pass


def dynamic_hidden_state():
    pass