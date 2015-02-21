
import agent

if __name__ == "__main__":
    host_ds = "localhost"
    port_ds = 8000
    host_cs = "localhost"
    port_cs = 5000
    sim = agent.Simulation(host_ds, port_ds, host_cs, port_cs)
    sim.run()
