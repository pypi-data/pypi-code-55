from graphviz import Digraph, Graph

from kubernetes_explorer.label_matching import LabelMatching


class KubernetesGraph():
    def __init__(self, group_by_namespace=False, more=False, attributes={}, engine='dot'):
        self.lm = LabelMatching()
        self.attributes = attributes
        self.group_by_namespace = group_by_namespace
        self.more = more
        self.namespace_graphs = {}

        graph_attr = {**{'label': "Kubernetes graph", 'labelloc': 't', 'labeljust': 'l', 'compound': 'true'},
                      **self._get_attr('graph', 'graph')}
        edge_attr = {**{'minlen': '2'}, **self._get_attr('graph', 'edge')}
        node_attr = {**{}, **self._get_attr('graph', 'node')}

        self.dot = Digraph(comment='Kubernetes graph', format='png', engine=engine,
                           graph_attr=graph_attr,
                           edge_attr=edge_attr,
                           node_attr=node_attr)

    def _get_graph(self, namespace):
        if self.group_by_namespace:
            return self.namespace_graphs[namespace]
        else:
            return self.dot

    def _get_attr(self, object_: str, kind: str) -> dict:
        if object_ in self.attributes:
            if kind in self.attributes[object_]:
                attr = self.attributes[object_][kind]
            else:
                attr = self.attributes[object_]
            attr = {k: str(v) for k, v in attr.items()}
            return attr
        else:
            return {}

    def _print_labels(self, labels: dict, newline: str = "\l", start_newline=True) -> str:
        if labels is None or len(labels) == 0:
            return f"{newline}labels: none"

        labels_str = f"{newline}labels:{newline}"
        for key, value in labels.items():
            labels_str += f"        {key}: {value}{newline}"

        return labels_str

    def add_pods(self, pods):
        for pod in pods:
            # Merge default attributes with custom attributes
            attributes = {**{'shape': 'plaintext'}, **self._get_attr('pod', 'node')}

            graph = self._get_graph(pod.metadata.namespace)

            containers = ""
            for container in pod.spec.containers:
                image = f"<br/>image: {container.image}" if self.more else ""
                containers += f"<TR><TD>Container: {container.name + image}</TD></TR>"

            labels = self._print_labels(pod.metadata.labels, '<br ALIGN="LEFT"/>') if self.more else ""

            graph.node(pod.metadata.uid,
                       f"<<TABLE CELLBORDER=\"1\"><TR><TD BORDER=\"0\">Pod: {pod.metadata.name}{labels}</TD></TR>{containers}</TABLE>>", **attributes)

            # Add pod to label selector
            self.lm.add(pod.metadata.uid, pod.metadata.labels)

    def add_services(self, services):
        for service in services:
            graph = self._get_graph(service.metadata.namespace)
            labels = self._print_labels(service.metadata.labels) if self.more else ""
            graph.node(service.metadata.uid, f"Service: {service.metadata.name}{labels}",
                       **self._get_attr('service', 'node'))

            # Add link to all selected pods
            for pod in self.lm.get(service.spec.selector):
                graph.edge(service.metadata.uid, pod, **self._get_attr('service', 'edge'))

    def add_deployments(self, deployments):
        for deployment in deployments:
            graph = self._get_graph(deployment.metadata.namespace)
            labels = self._print_labels(deployment.metadata.labels) if self.more else ""
            graph.node(deployment.metadata.uid, f"Deployment: {deployment.metadata.name}{labels}",
                       **self._get_attr('deployment', 'node'))

            # Add link to all selected pods
            for pod in self.lm.get(deployment.spec.selector):
                graph.edge(deployment.metadata.uid, pod, **self._get_attr('deployment', 'edge'))

    def add_secrets(self, secrets):
        for secret in secrets:
            graph = self._get_graph(secret.metadata.namespace)
            labels = self._print_labels(secret.metadata.labels) if self.more else ""
            graph.node(secret.metadata.uid, f"Secret: {secret.metadata.name}{labels}",
                       **self._get_attr('secret', 'node'))

    def add_namespaces(self, namespaces):
        for namespace in namespaces:
            if self.group_by_namespace:
                # Merge default attributes with custom attributes
                attributes = {**{'color': 'black', 'label': f"namespace: {namespace.metadata.name}",
                                 'labelloc': 't', 'compound': 'true'},
                              **self._get_attr('namespace', 'graph')}
                namespace_graph = Digraph(
                    name=f"cluster_namespace_{namespace.metadata.name}", graph_attr=attributes)
                self.namespace_graphs[namespace.metadata.name] = namespace_graph
            else:
                self.dot.node(namespace.metadata.uid, f"namespace: {namespace.metadata.name}",
                              **self._get_attr('namespace', 'node'))

    def get_graph(self):
        graph = self.dot.copy()

        for key, value in self.namespace_graphs.items():
            graph.subgraph(value)

        return graph

    def get_source(self):
        return self.get_graph().source


default_attributes = {}
