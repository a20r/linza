import networkx as nx
from osm import *
import geopy as geo
from geopy.distance import distance
import random
from array import array
from matplotlib import animation
import numpy as np
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Visualiser:
    def __init__(self, G):
        self.G = G

    def run():

        pos = {}

        for node_id in self.G.nodes():
            lat = self.G.node[node_id]['data'].lat
            lon = self.G.node[node_id]['data'].lon
            pos[node_id] = array('f')
            pos[node_id].append(lat)
            pos[node_id].append(lon)


            fig = plt.figure()
            fig.set_facecolor('white')

            def update(n):
                plt.clf()
                plt.axis('off')
                node_color = [random.choice(["b","0.75"]) for r in xrange(len(self.G.nodes()))]
                edge_color = [random.choice(["0.75","g"]) for r in xrange(len(self.G.edges()))]
                node_size = [random.randint(0,50) for r in xrange(len(self.G.nodes()))]
                nx.draw_networkx_edges(self.G, pos,edge_color=edge_color)
                nx.draw_networkx_nodes(self.G, pos,node_color=node_color,linewidths=0,node_size=node_size,alpha=0.8)

            anim = FuncAnimation(fig, update, 100, repeat=True)
            plt.show()
