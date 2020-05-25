# ===== Imports ===============================================================

import argparse
import logging

from kubernetes_explorer.kubernetes_explorer import KubernetesExplorer, KubernetesObject
from kubernetes_explorer.kubernetes_graph import KubernetesGraph
from kubernetes_explorer.utils import str2bool, read_yaml


def main():

    # ===== Arguments =============================================================

    description = "Kubernetes Explorer: Explore your Kubernetes cluster and all its objects."

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-c", "--context", default=None, type=str,
                        help="The kubectl context to use. Default to the active context.")
    parser.add_argument("-g", "--group-by-namespace", default=True, type=str2bool,
                        help="Whether to group together objects with the same namespace in the graph.")
    parser.add_argument("-i", "--ignore", default=[], type=str, nargs='+',
                        choices=[obj.value for obj in KubernetesObject],
                        help="List of objects to ignore.")
    parser.add_argument("-m", "--more", action="store_true",
                        help="Show more information about the objects.")
    parser.add_argument("-n", "--namespace", default=None, type=str,
                        help="If present, the namespace scope for this CLI request.")
    parser.add_argument("-o", "--output", default='graph.dot', type=str,
                        help="Filename of the output graph file.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose mode.")
    parser.add_argument("--attributes-file", default="ke-attributes.yaml", type=str,
                        help="Config file with attributes to add to the graph. Default to \"ke-attributes.yaml\"")

    args = parser.parse_args()

    attributes_file = args.attributes_file
    context = args.context
    ignore = args.ignore
    group_by_namespace = args.group_by_namespace if KubernetesObject.NAMESPACE.value not in ignore else False
    more = args.more
    namespace = args.namespace
    output = args.output
    verbose = args.verbose

    # ===== Initialization ========================================================

    logger = logging.getLogger('kubernetes-explorer')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level=logging.INFO if verbose else logging.WARNING)

    ke = KubernetesExplorer(context=context)

    attributes = read_yaml(attributes_file)

    # ===== Retrieve objects ======================================================

    logger.info("Retrieving objects...")

    if KubernetesObject.DEPLOYMENT.value not in ignore:
        deployments = ke.get_deployments(namespace)
        logger.info(f"----- Found {len(deployments)} deployments")

    if KubernetesObject.NAMESPACE.value not in ignore:
        namespaces = ke.get_namespaces(namespace)
        logger.info(f"----- Found {len(namespaces)} namespaces")

    if KubernetesObject.POD.value not in ignore:
        pods = ke.get_pods(namespace)
        logger.info(f"----- Found {len(pods)} pods")

    if KubernetesObject.SECRET.value not in ignore:
        secrets = ke.get_secrets(namespace)
        logger.info(f"----- Found {len(secrets)} secrets")

    if KubernetesObject.SERVICE.value not in ignore:
        services = ke.get_services(namespace)
        logger.info(f"----- Found {len(services)} services")

    # ===== Build graph ===========================================================

    logger.info("Building graph...")

    kg = KubernetesGraph(group_by_namespace=group_by_namespace, more=more,
                         attributes=attributes)

    if KubernetesObject.NAMESPACE.value not in ignore:
        kg.add_namespaces(namespaces)
    if KubernetesObject.POD.value not in ignore:
        kg.add_pods(pods)
    if KubernetesObject.SERVICE.value not in ignore:
        kg.add_services(services)
    if KubernetesObject.SECRET.value not in ignore:
        kg.add_secrets(secrets)
    if KubernetesObject.DEPLOYMENT.value not in ignore:
        kg.add_deployments(deployments)

    logger.info("----- Graph built")

    # ===== Output ================================================================

    logger.info("Writing graph to file...")

    with open(args.output, "w") as text_file:
        text_file.write(kg.get_source())

    logger.info("----- File written")
    logger.info("Done.")


if __name__ == "__main__":
    main()
