from pptree import *

if __name__ == '__main__':
    shame = Node("shame")

    conscience = Node("conscience", shame)
    selfdisgust = Node("selfdisgust", shame)
    embarrassment = Node("embarrassment", shame)

    selfconsciousness = Node("selfconsciousness", embarrassment)
    shamefacedness = Node("shamefacedness", embarrassment)
    chagrin = Node("chagrin", embarrassment)
    discomfiture = Node("discomfiture", embarrassment)
    abashment = Node("abashment", embarrassment)
    confusion = Node("confusion", embarrassment)

    print_tree(shame)