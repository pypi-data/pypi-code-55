# -*- coding: utf-8 -*-

from os import path
import logging
import glob
import re
import yaml
from .util import *

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Snapshot:
    KUBECTL_PATH_PREFIX = 'kubectlCommands'
    NODES_PATH_PREFIX = 'nodes'

    def __init__(self, fspath):
        if not isexist(fspath, self.KUBECTL_PATH_PREFIX):
            logging.error('Snapshot doesn\'t exist: %s' % fspath)
            raise FileNotFoundError

        if not isexist(fspath, self.KUBECTL_PATH_PREFIX):
            logging.error(
                'The path doesn\'t look like a snapshot: %s' % fspath)
            raise ValueError

        self.name = path.basename(fspath)
        self.fspath = fspath
        self.kubectl_cmd_fspath = path.join(self.fspath, self.KUBECTL_PATH_PREFIX)
        self.nodes_fspath = path.join(self.fspath, self.NODES_PATH_PREFIX)

        self.cluster_info = self.get_cluster()
        self.cluster_name = self.cluster_info['metadata']['name']

        self.namespaces = self.get_namespaces()
        self.nodes = self.get_nodes()

    def get_cluster(self):
        cluster_yaml = ls(self.kubectl_cmd_fspath, 'kubectl_get_clusters_-o_yaml*')
        if not cluster_yaml:
            logging.error('no cluster definition file found')
            return None

        clusterdef = yaml.load(open(cluster_yaml[0], 'r'), Loader=Loader)

        return clusterdef['items'][0]


    def get_namespaces(self):
        yamlfiles = ls(self.kubectl_cmd_fspath, 'kubectl_get_all_-o_yaml*')
        widefiles = ls(self.kubectl_cmd_fspath, 'kubectl_get_all_-o_wide*')
        descfiles = ls(self.kubectl_cmd_fspath, 'kubectl_describe_all_*')

        yamlfiles = list(map(lambda f: path.basename(f), yamlfiles))
        widefiles = list(map(lambda f: path.basename(f), widefiles))
        descfiles = list(map(lambda f: path.basename(f), descfiles))

        re_ns_name = re.compile(r'_--namespace_([^_]+)')

        nss = {}
        for yamlfile in yamlfiles:
            m = re_ns_name.findall(yamlfile)
            if not m:
                logging.error('Invalid file name. Skipped: %s' % yamlfile)
                continue

            widefile = list(filter(lambda f: re.findall('_--namespace_%s(?:$|_)' % m[0], f), widefiles))
            descfile = list(filter(lambda f: re.findall('_--namespace_%s(?:$|_)' % m[0], f), descfiles))

            ns = Namespace()
            ns.name = m[0]
            ns.yaml_file = yamlfile
            ns.yaml_content = yaml.load(open(self.realpath(self.KUBECTL_PATH_PREFIX, ns.yaml_file), 'r'), Loader=Loader)

            if widefile:
                ns.wide = widefile[0]

            if descfile:
                ns.desc = descfile[0]

            nss[m[0]] = ns

        return nss

    def get_nodes(self):
        dirs = ls(self.nodes_fspath, '*')

        nodenames = list(map(lambda d: path.basename(d), dirs))

        nodedef_yaml = ls(self.kubectl_cmd_fspath,
                          'kubectl_get_nodes_-o_yaml*')
        if not nodedef_yaml:
            logging.error('no nodes definition file found')

        machinedef_yaml = ls(self.kubectl_cmd_fspath,
                             'kubectl_get_machines_-o_yaml*')
        if not machinedef_yaml:
            logging.error('no machine definition file found')

        nodes = dict.fromkeys(nodenames)
        nodedef = yaml.load(open(nodedef_yaml[0], 'r'), Loader=Loader)
        machinedef = yaml.load(open(machinedef_yaml[0], 'r'), Loader=Loader)

        for n in nodedef['items']:
            node = Node()
            node.name = n['metadata']['name']
            node.machine_name = n['metadata']['annotations']['cluster.k8s.io/machine']

            addrs = n['status']['addresses']

            internal_ip = list(
                filter(lambda a: a['type'] == 'InternalIP', addrs))
            external_ip = list(
                filter(lambda a: a['type'] == 'ExternalIP', addrs))

            if internal_ip:
                node.internal_ip = internal_ip[0]['address']
            if external_ip:
                node.external_ip = external_ip[0]['address']

            nodes[node.machine_name] = node

        return nodes

    def get_pods(self, namespace):
        ns = self.namespaces[namespace]

        if not ns:
            logging.error('No such namespace: %s' % namespace)
            raise ValueError('No such namespace: %s' % namespace)

        podsdef = list(filter(lambda i: i['kind'] == 'Pod', ns.yaml_content['items']))

        pods = {}
        for poddef in podsdef:
            pod = Pod()

            pod.name = poddef['metadata']['name']
            pod.namespace = namespace
            pod.labels = poddef['metadata'].get('labels')
            pod.phase = poddef['status']['phase']
            pod.pod_ip = poddef['status']['podIP']
            pod.yaml_content = poddef

            pod.containers = {}
            for cdef in poddef['spec']['containers']:
                c = Container()

                c.name = cdef['name']
                c.image = cdef['image']
                c.pod_name = pod.name
                c.namespace = pod.namespace

                logfile = ls(self.kubectl_cmd_fspath, 'kubectl_logs_%s_--container_%s_*' % (c.pod_name, c.name))
                if logfile:
                    c.log = path.basename(logfile[0])

                pod.containers[c.name] = c

            pods[pod.name] = pod

        return pods

    def get_others(self, namespace):
        ns = self.namespaces[namespace]

        if not ns:
            logging.error('No such namespace: %s' % namespace)
            raise ValueError('No such namespace: %s' % namespace)

        othersdef = list(filter(lambda i: i['kind'] != 'Pod', ns.yaml_content['items']))

        others = []
        for itemdef in othersdef:
            item = Others()

            item.name = itemdef['metadata']['name']
            item.namespace = namespace
            item.kind = itemdef['kind'].lower()
            item.yaml_content = itemdef

            others.append(item)
        
        return others

    def realpath(self, *relpathelems):
        """Convert in bundle path to real accessable path"""
        return path.join(self.fspath, *relpathelems)

class Namespace:
    name = None
    wide = None
    desc = None
    yaml_content = None
    yaml_file = None

class Node:
    name = None
    machine_name = None
    internal_ip = None
    external_ip = None

class Pod:
    name = None
    namespace = None
    labels = None
    containers = {}
    phase = None
    pod_ip = None
    yaml_content = None

class Container:
    name = None
    pod_name = None
    namespace = None
    image = None
    log = None

class Others:
    kind = None
    name = None
    namespace = None
    yaml_content = None
