import sys
from copy import deepcopy
from itertools import repeat
from operator import add, sub
from logging import getLogger, ERROR
from collections import OrderedDict, deque
from multiprocessing import Process, Array, Lock, Manager, Pool

from numpy import array
from numpy.random import RandomState

# Local module imports

from cspy.checking import check
from cspy.algorithms.label import Label
from cspy.preprocessing import preprocess_graph

log = getLogger(__name__)


class BiDirectionalSearch:
    """
    """

    def __init__(self, G, max_res, min_res, direction, REF_forward,
                 REF_backward):
        # Preprocess graph
        self.G = G
        self.direction = direction
        self.max_res, self.min_res = max_res.copy(), min_res.copy()
        self.max_res_in, self.min_res_in = array(max_res.copy()), array(
            min_res.copy())

        # Algorithm specific parameters #
        # set bounds for bacward search
        # Current forward and backward labels
        if self.direction == "forward":
            self.current_label = Label(0, "Source", min_res, ["Source"])
        else:
            bwd_start = deepcopy(min_res)
            bwd_start[0] = max_res[0]
            self.current_label = Label(0, "Sink", bwd_start, ["Sink"])
        # Unprocessed labels dict (both directions)
        self.unprocessed_labels = deque()
        # To save all best labels
        self.best_labels = deque()
        # Final labels dicts for unidirectional search
        self.final_label = None

        # If given, set REFs for dominance relations and feasibility checks
        if REF_forward:
            Label._REF_forward = REF_forward
        else:
            Label._REF_forward = add
        if REF_backward:
            Label._REF_backward = REF_backward
        else:
            Label._REF_backward = sub

    def run(self, res_bound, results):
        while self.current_label:
            print(self.current_label)
            self.move(res_bound)
        results[self.direction] = self.best_labels

    def move(self, res_bound):
        lock.acquire()
        try:
            if self.direction == "forward":
                self.max_res = res_bound
            else:
                self.min_res = res_bound
        finally:
            lock.release()
        self._algorithm()

    def get_current_label(self):
        return self.current_label

    def get_res(self):
        if self.direction == "forward":
            return self.min_res
        else:
            return self.max_res

    def get_best_labels(self):
        return self.best_labels

    #############
    # ALGORITHM #
    #############
    def _algorithm(self):
        print(self.direction)
        if self.direction == "forward":  # forward
            idx = 0  # index for head node
            # Update backwards half-way point
            self.min_res[0] = max(
                self.min_res[0], min(self.current_label.res[0],
                                     self.max_res[0]))
            print("HB = ", self.min_res[0])
        else:  # backward
            idx = 1  # index for tail node
            # Update forwards half-way point
            self.max_res[0] = min(
                self.max_res[0], max(self.current_label.res[0],
                                     self.min_res[0]))
            print("HF = ", self.min_res[0])
        # Select edges with the same head/tail node as the current label node.
        edges = deque(e for e in self.G.edges(data=True)
                      if e[idx] == self.current_label.node)
        # If Label not been seen before, initialise a list
        # Propagate current label along all suitable edges in current direction
        deque(map(self._propagate_label, edges))
        # Extend label
        next_label = self._get_next_label()
        # Update current label
        self.current_label = next_label
        # Dominance checks
        self._check_dominance(next_label)

    def _propagate_label(self, edge):
        # Label propagation #
        new_label = self.current_label.get_new_label(edge, self.direction)
        # If the new label is resource feasible
        if new_label and new_label.feasibility_check(self.max_res,
                                                     self.min_res):
            # And is not already in the unprocessed labels list
            if new_label not in self.unprocessed_labels:
                self.unprocessed_labels.append(new_label)

    def _get_next_label(self):
        # Label Extension #
        # Add current label to processed list.
        current_label = self.current_label
        unproc_labels = self.unprocessed_labels

        self._remove_labels([current_label], unproc=True)
        # Return label with minimum monotone resource for the forward search
        # and the maximum monotone resource for the backward search
        if unproc_labels:
            if self.direction == "forward":
                return min(unproc_labels, key=lambda x: x.res[0])
            else:
                return max(unproc_labels, key=lambda x: x.res[0])
        else:
            return None

    #############
    # DOMINANCE #
    #############
    def _check_dominance(self, label_to_check, unproc=True, best=False):
        """
        For all labels, checks if ``label_to_check`` is dominated,
        or itself dominates any other label in either the unprocessed_labels
        list or the non-dominated labels list.
        If this is found to be the case, the dominated label(s) is(are)
        removed from the appropriate list.
        """
        # Select appropriate list to check
        if unproc:
            labels_to_check = self.unprocessed_labels
        elif best:
            labels_to_check = self.best_labels
        # If label is not None (at termination)
        if label_to_check:
            labels_to_pop = deque()
            # Gather all comparable labels (same node)
            all_labels = deque(
                l for l in labels_to_check
                if l.node == label_to_check.node and l != label_to_check)
            # Add to list for removal if they are dominated
            labels_to_pop.extend(l for l in all_labels
                                 if label_to_check.dominates(l, self.direction))
            # Add input label for removal if itself is dominated
            if any(
                    l.dominates(label_to_check, self.direction)
                    for l in all_labels):
                labels_to_pop.append(label_to_check)
            elif unproc:
                # check and save current label
                self._save_current_best_label()
            # if unprocessed labels checked then remove labels_to_pop
            if unproc:
                self._remove_labels(labels_to_pop, unproc, best)
            # Otherwise, return labels_to_pop for later removal
            elif best:
                return labels_to_pop

    def _remove_labels(self, labels_to_pop, unproc=True, best=False):
        """
        Remove all labels in ``labels_to_pop`` from either the array of
        unprocessed labels or the array of non-dominated labels
        """
        # Remove all processed labels from unprocessed dict
        for label_to_pop in deque(set(labels_to_pop)):
            if unproc and label_to_pop in self.unprocessed_labels:
                idx = self.unprocessed_labels.index(label_to_pop)
                del self.unprocessed_labels[idx]
            elif best and label_to_pop in self.best_labels:
                idx = self.best_labels.index(label_to_pop)
                del self.best_labels[idx]

    def _save_current_best_label(self):
        """
        Label saving
        """
        current_label = self.current_label

        self.best_labels.append(current_label)


class BiDirectionalParallel:

    def __init__(self,
                 G,
                 max_res,
                 min_res,
                 preprocess=False,
                 REF_forward=None,
                 REF_backward=None,
                 REF_join=None):
        # Check inputs
        check(G,
              max_res,
              min_res,
              REF_forward=REF_forward,
              REF_backward=REF_backward,
              REF_join=REF_join,
              algorithm=__name__)
        # Preprocess graph
        self.G = preprocess_graph(G, max_res, min_res, preprocess, REF_forward)
        self.REF_join = REF_join

        self.lock = Lock()
        mgr = Manager()
        self.max_res = mgr.list(max_res.copy())
        self.min_res = mgr.list(min_res.copy())
        self.results = mgr.dict()
        self.max_res_in, self.min_res_in = array(max_res.copy()), array(
            min_res.copy())
        # Initialise forward search
        self.fwd_search = BiDirectionalSearch(G, max_res, min_res, "forward",
                                              REF_forward, REF_backward)
        # initialise backward search
        self.bwd_search = BiDirectionalSearch(G, max_res, min_res, "backward",
                                              REF_forward, REF_backward)
        # Current forward and backward labels
        self.current_label = OrderedDict({
            "forward": self.fwd_search.get_current_label(),
            "backward": self.bwd_search.get_current_label()
        })
        # To save all best labels
        self.best_labels = OrderedDict({
            "forward": deque(),
            "backward": deque()
        })
        self.best_label = None

    @property
    def path(self):
        """
        Get list with nodes in calculated path.
        """
        if not self.best_label:
            raise Exception("Please call the .run() method first")
        return self.best_label.path

    @property
    def total_cost(self):
        """
        Get accumulated cost along the path.
        """
        if not self.best_label:
            raise Exception("Please call the .run() method first")
        return self.best_label.weight

    @property
    def consumed_resources(self):
        """
        Get accumulated resources consumed along the path.
        """
        if not self.best_label:
            raise Exception("Please call the .run() method first")
        return self.best_label.res

    def _init_pool(self, l):
        global lock
        lock = l

    def run(self):
        """
        Calculate shortest path with resource constraints.
        """
        self._init_pool(self.lock)
        p1 = Process(target=self.fwd_search.run,
                     args=(self.max_res, self.results))
        p2 = Process(target=self.bwd_search.run,
                     args=(self.min_res, self.results))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        self.best_labels = self.results

        self._clean_up()
        return self._process_paths()

    def _update_current_labels(self):
        self.current_label["forward"] = self.fwd_search.get_current_label()
        self.current_label["backward"] = self.bwd_search.get_current_label()

    def _update_res(self):
        self.min_res = self.fwd_search.get_res()
        self.max_res = self.bwd_search.get_res()

    def _move(self):
        if self.current_label["forward"]:
            self.fwd_search.move(self.max_res)
        if self.current_label["backward"]:
            self.bwd_search.move(self.min_res)

    def _update_best_labels(self):
        self.best_labels["forward"] = self.fwd_search.get_best_labels()
        self.best_labels["backward"] = self.bwd_search.get_best_labels()

    def _clean_up(self):
        pass

    ###################
    # PATH PROCESSING #
    ###################
    def _process_paths(self):
        # Processing of output path.
        self._join_paths()
        # if (self.best_labels["forward"] and self.best_labels["backward"]):
        #     # If bi-directional algorithm used, run path joining procedure.
        #     # self._clean_up_best_labels()
        #     self._join_paths()
        # else:
        #     # If mono-directional algorithm used or both directions not traversed,
        #     # return the appropriate path
        #     if not self.best_labels["backward"]:
        #         # Forward
        #         self.best_label = self.final_label
        #     else:
        #         # Backward
        #         self.best_label = self._process_bwd_label(
        #             self.final_label, self.min_res_in)

    def _process_bwd_label(self, label, cumulative_res):
        # Reverse backward path and inverts resource consumption
        label.path.reverse()
        label.res[0] = self.max_res_in[0] - label.res[0]
        label.res = label.res + cumulative_res
        return label

    def _clean_up_best_labels(self):
        # Removed all dominated labels in best_labels
        for direc in ["forward", "backward"]:
            labels_to_pop = deque()
            for l in self.best_labels[direc]:
                labels_to_pop.extend(
                    self._check_dominance(l, direc, unproc=False, best=True))
            self._remove_labels(labels_to_pop, direc, unproc=False, best=True)

    def _join_paths(self):
        """
        The procedure "Join" or Algorithm 3 from `Righini and Salani (2006)`_.

        Modified to get rid of nested for loops and reduced search.

        :return: list with the final path.

        .. _Righini and Salani (2006): https://www.sciencedirect.com/science/article/pii/S1572528606000417
        """
        log.debug("joining")
        for fwd_label in self.best_labels["forward"]:
            # Create generator for backward labels for current forward label.
            # Includes only those that:
            # 1. Paths can be joined (exists a connecting edge)
            # 2. Introduces no cycles
            # 3. When combined with the forward label, they satisfy the halfway check
            bwd_labels = (l for l in self.best_labels["backward"] if (
                (fwd_label.node, l.node) in self.G.edges() and \
                not any(n in fwd_label.path for n in l.path) and
                self._half_way(fwd_label, l)))
            for bwd_label in bwd_labels:
                # Merge two labels
                merged_label = self._merge_labels(fwd_label, bwd_label)
                # Check resource feasibility
                if (merged_label and merged_label.feasibility_check(
                        self.max_res_in, self.min_res_in)):
                    # Save label
                    self._save(merged_label)

    def _half_way(self, fwd_label, bwd_label):
        """
        Half-way check from `Righini and Salani (2006)`_.
        Checks if a pair of labels is closes to the half-way point.

        :return: bool. True if the half-way check passes, false otherwise.

        .. _Righini and Salani (2006): https://www.sciencedirect.com/science/article/pii/S1572528606000417
        """
        phi = abs(fwd_label.res[0] - (self.max_res_in[0] - bwd_label.res[0]))
        if 0 <= phi <= 2:
            return True
        else:
            return False

    def _merge_labels(self, fwd_label, bwd_label):
        """
        Merge labels produced by a backward and forward label.

        Paramaters
        ----------
        fwd_label : label.Label object
        bwd_label : label.Label object

        Returns
        -------
        merged_label : label.Label object
            If an s-t compatible path can be obtained the appropriately
            extended and merged label is returned

        None
            Otherwise.
        """
        # Make a copy of the backward label
        _bwd_label = deepcopy(bwd_label)
        # Reconstruct edge with edge data
        edge = (fwd_label.node, _bwd_label.node,
                self.G[fwd_label.node][_bwd_label.node])
        # Custom resource merging function
        if self.REF_join:
            final_res = self.REF_join(fwd_label.res, _bwd_label.res, edge)
            self._process_bwd_label(_bwd_label, self.min_res_in)
        # Default resource merging
        else:
            # Extend forward label along joining edge
            label = fwd_label.get_new_label(edge, "forward")
            if not label:
                return
            # Process backward label
            self._process_bwd_label(_bwd_label, label.res)
            final_res = _bwd_label.res
        # Record total weight, total_res and final path
        weight = fwd_label.weight + edge[2]['weight'] + _bwd_label.weight
        final_path = fwd_label.path + _bwd_label.path
        merged_label = Label(weight, "Sink", final_res, final_path)
        return merged_label

    @staticmethod
    def _full_dominance_check(label1, label2, direc):
        """
        Checks whether label 1 dominates label 2 for the input direction.
        In the case when neither dominates , i.e. they are non-dominated,
        the direction is flipped labels are compared again.
        """
        label1_dominates = label1.dominates(label2, direc)
        label2_dominates = label2.dominates(label1, direc)
        # label1 dominates label2 for the input direction
        if label1_dominates:
            return True
        # Both non-dominated labels in this direction.
        elif (not label1_dominates and not label2_dominates):
            # flip directions
            flip_direc = "forward" if direc == "backward" else "backward"
            label1_dominates_flipped = label1.dominates(label2, flip_direc)
            # label 1 dominates label2 in the flipped direction
            if label1_dominates_flipped:
                return True
            elif label1.weight < label2.weight:
                return True

    def _save(self, label):
        # Saves a label for exposure
        if not self.best_label or self._full_dominance_check(
                label, self.best_label, "forward"):
            log.debug("Saving label {} as best".format(label))
            log.debug("With path {}".format(label.path))
            self.best_label = label
