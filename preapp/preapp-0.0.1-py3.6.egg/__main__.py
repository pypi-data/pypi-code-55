from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from preapp.nodes import RootNode
import argparse
from preapp import Node


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="tool for setting up software projects"
    )
    parser.add_argument("-p", "--preset", action='store', type=str)
    args = parser.parse_args()
    root_node: RootNode = RootNode(args.preset)
    Node.register(root_node)
    root_node.process()
    
