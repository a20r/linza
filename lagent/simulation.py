
import simdata
import agent
import osm2nx
import concurrency
import interp
import heapq
import visualisation
import networkx as nx


class Simulation(object):

    def __init__(self, **kwargs):
        self.num_agents = kwargs.get("num_agents")
        self.num_runs = kwargs.get("num_runs")
        self.velocity = 10.0 / 1000  # km / s
        self.noise_std = 0.1
        self.i_funcs = dict()
        self.e_func = simdata.EnergyFunc(self.noise_std)
        self.t_func = simdata.TimeFunc(self.velocity, self.noise_std)
        self.ds = interp.make()
        self.cs = concurrency.make()
        self.graph = self.init_graph()

        for n_id in self.graph.nodes():
            self.i_funcs[n_id] = simdata.InformationFunc(100)

        self.vis = visualisation.Visualiser(self.graph, self.i_funcs)
        self.distance_mat = nx.all_pairs_dijkstra_path_length(self.graph)
        self.agents, self.s_agents = self.init_agents()

    def init_agents(self):
        s_agents = list()
        agents = list()
        for _ in xrange(self.num_agents):
            ag = agent.Agent(
                ds=self.ds,
                cs=self.cs,
                graph=self.graph,
                start_index=self.graph.nodes()[0],
                vel_estimate=self.velocity,
                distance_mat=self.distance_mat)

            ag.set_time_func(self.t_func)
            ag.set_energy_func(self.e_func)
            ag.set_info_funcs(self.i_funcs)
            agents.append(ag)

        for _ in xrange(self.num_agents):
            ag = agent.StupidAgent(
                ds=self.ds,
                cs=self.cs,
                graph=self.graph,
                start_index=self.graph.nodes()[0],
                vel_estimate=self.velocity,
                distance_mat=self.distance_mat)

            ag.set_time_func(self.t_func)
            ag.set_energy_func(self.e_func)
            ag.set_info_funcs(self.i_funcs)
            s_agents.append(ag)
        return agents, s_agents

    def init_graph(self):
        l, b, r, t = self.ds.get_bounding_box()
        return osm2nx.get_osm_graph(l, b, r, t)

    def run(self):
        heap = list()
        for ag in self.agents:
            heapq.heappush(heap, (0, ag))
        last_node = dict()
        info_table = dict()
        energy_table = dict()
        for i in xrange(self.num_runs):
            t, ag = heapq.heappop(heap)
            info, energy, p_node, c_node, t_needed = ag.step(t)
            heapq.heappush(heap, (t + t_needed, ag))
            # self.vis.update(last_node.get(ag, None), p_node, t)
            last_node[ag] = p_node

            if p_node in info_table and t > 0:
                info_table[p_node] += info
                energy_table[p_node] += energy
            else:
                info_table[p_node] = info
                energy_table[p_node] = energy
        return info_table, energy_table

    def run_stupid(self):
        heap = list()
        for ag in self.s_agents:
            heapq.heappush(heap, (0, ag))
        last_node = dict()
        info_table = dict()
        energy_table = dict()
        for i in xrange(self.num_runs):
            t, ag = heapq.heappop(heap)
            info, energy, p_node, c_node, t_needed = ag.step(t)
            heapq.heappush(heap, (t + t_needed, ag))
            # self.vis.update(last_node.get(ag, None), p_node, t)
            last_node[ag] = p_node

            if p_node in info_table and t > 0:
                info_table[p_node] += info
                energy_table[p_node] += energy
            else:
                info_table[p_node] = info
                energy_table[p_node] = energy
        return info_table, energy_table
