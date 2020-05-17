import json
from os import path
import networkx as nx

"""
self.ent2id = {ent: idx for idx, ent in enumerate(ent_set)}
self.rel2id = {rel: idx for idx, rel in enumerate(rel_set)}
self.rel2id.update(
        {rel + '_reverse': idx + len(self.rel2id) for idx, rel in enumerate(rel_set)})

self.id2ent = {idx: ent for ent, idx in self.ent2id.items()}
self.id2rel = {idx: rel for rel, idx in self.rel2id.items()}

"""


class Knowledge:
    def __init__(self, src: str,
                 for_load: bool = False,
                 separator='\t',
                 pattern: str = None,
                 name: str = None,
                 multi_graph: bool = True):
        """

        :param src: source file
        :param separator: h sep r sep t
        :param pattern: "h r t" or "h t r"
        :param multi_graph:
        """
        assert path.exists(src), f"KG Source File{src} not exists!"
        self._src = src
        with open(src, 'r') as s:
            self.lines = s.readlines()
        self._separator = separator
        self._pattern = pattern  # '{h r t} or {h t r}'
        self.name = name
        self.multi_graph = multi_graph
        self.ent2idx = dict()
        self.rel2idx = dict()
        self.idx2ent = dict()
        self.idx2rel = dict()
        self.entities = set()
        self.relations = set()
        self.rel_triplets = dict()  # k is rel and value is list
        self._graph = dict()  # Knowledge dict
        self.triplets = list()
        self.rev_suffix = "_reverse"

        self.nx_edge_keyword = set()
        self.built = False
        self.indexed = False

    def build_graph_from_raw(self):
        """
        Build whole graph
        """
        for line in self.lines:
            line = line.strip()  # remove \n
            head, rel, tail = line.split(sep=self._separator)
            self.triplets.append((head, rel, tail))
            self.entities.add(head)
            self.entities.add(tail)
            self.relations.add(rel)
            if head not in self._graph.keys():
                self._graph[head] = list()
            self._graph[head].append((rel, tail))
        self.built = True

    def build_graph_from_json(self):
        """
        Given: Triplets

        """
        for triplet in self.triplets:
            assert len(triplet) == 3, f"Triplet error with {triplet}"
            head, rel, tail = triplet
            if head not in self._graph.keys():
                self._graph[head] = list()
            self._graph[head].append((rel, tail))
            if rel not in self.rel_triplets.keys():
                self.rel_triplets[rel] = list()
            self.rel_triplets[rel].append((head, tail))
        self.built = True
        self.indexed = True

    def indexing(self, ent_specials: set = None, rel_specials: set = None):
        """
        :param ent_specials: Special entities to be indexing
        :param rel_specials: Special relations
        """
        if ent_specials is not None and rel_specials is not None:
            self.entities = self.entities.union(ent_specials)
            self.relations = self.relations.union(rel_specials)
        self.ent2idx = {ent: idx for idx, ent in enumerate(self.entities)}
        self.rel2idx = {rel: idx for idx, rel in enumerate(self.relations)}
        self.rel2idx.update(
                {rel + self.rev_suffix: idx + len(self.rel2idx) for idx, rel in enumerate(
                        self.relations)})
        self.idx2ent = {idx: ent for ent, idx in self.ent2idx.items()}
        self.idx2rel = {idx: rel for rel, idx in self.rel2idx.items()}
        self.indexed = True

    def raw_graph_nx(self):
        """
        TODO: Learn Networkx and finish

        :return: Networkx type graph
        """
        # G.add_edge(2, 3, weight=0.9) add weight keyword for edge attr
        # G.add_edge('y', 'x', function=math.cos)
        if self.multi_graph:
            graph_nx = nx.MultiDiGraph()
        else:
            graph_nx = nx.DiGraph()
        if not self.built:
            self.build_graph_from_raw()
        for ent in self._graph.keys():
            # key is entity
            for pair in self._graph[ent]:
                # [rel, tail]
                rel, tail = pair
                graph_nx.add_edge(ent, tail, rel_type=rel)
                self.nx_edge_keyword.add("rel_type")
                # deal with reverse
                graph_nx.add_edge(tail, ent, rel_type=rel + self.rev_suffix)
        return graph_nx

    def indexed_graph_nx(self):
        """
        Indexed graph
        Key is ent/rel index instead of raw text

        :return: Networkx type graph
        """
        if self.multi_graph:
            indexed_graph_nx = nx.MultiDiGraph()
        else:
            indexed_graph_nx = nx.DiGraph()
        if not self.built:
            self.build_graph_from_raw()
        assert self.indexed, "You should call self.indexing(self, ent_specials: set, " \
                             "rel_specials: set) before fetching indexed nx graph"
        for ent in self._graph.keys():
            ent_idx = self.ent2idx[ent]
            for pair in self._graph[ent]:
                rel, tail = pair
                rel_idx = self.rel2idx[rel]
                rel_rv_idx = self.rel2idx[rel + self.rev_suffix]
                tail_idx = self.ent2idx[tail]
                indexed_graph_nx.add_edge(ent_idx, tail_idx, rel_type=rel_idx)
                # todo: add reverse relations
                indexed_graph_nx.add_edge(tail_idx, ent_idx, rel_type=rel_rv_idx)
        return indexed_graph_nx

    def sub_graph(self, center_node, hop: int):
        """
        TODO: sub_graph method
        1. given: center node and hop count
        2. fetch all related node from graph
        :param center_node:
        :param hop:
        :return: node list
        """
        raise NotImplementedError

    def save(self, dest: str):
        """
        Save processed data to json file
        Includes:
            + Triplets
            + Rel2id
            + Ent2id

        """
        assert path.isdir(dest), f"{dest} should be a directory."
        assert self.indexed and self.built, "Can only save index and build obj."
        obj_path = path.join(dest, f"{self.name}-obj.json")
        result = dict()
        result['entities'] = self.ent2idx
        result['relations'] = self.rel2idx
        result['triplets'] = self.triplets
        result['rel-triplets'] = self.rel_triplets
        json.dump(result, open(obj_path, 'w'), ensure_ascii=False, indent='\t')
        print(f"JSON file saved in {obj_path}")
        print("JSON keys: entities, relations, triplets, rel-triplets")

    def load(self, filename: str):
        assert path.isfile(filename), f"{filename} is not a file"
        result = json.load(open(filename, 'r'))
        self.triplets = result['triplets']
        self.ent2idx = result['entities']
        self.rel2idx = result['relations']
        self.rel_triplets = result['rel-triplets']
        self.build_graph_from_json()

    def rel_bundle(self, indexing: bool = False) -> dict:
        """

        Returns: dict type
            key: rel
            val: list of (head, tail)

        """
        if not self.built:
            self.build_graph_from_raw()
        result = dict()
        for t in self.triplets:
            head, rel, tail = t
            if rel not in result.keys():
                result[rel] = list()
            result[rel].append((head, tail))
        return result

    @property
    def index_graph(self) -> dict:
        """
        Returns: indexed dict type graph
        """
        if not self.indexed:
            self.indexing()
        result = dict()
        for head, pair in self._graph.items():
            hidx = self.ent2idx[head]
            rel, tail = pair
            if hidx not in result.keys():
                result[hidx] = list()
            ridx, tidx = self.rel2idx[rel], self.ent2idx[tail]
            result[hidx].append((ridx, tidx))
        return result

    def __len__(self):
        return len(self.triplets)

    def save_dgl_ke(self, file_path: str):
        """

        Args:
            file_path: path to save dgl process file

        head\t rel \t tail

        Returns:

        """
