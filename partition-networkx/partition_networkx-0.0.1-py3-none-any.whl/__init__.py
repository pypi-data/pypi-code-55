__version__ = "0.0.1"
import networkx
import community

from .partition_networkx import (
    community_ecg,
    gam,
)

networkx.classes.graph.Graph.gam = gam
community.ecg = community_ecg

