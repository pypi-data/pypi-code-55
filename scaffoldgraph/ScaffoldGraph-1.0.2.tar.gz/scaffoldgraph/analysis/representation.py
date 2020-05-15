"""
scaffoldgraph.analysis.cse
"""

# TODO: Average pairwise tanimoto calculation (APT)
# TODO: Over represented scaffold analysis using APT
# TODO: Fingerprint selector function (by string)
# TODO: maybe use APS and have custom similarity functions (extension of HierS)

# create all fingerprints for compounds in the graph (multiprocess)
# for each scaffold we can get all molecules containing the query scaffold
# once we have the pool of molecules we can get the APT for the pool
# maybe possible to cache the similarities between two pairs as they will likely be encountered more than once
# OR create a pairwise similarity matrix of all by all similarities and use it as a lookup table
# fit method calculates APT
# user can extract over-represented scaffolds as a list (threshold)
# need to add molecular weight property to each scaffold node

# First HierS first builds a list of all scaffolds that exceed a user-defined APT criterion (e.g., 0.80)
# Next, HierS sorts the list by ascending molecular weight and then proceeds down the list and inspects each
# scaffold to see if it is derived from a scaffold that precedes it in the list
# Any scaffold in the list of over-represented scaffolds that is found to be derived from a higher ranking
# (i.e., lower molecular weight) scaffold is removed because all of the compounds that have membership
# in such scaffolds are already accounted for by the higher ranking scaffold.

# The thresholds Loose, Medium, and Strict correspond to 0.75, 0.80, and 0.85
# Calculate MW + broadcast to graph


def calculate_scaffold_apt():
    # calculate APT/APS
    pass


def broadcast_scaffold_property(graph, values, name=None):
    # broadcast a property to each scaffold in a scaffold graph
    # use to broadcast APT/APS
    pass
