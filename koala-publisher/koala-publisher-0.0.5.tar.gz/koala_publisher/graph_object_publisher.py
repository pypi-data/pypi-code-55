import sys
import requests
import logging
import os
import time

from collections.abc import Sequence
from koala_publisher.exceptions import exceptions


class GraphObjectPublisher:

    def __init__(self, url: str, chunk_size: int = 5000, max_num_retry: int=3, retry_delay_s: int=1):
        self._storage_url = url
        self._chunk_size = chunk_size
        self._max_num_retry = max_num_retry
        self._retry_delay_s = retry_delay_s
        self._logger = logging.getLogger(__name__)
        if not len(self._logger.handlers):
            self._add_log_handler()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def publish(self, nodes: Sequence, edges: Sequence):
        """ Publish the graph nodes

        :param nodes: Sequence of mapping objects representing the graph nodes to be published
        :param edges: Sequence of mapping objects representing the graph edges to be published
        :return: None
        """
        self._logger.info(f"Publishing {len(nodes)} graph nodes and {len(edges)} graph edges")
        self._publish_nodes(nodes)
        self._publish_edges(edges)

    def _publish_nodes(self, graph_nodes):
        chunks = self._divide_into_chunks(graph_nodes)
        for chunk_count, graph_node_chunk in enumerate(chunks, start=1):
            start = time.time()
            try:
                self._publish(url=f"{self._storage_url}/node", chunk=graph_node_chunk)
            except exceptions.PublishError as err:
                self._logger.error(f"Error publishing {len(graph_node_chunk)} graph nodes to {self._storage_url}")
                raise exceptions.PublishError(f"Error publishing {len(graph_node_chunk)} graph nodes "
                                              f"to {self._storage_url}: {err}")
            else:
                end = time.time()
                self._logger.info(f"Successfully published {len(graph_node_chunk)} graph nodes "
                                  f"in {end-start} seconds, chunk {chunk_count}/{len(chunks)}")

    def _publish_edges(self, graph_edges: Sequence):
        chunks = self._divide_into_chunks(graph_edges)
        for chunk_count, graph_edge_chunk in enumerate(chunks, start=1):
            start = time.time()
            try:
                self._publish(url=f"{self._storage_url}/edge", chunk=graph_edge_chunk)
            except exceptions.PublishError as err:
                self._logger.error(f"Error publishing {len(graph_edge_chunk)} graph edges to {self._storage_url}")
                raise exceptions.PublishError(f"Error publishing {len(graph_edge_chunk)} graph nodes "
                                              f"to {self._storage_url}: {err}")
            else:
                end = time.time()
                self._logger.info(f"Successfully published {len(graph_edge_chunk)} graph edges "
                                  f"in {end-start} seconds, chunk {chunk_count}/{len(chunks)}")

    def _publish(self, url: str, chunk: Sequence) -> None:
        for attempt in range(self._max_num_retry):
            try:
                res = requests.put(url, json=chunk,
                                   headers={"Authorization": f"bearer {os.environ['API_TOKEN']}"})
                res.raise_for_status()
            except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as err:
                time.sleep(self._retry_delay_s)
                continue
            else:
                return

        raise exceptions.PublishError(f"{self._max_num_retry} attempts to publish graph chunk failed: {err}")

    def _divide_into_chunks(self, graph_objects) -> Sequence:
        return [graph_objects[i:i + self._chunk_size] for i in range(0, len(graph_objects), self._chunk_size)]

    def _add_log_handler(self):
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(f"%(levelname)s:%(asctime)s: %(message)s",
                                      "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False
