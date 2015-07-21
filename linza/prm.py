
import scipy.spatial as spatial
import numpy as np
import networkx as nx
import point
import json


def nn_roadmap(N, k):
    G = nx.Graph()
    data = np.random.rand(N, 2)
    tree = spatial.KDTree(data)
    for i, vec in enumerate(data):
        G.add_node(i, position=point.Point(vec[0], vec[1]))
        ds, inds = tree.query(vec, k=k)
        for d, j in zip(ds, inds):
            G.add_edge(i, j, distance=d)
    return G
