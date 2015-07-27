

class Planner(object):

    def __init__(self, graph, **kwargs):
        self.graph = graph
        self.times = kwargs["times"]
        self.costs = kwargs["costs"]
        self.rate_funcs = kwargs["rate_funcs"]
        self.entropies = kwargs["entropies"]
        self.horizon = kwargs["horizon"]
        self.eps_time = kwargs["eps_time"]

    def events(self, i, t, t_diff):
        return self.rate_funcs[i].integral(t, t + t_diff)

    def naive_weight(self, i, j, t):
        evs = self.events(j, t + self.times[i][j], self.eps_time)
        return self.entropies[j] * evs

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
        return best_node, t + self.times[i][best_node] + self.eps_time
