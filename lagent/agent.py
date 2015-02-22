
import random
from geopy.distance import great_circle


class Agent(object):

    NN_RADIUS = 1  # miles
    MIN_TIME_STEP = 0.1  # seconds
    MIN_DISTANCE_STEP = 0.01  # km

    def __init__(self, **kwargs):
        self.cs = kwargs.get("cs")
        self.ds = kwargs.get("ds")
        self.graph = kwargs.get("graph")
        self.c_node = kwargs.get("start_index")
        self.vel_estimate = float(kwargs.get("vel_estimate"))
        self.distance_mat = kwargs.get("distance_mat")
        self.time_mat = dict()
        self.energy_mat = dict()
        self.time_func = None
        self.energy_func = None

    def set_time_func(self, time_func):
        self.time_func = time_func

    def set_energy_func(self, energy_func):
        self.energy_func = energy_func

    def set_info_funcs(self, info_funcs):
        self.info_funcs = info_funcs

    def get_distance(self, i, j):
        if i == j:
            return self.MIN_DISTANCE_STEP
        else:
            return self.distance_mat[i][j]

    def get_time(self, i, j):
        if not i in self.time_mat or not j in self.time_mat[i]:
            return self.get_distance(i, j) / self.vel_estimate
        else:
            return self.time_mat[i][j]

    def get_energy(self, i, j):
        if not i in self.energy_mat or not j in self.energy_mat[i]:
            return self.get_distance(i, j)
        else:
            return self.energy_mat[i][j]

    def learn_time(self, i, j, t):
        if i == j:
            return self

        if not i in self.time_mat:
            self.time_mat[i] = dict()

        if not j in self.time_mat:
            self.time_mat[j] = dict()

        if j in self.time_mat[i]:
            self.time_mat[i][j] = 0.7 * self.time_mat[i][j] + 0.3 * t
        else:
            self.time_mat[i][j] = t

        if i in self.time_mat[j]:
            self.time_mat[j][i] = 0.7 * self.time_mat[j][i] + 0.3 * t
        else:
            self.time_mat[j][i] = t

        return self

    def learn_energy(self, i, j, t):
        if i == j:
            return self

        if not i in self.energy_mat:
            self.energy_mat[i] = dict()

        if not j in self.energy_mat:
            self.energy_mat[j] = dict()

        if j in self.energy_mat[i]:
            self.energy_mat[i][j] = 0.7 * self.energy_mat[i][j] + 0.3 * t
        else:
            self.energy_mat[i][j] = t

        if i in self.energy_mat[j]:
            self.energy_mat[j][i] = 0.7 * self.energy_mat[j][i] + 0.3 * t
        else:
            self.energy_mat[j][i] = t

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
        arival_time = t + self.get_time(i, j)
        information = self.ds.get_distribution(arival_time, j)
        energy = self.get_energy(i, j)
        return information / energy

    def step(self, c_time):
        occupied = self.cs.get_occupied()
        lat = self.graph.node[self.c_node]["data"].lat
        lon = self.graph.node[self.c_node]["data"].lon
        neighbours = self.nearest_neighbours(lat, lon)
        s_nbrs = neighbours - occupied
        max_weight = 0
        next_node = None
        for nbr in s_nbrs:
            wght = self.weight(self.c_node, nbr, c_time)
            if wght > max_weight:
                max_weight = wght
                next_node = nbr

        self_weight = self.weight(self.c_node, self.c_node,
                                  c_time + self.MIN_TIME_STEP)

        if max_weight < self_weight and not self.c_node in occupied:
            next_node = self.c_node

        self.cs.update_occupied(self.c_node, next_node)
        dist = self.get_distance(self.c_node, next_node)
        time_needed = self.time_func(dist)
        energy_needed = self.energy_func(dist)

        # learns the time and energy matrices
        info = self.info_funcs[self.c_node](c_time)
        self.learn_time(self.c_node, next_node, time_needed)
        self.learn_energy(self.c_node, next_node, energy_needed)
        self.ds.update_distribution(c_time, self.c_node, info)
        old_c_node = self.c_node
        self.c_node = next_node
        return info, energy_needed, old_c_node, self.c_node, time_needed


class StupidAgent(object):

    MIN_TIME_STEP = 0.1  # seconds
    MIN_DISTANCE_STEP = 0.01  # km

    def __init__(self, **kwargs):
        self.graph = kwargs.get("graph")
        self.c_node = kwargs.get("start_index")
        self.vel_estimate = float(kwargs.get("vel_estimate"))
        self.distance_mat = kwargs.get("distance_mat")
        self.time_func = None
        self.energy_func = None
        self.time_mat = dict()
        self.energy_mat = dict()

    def set_time_func(self, time_func):
        self.time_func = time_func

    def set_energy_func(self, energy_func):
        self.energy_func = energy_func

    def set_info_funcs(self, info_funcs):
        self.info_funcs = info_funcs

    def get_distance(self, i, j):
        if i == j:
            return self.MIN_DISTANCE_STEP
        else:
            return self.distance_mat[i][j]

    def get_time(self, i, j):
        if not i in self.time_mat or not j in self.time_mat[i]:
            return self.get_distance(i, j) / self.vel_estimate
        else:
            return self.time_mat[i][j]

    def get_energy(self, i, j):
        if not i in self.energy_mat or not j in self.energy_mat[i]:
            return self.get_distance(i, j)
        else:
            return self.energy_mat[i][j]

    def step(self, c_time):
        next_node = random.choice(self.graph.nodes())
        dist = self.get_distance(self.c_node, next_node)
        time_needed = self.time_func(dist)
        energy_needed = self.energy_func(dist)

        # learns the time and energy matrices
        info = self.info_funcs[self.c_node](c_time)
        old_c_node = self.c_node
        self.c_node = next_node
        return info, energy_needed, old_c_node, self.c_node, time_needed
