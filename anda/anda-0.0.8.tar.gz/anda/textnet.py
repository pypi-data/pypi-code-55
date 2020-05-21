
### these should go easy
import sys
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('display.max_rows', 150)

import numpy as np
import os
import string
import collections
import math
import random
import statistics as stat
import re
import unicodedata
import json

# Natural Language Processing Toolkit - we use it especially for building bigrams
import nltk
from nltk.collocations import *

### Beautiful Soup and Urllib
### for scrapping of web data and parsing xml files
from urllib.request import urlopen
# urllib and requests do basically the same, but my preferences are changing all the time, so let's import both
from urllib.parse import quote  
import requests
from bs4 import BeautifulSoup
### in some cases I prefer Element Tree
import xml.etree.cElementTree as ET


### for visualization
# in some cases I use matplotlib, which is much easier to configure, elsewhere I prefer Plotly, which is more "sexy"
import matplotlib.pyplot as plt
from PIL import Image

import seaborn as sns

### to generate wordcloud data
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator, get_single_color_func

# There is a lot of changes in Plotly nowadays. Perhaps some modifications of the code will be needed at some point
import plotly
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
plotly.offline.init_notebook_mode(connected=True)

### for network analysis
import networkx as nx

def network_formation_df(dataset, column, book_abbr, lexicon_size, threshold):
    '''From a dataframe with rows corresponding to individual documents,
    to be subsellected on the basis of author's name column, for instance'''
    lemmata_list = dataset[book_abbr][column]
    lemmata_list = [lemma for lemma in lemmata_list if lemma != "být"]
    lemmata_list = [lemma for lemma in lemmata_list if lemma != "εἰμί"]
    lexicon = [word_tuple[0] for word_tuple in nltk.FreqDist(lemmata_list).most_common(lexicon_size)]
    bigrams_list = []
    for bigram in nltk.bigrams([lemma for lemma in lemmata_list if lemma != "být"]):
      if ((bigram[0] in lexicon) & (bigram[1] in lexicon)):
        if bigram[0] != bigram[1]:
          bigrams_list.append(tuple(sorted(bigram)))
    bigrams_counts = list((collections.Counter(bigrams_list)).items())
    bigrams_counts = sorted(bigrams_counts, key=lambda x: x[1], reverse=True)
    ### create a NetworkX object
    G = nx.Graph()
    G.clear()
    ### form the network from tuples of this form: (node1, node2, number of co-occurrences / lenght of the document)
    G.add_weighted_edges_from(np.array([(bigram_count[0][0], bigram_count[0][1],  int(bigram_count[1])) for bigram_count in bigrams_counts if bigram_count[1] >= threshold]))
    ### add edges attributes 
    for (u, v, wt) in G.edges.data('weight'):
        G[u][v]["weight"] = int(wt)
    total_weight = sum([int(n) for n in nx.get_edge_attributes(G, "weight").values()])
    for (u, v) in G.edges:
        G[u][v]["norm_weight"] = round((G[u][v]["weight"] / total_weight), 5)
        G[u][v]["distance"] = round(1 / (G[u][v]["weight"]), 5)
        G[u][v]["norm_distance"] = round(1 / (G[u][v]["norm_weight"] ), 5)
    return G

def network_from_lemmata_list(lemmata_list, lexicon_size, threshold):
    '''From a list of words'''
    lemmata_list = [lemma for lemma in lemmata_list if lemma != "být"]
    lemmata_list = [lemma for lemma in lemmata_list if lemma != "εἰμί"]
    lexicon = [word_tuple[0] for word_tuple in nltk.FreqDist(lemmata_list).most_common(lexicon_size)]
    bigrams_list = []
    for bigram in nltk.bigrams([lemma for lemma in lemmata_list if lemma != "být"]):
      if ((bigram[0] in lexicon) & (bigram[1] in lexicon)):
        if bigram[0] != bigram[1]:
          bigrams_list.append(tuple(sorted(bigram)))
    bigrams_counts = list((collections.Counter(bigrams_list)).items())
    bigrams_counts = sorted(bigrams_counts, key=lambda x: x[1], reverse=True)
    ### create a NetworkX object
    G = nx.Graph()
    G.clear()
    ### form the network from tuples of this form: (node1, node2, number of co-occurrences / lenght of the document)
    G.add_weighted_edges_from(np.array([(bigram_count[0][0], bigram_count[0][1],  int(bigram_count[1])) for bigram_count in bigrams_counts if bigram_count[1] >= threshold]))
    ### add edges attributes 
    for (u, v, wt) in G.edges.data('weight'):
        G[u][v]["weight"] = int(wt)
    total_weight = sum([int(n) for n in nx.get_edge_attributes(G, "weight").values()])
    for (u, v) in G.edges:
        G[u][v]["norm_weight"] = round((G[u][v]["weight"] / total_weight), 5)
        G[u][v]["distance"] = round(1 / (G[u][v]["weight"]), 5)
        G[u][v]["norm_distance"] = round(1 / (G[u][v]["norm_weight"] ), 5)
    return G
  
def network_by_author(dataset, column, book_abbr, lexicon_size, threshold):
    '''From a dataframe with rows corresponding to individual documents,
    to be subsellected on the basis of author's name column, for instance'''
    works = dataset[dataset["author"]==book_abbr][column].tolist()
    works_merged = [item for sublist in works for item in sublist]
    lexicon = [word_tuple[0] for word_tuple in nltk.FreqDist(works_merged).most_common(lexicon_size)]
    bigrams_list = []
    for work in works:
      for bigram in nltk.bigrams([lemma for lemma in work if lemma != "εἰμί"]):
        if ((bigram[0] in lexicon) & (bigram[1] in lexicon)):
          if bigram[0] != bigram[1]:
            bigrams_list.append(tuple(sorted(bigram)))
    bigrams_counts = list((collections.Counter(bigrams_list)).items())
    bigrams_counts = sorted(bigrams_counts, key=lambda x: x[1], reverse=True)
    ### create a NetworkX object
    G = nx.Graph()
    G.clear()
    ### form the network from tuples of this form: (node1, node2, number of co-occurrences / lenght of the document)
    G.add_weighted_edges_from(np.array([(bigram_count[0][0], bigram_count[0][1],  int(bigram_count[1])) for bigram_count in bigrams_counts if bigram_count[1] >= threshold]))
    ### add distance attribute
    for (u, v, wt) in G.edges.data('weight'):
        G[u][v]["weight"] = int(wt)
    total_weight = sum([int(n) for n in nx.get_edge_attributes(G, "weight").values()])
    for (u, v) in G.edges:
        G[u][v]["norm_weight"] = round((G[u][v]["weight"] / total_weight), 5)
        G[u][v]["distance"] = round(1 / (G[u][v]["weight"]), 5)
        G[u][v]["norm_distance"] = round(1 / (G[u][v]["norm_weight"] ), 5)
    return G

def draw_2d_network(networkx_object, file_name, mode):
    '''take networkX object and draw it'''
    pos_2d=nx.kamada_kawai_layout(networkx_object, weight="weight_norm")
    nx.set_node_attributes(networkx_object, pos_2d, "pos_2d")
    dmin=1
    ncenter=0
    Edges = list(networkx_object.edges)
    L=len(Edges)
    labels= list(networkx_object.nodes)
    N = len(labels)
    distance_list = [float(distance[2]) for distance in list(networkx_object.edges.data("distance"))]
    weight_list = [int(float(weight[2])) for weight in list(networkx_object.edges.data("weight"))]
    for n in pos_2d:
        x,y=pos_2d[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d
    p =nx.single_source_shortest_path_length(networkx_object, ncenter)
    adjc= [len(one_adjc) for one_adjc in list((nx.generate_adjlist(networkx_object)))]
    middle_node_trace = go.Scatter(
        x=[],
        y=[],
        opacity=0,
        text=weight_list,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            opacity=0
            )
        )
    for Edge in Edges:
        x0,y0 = networkx_object.nodes[Edge[0]]["pos_2d"]
        x1,y1 = networkx_object.nodes[Edge[1]]["pos_2d"]
        middle_node_trace['x'] += tuple([(x0+x1)/2])
        middle_node_trace['y'] += tuple([(y0+y1)/2])
    edge_trace1 = go.Scatter(
        x=[], y=[],
        #hoverinfo='none',
        mode='lines',
        line=dict(width=1,color="#000000"),
        )
    edge_trace2 = go.Scatter(
        x=[],y=[],
        #hoverinfo='none',
        mode='lines',
        line=dict(width=0.7,color="#404040"),
        )
    edge_trace3 = go.Scatter(
        x=[], y=[],
        #hoverinfo='none',
        mode='lines',
        line=dict(width=0.5,color="#C0C0C0"),
        )
    best_5percent_norm_weight = sorted(list(networkx_object.edges.data("norm_weight")), key=lambda x: x[2], reverse=True)[int((len(networkx_object.edges.data("norm_weight")) / 100) * 5)][2]
    best_20percent_norm_weight = sorted(list(networkx_object.edges.data("norm_weight")), key=lambda x: x[2], reverse=True)[int((len(networkx_object.edges.data("norm_weight")) / 100) * 20)][2]
    for edge in networkx_object.edges.data():
        if edge[2]["norm_weight"] >= best_5percent_norm_weight:
            x0, y0 = networkx_object.nodes[edge[0]]['pos_2d']
            x1, y1 = networkx_object.nodes[edge[1]]['pos_2d']
            edge_trace1['x'] += tuple([x0, x1, None])
            edge_trace1['y'] += tuple([y0, y1, None])
        else:
            if edge[2]["norm_weight"] >= best_20percent_norm_weight:
                x0, y0 = networkx_object.nodes[edge[0]]['pos_2d']
                x1, y1 = networkx_object.nodes[edge[1]]['pos_2d']
                edge_trace2['x'] += tuple([x0, x1, None])
                edge_trace2['y'] += tuple([y0, y1, None])
            else:
                x0, y0 = networkx_object.nodes[edge[0]]['pos_2d']
                x1, y1 = networkx_object.nodes[edge[1]]['pos_2d']
                edge_trace3['x'] += tuple([x0, x1, None])
                edge_trace3['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[],
        y=[],
        #name=[],
        text=[],
        textposition='bottom center',
        mode='markers+text',
        hovertext=adjc,
        hoverinfo='text',
        marker=dict(
            ###showscale=True,
            showscale=False, ### change to see scale
            colorscale='Greys',
            reversescale=True,
            color=[],
            size=7,
            colorbar=dict(
                thickness=15,
                title='degree',
                xanchor='left',
                titleside='right'
                ),
            line=dict(width=1)
            )
        )

    for node in networkx_object.nodes():
        x, y = networkx_object.nodes[node]['pos_2d']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace["text"] += tuple([node])
        ### original version: node_trace["text"] += tuple([node])

    ### Color Node Points
    for node, adjacencies in enumerate(nx.generate_adjlist(networkx_object)):
        node_trace['marker']['color'] += tuple([len(adjacencies)])
        ###node_info = ' of connections: '+str(len(adjacencies))
        ###node_trace['something'].append(node_info)

    fig = go.Figure(data=[edge_trace1, edge_trace2, edge_trace3, node_trace, middle_node_trace],
        layout=go.Layout(
            plot_bgcolor='rgba(0,0,0,0)',
            autosize=False,
            width=500,
            height=500,
            #title=file_name,
            titlefont=dict(size=16),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=10,l=10,r=10, t=10),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            ))
    if mode=="offline":
        return iplot(fig, filename=gdrive_root +  "figures/nt_cep_networks" + file_name +".html")
    if mode=="online":
        return iplot(fig, filename=file_name)
    if mode=="file":
         return plot(fig, filename=gdrive_root +  "figures/nt_cep_networks/" + file_name + ".png" , auto_open=False)

def draw_3d_network(networkx_object, file_name, mode):
    '''take networkX object and draw it in 3D'''
    Edges = list(networkx_object.edges)
    L=len(Edges)
    distance_list = [distance[2] for distance in list(networkx_object.edges.data("distance"))]
    weight_list = [int(float(weight[2])) for weight in list(networkx_object.edges.data("weight"))]
    labels= list(networkx_object.nodes)
    N = len(labels)
    adjc= [len(one_adjc) for one_adjc in list((nx.generate_adjlist(networkx_object)))] ### instead of "group"
    pos_3d=nx.spring_layout(networkx_object, weight="weight", dim=3)
    nx.set_node_attributes(networkx_object, pos_3d, "pos_3d")
    layt = [list(array) for array in pos_3d.values()]
    N= len(networkx_object.nodes)
    Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
    Yn=[layt[k][1] for k in range(N)]# y-coordinates
    Zn=[layt[k][2] for k in range(N)]# z-coordinates
    Xe=[]
    Ye=[]
    Ze=[]
    for Edge in Edges:
        Xe+=[networkx_object.nodes[Edge[0]]["pos_3d"][0],networkx_object.nodes[Edge[1]]["pos_3d"][0], None]# x-coordinates of edge ends
        Ye+=[networkx_object.nodes[Edge[0]]["pos_3d"][1],networkx_object.nodes[Edge[1]]["pos_3d"][1], None]
        Ze+=[networkx_object.nodes[Edge[0]]["pos_3d"][2],networkx_object.nodes[Edge[1]]["pos_3d"][2], None]

        ### to get the hover into the middle of the line
        ### we have to produce a node in the middle of the line
        ### based on https://stackoverflow.com/questions/46037897/line-hover-text-in-plotly

    middle_node_trace = go.Scatter3d(
            x=[],
            y=[],
            z=[],
            opacity=0,
            text=weight_list,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                opacity=0
            )
        )

    for Edge in Edges:

        x0,y0,z0 = networkx_object.nodes[Edge[0]]["pos_3d"]
        x1,y1,z1 = networkx_object.nodes[Edge[1]]["pos_3d"]
        ###trace3['x'] += [x0, x1, None]
        ###trace3['y'] += [y0, y1, None]
        ###trace3['z'] += [z0, z1, None]
        ###trace3_list.append(trace3)
        middle_node_trace['x'] += tuple([(x0+x1)/2])
        middle_node_trace['y'] += tuple([(y0+y1)/2])#.append((y0+y1)/2)
        middle_node_trace['z'] += tuple([(z0+z1)/2])#.append((z0+z1)/2)
        

    ### edge trace
    trace1=go.Scatter3d(x=Xe,
                       y=Ye,
                       z=Ze,
                       mode='lines',
                       line=dict(color='rgb(125,125,125)', width=1),
                       text=distance_list,
                       hoverinfo='text',
                       textposition="top right"
                       )
    ### node trace
    trace2=go.Scatter3d(x=Xn,
                       y=Yn,
                       z=Zn,
                       mode='markers+text',
                       ###name=labels,
                       marker=dict(symbol='circle',
                                     size=6,
                                     color=adjc,
                                     colorscale='Earth',
                                     reversescale=True,
                                     line=dict(color='rgb(50,50,50)', width=0.5)
                                     ),
                       text=[],
                       #textposition='bottom center',
                       #hovertext=adjc,
                       #hoverinfo='text'
                       )
    for node in networkx_object.nodes():
        trace2["text"] += tuple([node])
    
    axis=dict(showbackground=False,
                  showline=False,
                  zeroline=False,
                  showgrid=False,
                  showticklabels=False,
                  title=''
                  )
    layout = go.Layout(
                plot_bgcolor='rgba(0,0,0,0)',
                 title="",
                 width=900,
                 height=700,
                 showlegend=False,
                 scene=dict(
                     xaxis=dict(axis),
                     yaxis=dict(axis),
                     zaxis=dict(axis),
                ),
             margin=dict(
                t=100
            ),
            hovermode='closest',
            annotations=[
                   dict(
                   showarrow=False,
                    text="",
                    xref='paper',
                    yref='paper',
                    x=0,
                    y=0.1,
                    xanchor='left',
                    yanchor='bottom',
                    font=dict(
                    size=14
                    )
                    )
                ],    )
    data=[trace1, trace2, middle_node_trace]
    fig=go.Figure(data=data, layout=layout)
    if mode=="offline":
        return iplot(fig) ###, filename=file_name+".html")
    if mode=="online":
        return iplot(fig, filename=file_name)
    if mode=="eps":
        return pio.write_image(fig, "images/" + file_name + "_3D.eps" , scale=1)

def ego_network_drawing_reduced(network, term, num_of_neighbours, title, mode, dimensions):
    '''derrive ego network from a preexisting network
    specify source term and number of neighbors
    includes only shortest paths from the source'''
    length, path = nx.single_source_dijkstra(network, term, target=None, weight="distance")
    shortest_nodes = list(length.keys())[0:num_of_neighbours+1]
    path_values_sorted = [dict_pair[1] for dict_pair in sorted(path.items(), key=lambda pair: list(length.keys()).index(pair[0]))]
    path_edges = []
    for path_to_term in path_values_sorted[1:num_of_neighbours+1]:
        path_edges.extend([tuple(sorted(bigram)) for bigram in nltk.bigrams(path_to_term)])
    shortest_edges = list(set(path_edges))
    ego_network = network.copy(as_view=False)
    nodes_to_remove = []
    for node in ego_network.nodes:
        if node not in shortest_nodes:
            nodes_to_remove.append(node)
    for element in nodes_to_remove:
        ego_network.remove_node(element) 
    edges_to_remove = []
    for edge in ego_network.edges:
        if edge not in shortest_edges:
            if (edge[1],edge[0]) not in shortest_edges:
                edges_to_remove.append(edge)
    for element in edges_to_remove:
        ego_network.remove_edge(element[0], element[1])
    if dimensions == "2D":
      return draw_2d_network(ego_network, title, mode)   
    if dimensions == "3D":
      return draw_3d_network(ego_network, title, mode)  

      
def ego_network_standard(dataset, column, book_abbr, term, mode, dimensions):
    if isinstance(dataset, pd.DataFrame) == True:
      network = network_by_author(dataset, column, book_abbr, 500, 1)
    else: 
      network = network_formation_df(dataset, column, book_abbr, 500, 1)
    ego_network_drawing_reduced(network, term, 30, book_abbr + " - " + term, mode, dimensions)


def ego_network_closest(dataset, column, book_abbr, term, num_of_neighbours):
  if isinstance(dataset, pd.DataFrame) == True:
      network = network_by_author(dataset, column, book_abbr, 500, 1)
  else: 
      network = network_formation_df(dataset, book_abbr, 500, 1)
  length, path = nx.single_source_dijkstra(network, term, target=None, weight="distance")
  length_sorted = sorted(length.items(), key=lambda x:x[1])[1:num_of_neighbours+1]
  length_sorted_trans = [(translator_short(tup[0]), round(tup[1], 3)) for tup in length_sorted]
  return length_sorted_trans

def ego_network_list_from_list(lemmata_list, term, num_of_neighbours):
  network = network_from_lemmata_list(lemmata_list, 500, 1)
  try: 
    length, path = nx.single_source_dijkstra(network, term, target=None, weight="distance")
    length_sorted = sorted(length.items(), key=lambda x:x[1])[1:num_of_neighbours+1]
    length_sorted_trans = [(tup[0], list_of_meanings(tup[0]), round(tup[1], 3)) for tup in length_sorted]
    return length_sorted_trans
  except:
    return []

  
def ego_network_data(dataset, column, book_abbr, term, num_of_neighbours):
    '''create network and ego network on its basis
    specify source term and number of neighbors
    includes only shortest paths from the source'''
    if isinstance(dataset, pd.DataFrame) == True:
      network = network_by_author(dataset, column, book_abbr, 500, 1)
    else: 
      network = network_formation_df(dataset, column, book_abbr, 500, 1)
    length, path = nx.single_source_dijkstra(network, term, target=None, weight="distance")
    shortest_nodes = list(length.keys())[0:num_of_neighbours+1]
    path_values_sorted = [dict_pair[1] for dict_pair in sorted(path.items(), key=lambda pair: list(length.keys()).index(pair[0]))]
    path_edges = []
    for path_to_term in path_values_sorted[1:num_of_neighbours+1]:
        path_edges.extend([tuple(sorted(bigram)) for bigram in nltk.bigrams(path_to_term)])
    shortest_edges = list(set(path_edges))
    ego_network = network.copy(as_view=False)
    nodes_to_remove = []
    for node in ego_network.nodes:
        if node not in shortest_nodes:
            nodes_to_remove.append(node)
    for element in nodes_to_remove:
        ego_network.remove_node(element)    
    edges_to_remove = []
    for edge in ego_network.edges:
        if edge not in shortest_edges:
            if (edge[1],edge[0]) not in shortest_edges:
                edges_to_remove.append(edge)
    for element in edges_to_remove:
        ego_network.remove_edge(element[0], element[1])
    ego_network_data_prec = sorted(list(ego_network.edges.data("weight")), key=lambda tup: int(tup[2]), reverse=True)
    ego_network_data_complete = []
    for tup in ego_network_data_prec:
      if tup[1] == term:
        ego_network_data_complete.append([tup[1], tup[0], int(tup[2]), round(1 / int(tup[2]), 5)])
      else:
        ego_network_data_complete.append([tup[0], tup[1], int(tup[2]), round(1 / int(tup[2]), 5)])
    return ego_network_data_complete
  

    
# to work with plotly in google colab environment
def configure_plotly_browser_state():
  import IPython
  display(IPython.core.display.HTML('''
        <script src="/static/components/requirejs/require.js"></script>
        <script>
          requirejs.config({
            paths: {
              base: '/static/base',
              plotly: 'https://cdn.plot.ly/plotly-latest.min.js?noext',
            },
          });
        </script>
        '''))
