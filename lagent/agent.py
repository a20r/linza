
import networkx as nx
from geopy.distance import great_circle
import numpy as np
import time


class Agent(object):

    NN_RADIUS = 0.2 # miles
    MIN_TIME_STEP = 0.1 # seconds
    MIN_DISTANCE_STEP = 1

    def __init__(self, **kwargs):
        cs = kwargs.get("cs")
        ds = kwargs.get("ds")
        graph = kwargs.get("graph")
        start_index = kwargs.get("start_index")
        vel_estimate = kwargs.get("vel_estimate")
        sec_eq = kwargs.get("sec_eq")
        self.c_node = start_index
        self.sec_eq = sec_eq
        self.ds = ds
        self.cs = cs
        self.vel_estimate = float(vel_estimate)
        self.graph = graph
        self.distance_mat = self.init_distance_matrix()
        self.time_mat = self.init_time_matrix()
        self.energy_mat = self.init_energy_matrix()
        self.time_func = None
        self.energy_func = None

    def set_time_func(self, time_func):
        self.time_func = time_func

    def set_energy_func(self, energy_func):
        self.energy_func = energy_func

    def set_info_func(self, info_func):
        self.info_func = info_func

    def init_time_matrix(self):
        t_mat = dict()
        for i in self.graph.nodes():
            for j in self.graph.nodes():
                if not t_mat.has_key(i):
                    t_mat[i] = dict()

                if not t_mat.has_key(j):
                    t_mat[j] = dict()

                if not i == j:
                    t_mat[i][j] = self.distance_mat[i][j] /\
                        (self.sec_eq * self.vel_estimate)
                    t_mat[j][i] = self.distance_mat[j][i] /\
                        (self.sec_eq * self.vel_estimate)
                else:
                    t_mat[i][j] = self.MIN_TIME_STEP

        return t_mat

    def init_energy_matrix(self):
        e_mat = dict()
        for i in self.graph.nodes():
            for j in self.graph.nodes():
                if not e_mat.has_key(i):
                    e_mat[i] = dict()

                if not e_mat.has_key(j):
                    e_mat[j] = dict()

                if not i == j:
                    e_mat[i][j] = self.distance_mat[i][j]
                    e_mat[j][i] = self.distance_mat[j][i]
                else:
                    e_mat[i][j] = self.MIN_DISTANCE_STEP

        return e_mat

    def init_distance_matrix(self):
        d_mat = nx.all_pairs_shortest_path_length(self.graph)
        return d_mat

    def learn_time(self, i, j, t):
        self.time_mat[i][j] = 0.9 * self.time_mat[i][j] + 0.1 * t
        return self

    def learn_energy(self, i, j, e):
        self.energy_mat[i][j] = 0.9 * self.energy_mat[i][j] + 0.1 * e
        return self

    def nearest_neighbours(self, lat, lon):
        neighbours = set()
        for name, data in self.graph.nodes(data=True):
            # check order of lat lon here
            this_pos = (lat, lon)
            node_pos = (data["data"].lat, data["data"].lon)
            dist = great_circle(this_pos, node_pos).miles
            if dist <= self.NN_RADIUS:
                neighbours.add(name)

        return neighbours

    def weight(self, i, j, t):
        arival_time = t + self.time_mat[i][j]
        information = self.ds.get_distribution(arival_time, i)
        energy = self.energy_mat[i][j]
        return information / energy

    def step(self):
        occupied = self.cs.get_occupied()
        lat = self.graph.node[self.c_node]["data"].lat
        lon = self.graph.node[self.c_node]["data"].lon
        neighbours = self.nearest_neighbours(lat, lon)
        s_nbrs = neighbours - occupied
        max_weight = 0
        next_node = None
        c_time = time.time()
        for nbr in s_nbrs:
            wght = self.weight(self.c_node, nbr, c_time)
            if wght > max_weight:
                max_weight = weight
                next_node = nbr

        self.cs.update_occupied(c_node, next_node)
        dist = self.distance_mat[c_node][next_node]
        time_needed = self.time_func(dist) / self.sec_eq
        energy_needed = self.energy_func(dist)

        # learns the time and energy matrices
        self.learn_time(c_node, next_node, time_needed)
        self.learn_energy(c_node, next_node, energy_needed)
        self.ds.update_distribution(c_time, c_node, self.info_func(c_time))
        self.c_node = next_node
        time.sleep(time_needed)
        return self.c_node
