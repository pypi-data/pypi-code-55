#!/usr/bin/python3

"""
Turtle To Markdown

This application loads Turtle files together into a graph.  It looks for a
doc:Document node as the root section and doc:subsections property for
each node for children, recursive descent.  For each node it generates
markdown content.

Because running the deductive closure with both RDFS and OWLRL semantics can
take a while, run the application the '--expanded' option to save or load in
the expanded graph.
"""

import sys
import textwrap
import argparse

from rdflib import Graph, Namespace, BNode, RDF, RDFS, OWL
import owlrl

# globals
g = Graph()
document = ""
namespace_map = {}


def walk_list(node):
    """Given the head of an RDF list, yield each of the nodes."""
    while node != RDF.nil:
        yield g.value(node, RDF.first)
        node = g.value(node, RDF.rest)


def do_section(node, sections):
    """Generate the documentation for a given node."""
    global document

    # section_number = ".".join(str(sect) for sect in sections)
    DOC = namespace_map["doc"]

    # extract the section title from blank nodes
    if isinstance(node, BNode):
        node_name = g.value(node, DOC.title).value
    else:
        node_name = str(node)
        for prefix, namespace in namespace_map.items():
            if node_name.startswith(namespace):
                node_name = prefix + ":" + node_name[len(namespace):]
                break

    # generate the heading
    document += "#" * len(sections) + " " + node_name + "\n"

    # if this is not a blank node, include the full IRI
    if not isinstance(node, BNode):
        document += f"\n> **IRI:** {node}\n"

    # build a description
    desc = None
    if (node, RDF.type, RDFS.Class) in g:
        desc = "A class"
    elif (node, RDF.type, RDF.Property) in g:
        desc = "A property"
    elif (node, RDF.type, OWL.ObjectProperty) in g:
        desc = "An OWL object property"
    elif (node, RDF.type, OWL.DatatypeProperty) in g:
        desc = "An OWL datatype property"
    if desc:
        document += f"\n{desc}\n"

    # add the comments as descriptive text (warning: unordered)
    for comment in g.objects(node, RDFS.comment):
        text = textwrap.dedent(comment.value)
        document += f"\n{text}\n"

    document += "\n"

    # recursively do subsections
    child_subsections = g.value(node, DOC.subsections)
    if child_subsections:
        for i, child in enumerate(walk_list(child_subsections)):
            do_section(child, sections + [i + 1])


# main entry point
def main(ttlfiles, do_rdfs=False, do_owl=False, save_expanded=False):
    # load the files
    for fname in ttlfiles:
        g.parse(fname, format="turtle")

    # expand the graph
    if (do_rdfs and do_owl):
        inferencer = owlrl.DeductiveClosure(owlrl.RDFS_OWLRL_Semantics)
        inferencer.expand(g)
    elif do_rdfs:
        inferencer = owlrl.DeductiveClosure(owlrl.RDFS_Semantics)
        inferencer.expand(g)
    elif do_owl:
        inferencer = owlrl.DeductiveClosure(owlrl.OWLRL_Semantics)
        inferencer.expand(g)
    # make a reverse namespace
    for prefix, uriref in g.namespaces():
        namespace_map[prefix] = Namespace(uriref)

    # use whatever was bound to doc prefix
    if "doc" not in namespace_map:
        sys.stderr.write("error: 'doc' namespace not found\n")
        sys.exit(1)

    DOC = namespace_map["doc"]

    # look for all of the root documents (warning: unordered)
    for root in g.subjects(RDF.type, DOC.Document):
        for i, child in enumerate(walk_list(g.value(root, DOC.subsections))):
            do_section(child, [i + 1])

    # save the exloded graph for debugging
    if save_expanded:
        with open(args.expanded, "wb") as f:
            g.serialize(f, format="turtle")

    return document


if __name__ == '__main__':
    # build a parser for the command line arguments
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # sample additional option to load/store from/to the expanded graph
    parser.add_argument(
        "ttl", type=str, nargs="+", help="turtle files to load",
    )

    parser.add_argument(
        "md", type=str, help="output markdown file",
    )

    # add an option to run RDFS semantics
    parser.add_argument(
        "--rdfs", action="store_true", help="run RDFS semantics",
    )

    # add an option to run OWLRL semantics
    parser.add_argument(
        "--owlrl", action="store_true", help="run OWLRL semantics",
    )

    # add an option to run both RDFS and OWLRL semantics
    parser.add_argument(
        "--both", action="store_true", help="run both RDFS and OWLRL semantics",
    )

    # sample additional option to store the expanded graph
    parser.add_argument(
        "--expanded", type=str, help="load/store the expanded graph",
    )

    # parse the command line arguments
    args = parser.parse_args()
    document = main(args.ttl, do_rdfs=args.rdfs or args.both,
                    do_owl=args.owl or args.both, save_expanded=args.expanded)
    # save the document
    with open(args.md, "w") as f:
        f.write(document)
