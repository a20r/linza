
import numpy as np
import heapq
import planner


class Linza(object):

    def __init__(self, graph, **kwargs):
        self.graph = graph
        self.capacities = kwargs["capacities"]
        self.horizon = kwargs["horizon"]
        self.speed = kwargs["speed"]
        self.visualizer = kwargs.get("visualizer", None)
        self.agent_heap = [(0, i, a) for a, i in enumerate(kwargs["agents"])]
        self.times = self.init_times()
        self.costs = self.init_costs()
        self.means = self.init_means()
        self.pl = planner.Planner(self.graph, capacities=self.capacities,
                                  horizon=self.horizon, times=self.times,
                                  costs=self.costs, means=self.means)

    def init_times(self):
        n_nodes = len(self.graph.nodes())
        times = np.zeros((n_nodes, n_nodes))
        for i in self.graph.nodes():
            for j in self.graph.neighbors(i):
                times[i][j] = self.graph[i][j]["distance"] / self.speed
        return times

    def init_costs(self):
        n_nodes = len(self.graph.nodes())
        costs = np.zeros((n_nodes, n_nodes))
        for i in self.graph.nodes():
            for j in self.graph.neighbors(i):
                t = self.graph[i][j]["distance"] / self.speed
                costs[i][j] = pow(t + 1, 2)
        return costs

    def init_means(self):
        n_nodes = len(self.graph.nodes())
        means = np.zeros((n_nodes, 1))
        for i, cap in enumerate(self.capacities):
            means[i] = 1
        return means

    def update_time(self, i, j, t):
        self.times[i][j] = t
        return self

    def update_cost(self, i, j, c):
        self.costs[i][j] = c
        return self

    def update_mean(self, i, l):
        self.means[i] = l
        return self

    def run(self, num_runs):
        heapq.heapify(self.agent_heap)
        for _, i, _ in self.agent_heap:
            self.pl.update_last_time(i, 0)
        for k in xrange(num_runs):
            t, i, a = heapq.heappop(self.agent_heap)
            i_new, t_new = self.pl.move(i, t)
            heapq.heappush(self.agent_heap, (t_new, i_new, a))
            if self.visualizer:
                self.visualizer.draw(
                    i, i_new, t_new,
                    self.pl.last_times)
            self.pl.update_last_time(i_new, t_new)
