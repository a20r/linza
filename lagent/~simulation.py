
import simdata
import agent
import osm2nx
import rest


class Simulation(object):

    def __init__(self, **kwargs):
        host_cs = kwargs.get("host_cs")
        port_cs = kwargs.get("port_cs")
        host_ds = kwargs.get("host_ds")
        port_ds = kwargs.get("port_ds")
        num_runs = kwargs.get("num_runs")
        start_index = kwargs.get("start_index")
        self.num_runs = num_runs
        self.velocity = 10.0 / 1000 # km / s
        self.noise_std = 0.1
        self.sec_eq = 60 * 60
        self.i_funcs = dict()
        self.e_func = simdata.EnergyFunc(self.noise_std)
        self.t_func = simdata.TimeFunc(self.velocity, self.noise_std)
        self.ds = rest.make_ds(host_ds, port_ds)
        self.cs = rest.make_cs(host_cs, port_cs)
        self.graph = self.init_graph()
        for n_id in self.graph.nodes():
            self.i_funcs[n_id] = simdata.InformationFunc(10)

        self.ag = agent.Agent(
            ds=self.ds,
            cs=self.cs,
            graph=self.graph,
            start_index=self.graph.nodes()[start_index],
            vel_estimate=self.velocity,
            sec_eq=self.sec_eq)
        self.ag.set_time_func(self.t_func)
        self.ag.set_energy_func(self.e_func)
        self.ag.set_info_funcs(self.i_funcs)

    def init_graph(self):
        l, b, r, t = self.ds.get_bounding_box()
        return osm2nx.get_osm_graph(l, b, r, t)

    def run(self):
        for i in xrange(self.num_runs):
            print self.ag.step()
