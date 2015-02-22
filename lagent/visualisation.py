from array import array
import networkx as nx
import matplotlib.pyplot as plt


class Visualiser:

    OCCUPIED = "b"
    FREE = "0.75"

    def __init__(self, G, i_funcs):
        self.G = G
        self.i_funcs = i_funcs
        self.fig = plt.figure()

        self.node_keys = dict()
        for i, r in enumerate(self.G.nodes()):
            self.node_keys[r] = i

        self.node_color = [self.FREE for r in self.G.nodes()]
        self.node_color[0] = self.OCCUPIED

    def update(self, past_id, next_id, t):
        if past_id:
            self.node_color[self.node_keys[past_id]] = self.FREE
        self.node_color[self.node_keys[next_id]] = self.OCCUPIED
        node_size = [0.7 * self.i_funcs[r](t) for r in self.G.nodes()]

        pos = {}

        for node_id in self.G.nodes():
            lat = self.G.node[node_id]['data'].lat
            lon = self.G.node[node_id]['data'].lon
            pos[node_id] = array('f')
            pos[node_id].append(lat)
            pos[node_id].append(lon)

        plt.clf()
        nx.draw_networkx_edges(self.G, pos)
        nx.draw_networkx_nodes(self.G, pos, node_color=self.node_color,
                               linewidths=0, node_size=node_size, alpha=0.8)
        plt.draw()
        plt.pause(0.00001)
