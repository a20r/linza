
import lagent

if __name__ == "__main__":
    sim = lagent.Simulation(
        host_ds="52.16.10.199",
        port_ds=8080,
        host_cs="52.16.10.199",
        port_cs=5000,
        num_runs=100,
        start_index=0)
    sim.run()
