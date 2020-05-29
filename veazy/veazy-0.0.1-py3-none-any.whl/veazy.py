import re
import networkx as nx
import pydotplus
import os
import itertools
from pathlib import Path

"""
VeazyHelper is built around two assumptions:
* A function name never contains '__' within the function name 
    (though at start/end is fine, like __init__)
* A function name never contains '___'
"""

class Veazy:
    def __init__(self, pyg):
        self.pyg = pyg
        self.node_list = []
        self.depth_of_nodes = []
        self.nodes_to_deep = []
        self.edges_to_deep = []
        self.max_depth = 0

        self._fill_node_list(self.pyg)
        self.node_list = self._filter_node_list(self.node_list)
        self._fill_depth_of_nodes()

    def _fill_node_list(self, graph):
        self.node_list = self.node_list + list(graph.obj_dict["nodes"].keys())
        for subgraph in graph.get_subgraph_list():
            self._fill_node_list(subgraph)

    def _filter_node_list(self, node_list):
        # TODO: static method, move to helper module?
        # TODO feels a bit over the top to put this in a function
        return set([node for node in node_list if node != "graph"])

    def _fill_depth_of_nodes(self):
        # utilize networkx to calculate depth
        nxg = nx.drawing.nx_pydot.from_pydot(self.pyg)

        # identify top node based on dot file
        def find_top_node(graph):
            for node in graph.get_node_list():
                try:
                    if node.obj_dict["attributes"]["group"] == '"0"':
                        return node
                except KeyError:
                    pass
            # repeat for every subgraph in graph (recursively)
            for subgraph in graph.get_subgraph_list():
                result = find_top_node(subgraph)
                if result:
                    return result.obj_dict["name"]

        top_node = find_top_node(self.pyg)
        # calculate depth of nodes, based on first node
        self.depth_of_nodes = dict(nx.single_source_shortest_path_length(nxg, top_node))
        # add depth 0 for all disconnected nodes
        missing_depths = {
            node: 0 for node in self.node_list if node not in self.depth_of_nodes.keys()
        }
        self.depth_of_nodes = {**self.depth_of_nodes, **missing_depths}

    def _split_func_str(self, func_str):
        # TODO: static method, move to helper module?
        """
        :param func_str: e.g. "bacon__eggs"
        :return: ("bacon", "eggs")
        """
        # derive the number of functions in the func_str
        n_func = len([sub_func for sub_func in func_str.split("__") if sub_func != ""])
        # construct regex pattern based on number of functions
        # this ensures that we have enough regex capture groups
        # (regex's own repeat pattern functionality didn't work well in this respect)
        regex_pattern_partial = "(__.*[^_]__|.*[^_])"
        regex_pattern = "__".join([regex_pattern_partial] * n_func)
        # make sure output is tuple
        split_func = re.findall(regex_pattern, func_str)[0]
        if type(split_func) == str:
            split_func = tuple([split_func])
        return split_func

    def _find_edges(self, nodes_to_search, originating_from_node):
        """
        :param nodes_to_search: list of node names (str)
        :param originating_from_node:
            if true, function will return edges originating from nodes
            if false, function will return edges pointing at nodes
        :return: list of edge tuples
        """
        edge_idx = 0 if originating_from_node else 1
        return [
            edge
            for edge in self.pyg.obj_dict["edges"].keys()
            if edge[edge_idx] in nodes_to_search
        ]

    def _delete_node_edge(self, nodes, edges):
        def del_node_recursive(graph, node):
            # TODO: static method, move to helper module?
            """
            :param graph: a graph in which to delete nodes and look for subgraphs
            :param node: node name (str)
            """
            graph.del_node(node)
            # repeat for every subgraph in self.pyg (recursively)
            for subgraph in graph.get_subgraph_list():
                del_node_recursive(subgraph, node)

        for node in nodes:
            del_node_recursive(self.pyg, node)
        for edge in edges:
            self.pyg.del_edge(edge)

    def _find_and_delete_deep(self):
        self.nodes_to_deep = [
            node
            for node, depth in self.depth_of_nodes.items()
            if depth > self.max_depth
        ]
        self.edges_to_deep = self._find_edges(
            self.nodes_to_deep, originating_from_node=False
        )
        self._delete_node_edge(self.nodes_to_deep, self.edges_to_deep)

    def _delete_scripts(self):
        # TODO: clean line below (some code duplication present)
        nodes_from_script = self._filter_node_list(
            list(self.pyg.get_subgraph_list()[0].obj_dict["nodes"].keys())
        )
        edges_from_script = self._find_edges(
            nodes_from_script, originating_from_node=True
        ) + self._find_edges(nodes_from_script, originating_from_node=False)
        self._delete_node_edge(nodes_from_script, edges_from_script)

    def _add_summarizing(self):
        def find_cluster(graph, cluster):
            """
            :param graph: a graph in which to search for cluster and look for subgraphs
            :param cluster: cluster name (str)
            """
            if cluster[:8] != "cluster_":
                cluster = "cluster_" + cluster
            if graph.obj_dict["name"] == cluster:
                return graph
            # repeat for every subgraph in graph (recursively)
            for subgraph in graph.get_subgraph_list():
                result = find_cluster(subgraph, cluster)
                if result:
                    return result

        # TODO: clean code
        # From the deleted nodes, find highest (idx 0) layer.
        # This layer will be re-added as summarizing node.
        summarizing_nodes = set(
            [self._split_func_str(node)[0] for node in self.nodes_to_deep]
        )
        for node in summarizing_nodes:
            add_to_graph = find_cluster(self.pyg, node)
            # TODO: can `if` below be incorporated into recursive function?
            if not add_to_graph:
                add_to_graph = self.pyg
            # TODO: add 'other' to node name
            add_to_graph.add_node(pydotplus.graphviz.Node(name=node))
        for edge in self.edges_to_deep:
            # TODO: does this work for adding edge
            # TODO: from summarizing node node 1 to summarizing node 2?
            if not (edge[0] in self.nodes_to_deep and edge[1] in self.nodes_to_deep):
                self.pyg.add_edge(
                    pydotplus.graphviz.Edge(
                        src=edge[0], dst=self._split_func_str(edge[1])[0]
                    )
                )
        # TODO: point at cluster
        # Does not seem possible. This would require clusters to be named.
        # We tried to achieve this, using function below,
        # but this messes up visual formatting.
        #     def _give_cluster_unique_names(graph):
        #         subgraph_list = graph.get_subgraph_list()
        #         for subgraph in subgraph_list:
        #             parent_name = subgraph.obj_dict["name"]
        #             for node in subgraph.get_node_list():
        #                 node_name = node.obj_dict["name"]
        #                 if node_name == "graph":
        #                     node.obj_dict["name"] = parent_name + "_graph"
        #             _give_cluster_unique_names(subgraph)
        # _give_cluster_unique_names(self.pyg)

        # TODO: improve visual formatting of summarizing nodes

    def get_pruned_graph(self, max_depth):
        self.max_depth = max_depth
        self._find_and_delete_deep()
        self._delete_scripts()
        self._add_summarizing()
        return self.pyg
