
import networkx as nx
import matplotlib.pyplot as plt


class Visualizer:

    OCCUPIED = "b"
    FREE = "0.94"
    K = 0.7

    def __init__(self, G, resources):
        self.G = G
        self.resources = resources
        self.fig = plt.figure()
        self.node_colors = [self.FREE for r in self.G.nodes()]

    def update(self, past_id, next_id, t):
        self.node_color[past_id] = self.FREE
        self.node_color[next_id] = self.OCCUPIED
        node_sizes = [self.K * self.resources[r](t) for r in self.G.nodes()]
        positions = dict()
        for node_id in self.G.nodes():
            positions[node_id] = self.G.node[node_id]['position'].to_list_2d()
        plt.clf()
        nx.draw_networkx_edges(self.G, positions)
        nx.draw_networkx_nodes(self.G, positions, node_color=self.node_color,
                               linewidths=0, node_size=node_sizes, alpha=0.8)
        plt.draw()
        plt.pause(0.00001)
