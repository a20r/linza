
import simdata
import agent
import rest


class Simulation(object):

    def __init__(self, host_cs, port_cs, host_ds, port_ds, num_runs):
        self.num_runs = num_runs
        self.velocity = 10
        self.noise_std = 0.1
        self.sec_eq = 1
        self.i_func = simdata.InformationFunc(10)
        self.e_func = simdata.EnergyFunc(self.noise_std)
        self.t_func = simdata.TimeFunc(self.velocity, self.noise_std)
        self.ds = rest.make_ds(host_ds, port_ds)
        self.cs = rest.make_cs(host_cs, port_cs)
        self.ag = agent.Agent(self.ds, self.cs, self.velocity, self.sec_eq)
        self.ag.set_time_func(self.t_func)
        self.ag.set_energy_func(self.e_func)

    def run(self):
        for i in xrange(self.num_runs):
            self.ag.step()
