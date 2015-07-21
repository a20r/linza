
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

    def resource(self, i, j, t):
        ret_sum = 0.0
        for k in xrange(1, self.capacities[j] + 1):
            l_k = math.pow(self.means[j], k)
            t_k = math.pow(t - self.last_times[j] + self.times[i][j], k)
            e_pow = self.means[j] * (t - self.last_times[j] + self.times[i][j])
            e_l = math.exp(-e_pow)
            fac = math.factorial(k - 1)
            ret_sum += l_k * t_k * e_l / fac
        return ret_sum

    def naive_weight(self, i, j, t):
        return self.resource(i, j, t) / self.costs[i][j]

    def eligible_neighbours(self, i, theta):
        N = list(set(self.graph.neighbors(i)) - set(theta))
        N_star = list()
        t_sum = 0.0
        for k in xrange(len(theta) - 1):
            t_sum += self.times[theta[k]][theta[k + 1]]
        for n in N:
            if t_sum + self.times[i][n] <= self.horizon:
                N_star.append(n)
        return N_star

    def weight(self, i, j, t, theta=list()):
        ret_w = self.naive_weight(i, j, t)
        for k in self.eligible_neighbours(i, theta):
            ret_w += self.weight(j, k, t + self.times[i][j], theta + [i])
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
