
import scipy.spatial as spatial
import numpy as np
import networkx as nx
import point
import math


def grid_graph(N, k):
    data = np.zeros((N, 2))
    ps = np.linspace(0, 1, int(math.sqrt(N)))
    counter = 0
    for x in ps:
        for y in ps:
            data[counter][0] = x
            data[counter][1] = y
            counter += 1
    return nn_roadmap_given_points(N, k, data)


def nn_roadmap(N, k):
    data = np.random.rand(N, 2)
    return nn_roadmap_given_points(N, k, data)


def nn_roadmap_given_points(N, k, data):
    G = nx.Graph()
    tree = spatial.KDTree(data)
    for i, vec in enumerate(data):
        G.add_node(i, position=point.Point(vec[0], vec[1]))
        ds, inds = tree.query(vec, k=k)
        for d, j in zip(ds, inds):
            G.add_edge(i, j, distance=d)
    return G
