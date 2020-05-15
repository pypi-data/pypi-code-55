"""Tensorflow Runner ulils."""
from typing import List, Dict

import numpy as np
import tensorflow as tf

from .runner import Runner
from .graph_utils import load_graph


class TFRunner(Runner):
    """Runner for Tensorflow graph."""

    def __init__(self, graph_path: str, input_nodes: List[str], output_nodes: List[str]):
        """
        Initialize Tensorflow Runner with protobuf graph.

        Parameters
        ----------
        graph_path: path to protobuf file
        input_nodes: input nodes' names
        output_nodes: output nodes' names
        """
        super().__init__(graph_path, input_nodes, output_nodes)
        loaded_graph = load_graph(graph_path)
        self.sess = tf.compat.v1.Session(graph=loaded_graph)

    def __call__(self, tensor: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Run inference using TensorFlow.

        Parameters
        ----------
        tensor: input matrices

        Returns
        -------
        outputs_dict: output matrices
        """
        outputs_dict = {}
        inputs_dict = {}
        graph_output_tensors = []
        for index, node_name in enumerate(self.output_nodes):
            graph_output_tensors.append(self.sess.graph.get_tensor_by_name(node_name))
        for key, value in tensor.items():
            node_dict = {
                self.sess.graph.get_tensor_by_name(key): value
            }
            inputs_dict.update(node_dict)
        outputs = self.sess.run(
            graph_output_tensors,
            feed_dict=inputs_dict)
        for index, _ in enumerate(outputs):
            node_dict = {self.output_nodes[index]: outputs[index]}
            outputs_dict.update(node_dict)
        return outputs_dict
