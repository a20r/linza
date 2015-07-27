
import networkx as nx
import matplotlib.pyplot as plt


class Visualizer:

    OCCUPIED = "r"
    FREE = "b"
    K = 10

    def __init__(self, G, rates):
        self.G = G
        self.rates = rates
        self.fig = plt.figure()
        self.node_colors = [self.FREE for r in self.G.nodes()]

    def draw(self, past_id, next_id, t):
        self.node_colors[past_id] = self.FREE
        self.node_colors[next_id] = self.OCCUPIED
        node_sizes = list()
        positions = dict()
        for r in self.G.nodes():
            node_sizes.append(self.rates[r](t))
        for node_id in self.G.nodes():
            positions[node_id] = self.G.node[node_id]['position'].to_list_2d()
        plt.clf()
        nx.draw_networkx_edges(self.G, positions)
        nx.draw_networkx_nodes(self.G, positions, node_color=self.node_colors,
                               linewidths=0, node_size=node_sizes, alpha=0.8)
        plt.draw()
        plt.pause(0.00001)
