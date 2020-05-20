import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import manifold


def align_heatmap(weight_matrix, source, target, save_file, color="Blues"):
    """
    Show and save an align heatmap for two sentence.

    Parameters
    ----------
    weight_matrix : list
        the weight matrix for the heatmap
    source : String
        the horizontal axis, word number of source must equal to weight_matrix.shape[1]
    target : String
        the vertical axis, word number of target must equal to weight_matrix.shape[0]
    save_file : String
        the name of the file to be saved
    color : String
        the color of the heatmap, with "Blues" as default

    Returns
    -------
    heatmap : plt.Figure
    """
    s = source.split()
    t = target.split()
    weight_matrix = np.array(weight_matrix)
    assert weight_matrix.shape[0] == len(t)
    assert weight_matrix.shape[1] == len(s)
    weights = pd.DataFrame(weight_matrix, columns=s, index=t)
    # sns.heatmap(weights, cmap=sns.dark_palette('white')) # white and black map
    # sns.heatmap(weights,cmap=sns.color_palette('Blues'), linewidth=0.5) # blue map
    sns.heatmap(weights, cmap=sns.color_palette(color), linewidth=0.5)

    ax = plt.gca()
    ax.xaxis.set_ticks_position('bottom')
    plt.xticks(rotation=90)
    fig = plt.gcf()
    plt.savefig(save_file)
    plt.show()
    plt.close()
    return fig


def highlight_heatmap(weight_matrix, source, save_file):
    """
    show and save a highlighted heatmap for some sentences

    Parameters
    ----------
    weight_matrix : list
        the weight list for the heatmap
    source : list
        the sentences that will be highlighted
    save_file : String
        the name of the file to be saved

    Returns
    -------

    """

    part1 = """
        <html lang="en">
        <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8">
        <style>
        body {
        font-family: Sans-Serif;
        }
        </style>
        </head>
        <body>
        <h3>
        Heatmaps
        </h3>
        </body>
        <script>
        """
    part2 = """
        var color = "255,0,0";
        var ngram_length = 3;
        var half_ngram = 1;
        for (var k=0; k < any_text.length; k++) {
        var tokens = any_text[k].split(" ");
        var intensity = new Array(tokens.length);
        var max_intensity = Number.MIN_SAFE_INTEGER;
        var min_intensity = Number.MAX_SAFE_INTEGER;
        for (var i = 0; i < intensity.length; i++) {
        intensity[i] = 0.0;
        for (var j = -half_ngram; j < ngram_length-half_ngram; j++) {
        if (i+j < intensity.length && i+j > -1) {
        intensity[i] += trigram_weights[k][i + j];
        }
        }
        if (i == 0 || i == intensity.length-1) {
        intensity[i] /= 2.0;
        } else {
        intensity[i] /= 3.0;
        }
        if (intensity[i] > max_intensity) {
        max_intensity = intensity[i];
        }
        if (intensity[i] < min_intensity) {
        min_intensity = intensity[i];
        }
        }
        var denominator = max_intensity - min_intensity;
        for (var i = 0; i < intensity.length; i++) {
        intensity[i] = (intensity[i] - min_intensity) / denominator;
        }
        if (k%2 == 0) {
        var heat_text = "<p><br><b>Example:</b><br>";
        } else {
        var heat_text = "<b>Example:</b><br>";
        }
        var space = "";
        for (var i = 0; i < tokens.length; i++) {
        heat_text += "<span style='background-color:rgba(" + color + "," + intensity[i] + ")'>" + space + tokens[i] + "</span>";
        if (space == "") {
        space = " ";
        }
        }
        //heat_text += "<p>";
        document.body.innerHTML += heat_text;
        }
        </script>
        </html>"""
    putQuote = lambda x: "\"%s\"" % x
    textsString = "var any_text = [%s];\n" % (",".join(map(putQuote, source)))
    weightsString = "var trigram_weights = [%s];\n" % (",".join(map(str, weight_matrix)))
    with open(save_file, "w", encoding="utf-8") as f:
        f.write(part1)
        f.write(textsString)
        f.write(weightsString)
        f.write(part2)


def attention_heatmap(weight_list, source, save_file, color="Blues"):
    """
    show and save a attention weights heatmap for a sentences

    Parameters
    ----------
    weight_list : list
        the attention weights for the heatmap
    source : String
        the horizontal axis, word number of source must equal to len(weight_list)
    save_file : String
        the name of the file to be saved
    color : String
        the color of the heatmap, with "Blues" as default

    Returns
    -------
    heatmap : plt.Figure
    """
    s = source.split()
    word_num = len(s)
    assert len(weight_list) == len(s)
    weight_matrix = np.array([weight_list])

    plt.figure(figsize=(word_num, 2))

    weights = pd.DataFrame(weight_matrix, columns=s)
    # sns.heatmap(weights, cmap=sns.dark_palette('white')) # white and black map
    # sns.heatmap(weights,cmap=sns.color_palette('Blues'), linewidth=0.5) # blue map
    sns.heatmap(weights, cmap=sns.color_palette(color), linewidth=0.5)
    ax = plt.gca()
    ax.xaxis.set_ticks_position('bottom')
    # plt.xticks(labels=s)
    plt.xticks(rotation=90)
    plt.yticks([])
    fig = plt.gcf()
    plt.savefig(save_file)
    plt.show()
    plt.close()
    return fig


def double_attention_heatmap(first_weight_list, second_weight_matrix, sources, save_file, color="Blues"):
    """
    show and save a attention weights heatmap for a sentences

    Parameters
    ----------
    first_weight_list : list
        the attention weights in sentence level
    second_weight_matrix : list
        the element is a list that is the attention weights in word level
    sources : list
        the element is a String that is a sentence
    save_file : String
        the name of the file to be saved
    color : String
        the color of the heatmap, with "Blues" as default

    Returns
    -------
    heatmap : plt.Figure
    """
    sentence_num = len(first_weight_list)
    max_sentence_len = max([len(i) for i in second_weight_matrix])
    first_w = np.transpose(np.array([first_weight_list]))

    first_w = pd.DataFrame(first_w, index=list(range(1, sentence_num+1)))
    grid = plt.GridSpec(sentence_num, 1+max_sentence_len)
    plt.subplot(grid[:, 0])
    sns.heatmap(first_w, cmap=sns.color_palette(color), linewidth=0.5)
    # plt.figure(figsize=(2, sentence_num))
    plt.xticks([])
    # plt.legend('off')

    for i in range(sentence_num):
        s = sources[i].split()

        second_w = np.array([second_weight_matrix[i]])
        second_w = pd.DataFrame(second_w, columns=s)
        plt.subplot(grid[i, 1:])
        sns.heatmap(second_w, cmap=sns.color_palette(color), linewidth=0.5)
        ax = plt.gca()
        ax.xaxis.set_ticks_position('bottom')
        # plt.xticks(labels=s)
        plt.xticks(rotation=90)
        plt.yticks([])

    fig = plt.gcf()
    plt.savefig(save_file)
    plt.show()
    plt.close()
    return fig
