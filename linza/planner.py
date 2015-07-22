
import collections
import math


class Planner(object):

    def __init__(self, graph, **kwargs):
        self.graph = graph
        self.times = kwargs["times"]
        self.costs = kwargs["costs"]
        self.means = kwargs["means"]
        self.capacities = kwargs["capacities"]
        self.horizon = kwargs["horizon"]
        self.last_times = collections.defaultdict(int)

    def update_last_time(self, i, t):
        self.last_times[i] = t
        return self

    def get_last_time(self, i):
        return self.last_times[i]

    def resource(self, i, j, t):
        ret_sum = 0.0
        for k in xrange(1, self.capacities[j] + 1):
            T = t - self.last_times[j] + self.times[i][j]
            param = self.means[j] * T
            l_k = math.pow(param, k)
            e_l = math.exp(-param)
            fac = math.factorial(k - 1)
            ret_sum += l_k * e_l / fac
        return ret_sum

    def naive_weight(self, i, j, t):
        return self.resource(i, j, t) / self.costs[i][j]

    def eligible_neighbours(self, i, T, theta):
        N = list(set(self.graph.neighbors(i)) - set(theta))
        N_star = list()
        for n in N:
            if T + self.times[i][n] <= self.horizon:
                N_star.append(n)
        return N_star

    def weight(self, i, j, t):
        to_search = list()
        for k in self.graph.neighbors(j):
            to_search.append((j, k, t + self.times[i][j], self.times[i][j]))
        already_searched = set([i])
        ret_w = self.naive_weight(i, j, t)
        while len(to_search) > 0:
            i_s, j_s, t_s, T_s = to_search.pop()
            ret_w += self.naive_weight(i_s, j_s, t_s)
            ns = self.eligible_neighbours(j_s, T_s + self.times[i_s][j_s],
                                          already_searched)
            already_searched.update(ns)
            for k in ns:
                to_search.append((j_s, k, t_s + self.times[i_s][j_s],
                                  T_s + self.times[i_s][j_s]))
        return ret_w

    def move(self, i, t):
        best_node = None
        max_weight = 0
        for j in self.graph.neighbors(i):
            w = self.weight(i, j, t)
            if w > max_weight:
                best_node = j
                max_weight = w
        return best_node, t + self.times[i][best_node]
