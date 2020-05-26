# -*- coding: utf-8 -*-

from os import path
import os
import logging
import yaml
from .util import *
from .snapshot import Snapshot


class Index:
    def __init__(self, snapshot, destpath):
        dest_cluster = path.join(destpath, snapshot.cluster_name)
        src_kubectl = snapshot.realpath(snapshot.KUBECTL_PATH_PREFIX)
        src_nodes = snapshot.realpath(snapshot.NODES_PATH_PREFIX)

        # create namespaces
        for ns in snapshot.namespaces.values():
            os.makedirs(path.join(dest_cluster, 'namespaces',
                                  ns.name), exist_ok=True)
            symlink(path.join(src_kubectl, ns.yaml_file), path.join(
                dest_cluster, 'namespaces', ns.name), 'all.yaml')

            if ns.wide:
                symlink(path.join(src_kubectl, ns.wide), path.join(
                    dest_cluster, 'namespaces', ns.name), 'all-list.txt')

            if ns.desc:
                symlink(path.join(src_kubectl, ns.desc), path.join(
                    dest_cluster, 'namespaces', ns.name), 'all-desc.txt')

            # create each pod
            for pod in snapshot.get_pods(ns.name).values():
                dest_pod_dir = path.join(
                    dest_cluster, 'namespaces', pod.namespace, 'pod.%s' % pod.name)
                os.makedirs(dest_pod_dir, exist_ok=True)

                yaml.dump(pod.yaml_content, open(
                    path.join(dest_pod_dir, 'definition.yaml'), 'w+'))

                # create each container
                for c in pod.containers.values():
                    if c.log:
                        symlink(path.join(src_kubectl, c.log),
                                dest_pod_dir, '%s.log' % c.name)

            # create each deployment, statefulset, daemonset
            for item in snapshot.get_others(ns.name):
                dest_yaml = path.join(
                    dest_cluster, 'namespaces', item.namespace, '%s.%s.yaml' % (item.kind, item.name))

                yaml.dump(item.yaml_content, open(dest_yaml, 'w+'))

        os.makedirs(path.join(dest_cluster, 'nodes'), exist_ok=True)

        for nodename, node in snapshot.nodes.items():
            destname = nodename
            if node:
                destname = '%s(%s:%s)' % (
                    nodename, node.name, node.internal_ip)
            symlink(path.join(src_nodes, nodename),
                    path.join(dest_cluster, 'nodes'), destname)

        yaml.dump(snapshot.cluster_info, open(
            path.join(dest_cluster, 'cluster.yaml'), 'w+'))


def symlink(src, destdir, filename):
    os.symlink(path.relpath(src, destdir), path.join(destdir, filename))
