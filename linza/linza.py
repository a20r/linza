
import numpy as np
import random
import heapq
import planner
from progressbar import ProgressBar


class Linza(object):

    def __init__(self, graph, **kwargs):
        self.graph = graph
        self.horizon = kwargs["horizon"]
        self.speed = kwargs["speed"]
        self.rate_funcs = kwargs["rate_funcs"]
        self.entropies = kwargs["entropies"]
        self.eps_time = kwargs["eps_time"]
        self.visualizer = kwargs.get("visualizer", None)
        self.agent_heap = self.init_agent_heap(kwargs["agents"])
        self.times = self.init_times()
        self.costs = self.init_costs()
        self.pl = planner.Planner(self.graph, times=self.times,
                                  rate_funcs=self.rate_funcs,
                                  entropies=self.entropies, costs=self.costs,
                                  horizon=self.horizon, eps_time=self.eps_time)

    def init_agent_heap(self, agents):
        agent_heap = list()
        for a, i in enumerate(agents):
            agent_heap.append((0, i, a))
        return agent_heap

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
                costs[i][j] = pow(t + 1, 1)
        return costs

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
        progress = ProgressBar()
        for k in progress(xrange(num_runs)):
            t, i, a = heapq.heappop(self.agent_heap)
            i_new, t_new = self.pl.move(i, t)
            heapq.heappush(self.agent_heap, (t_new, i_new, a))
            if self.visualizer:
                self.visualizer.draw(i, i_new, t_new)
