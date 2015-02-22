
import lagent

if __name__ == "__main__":
    sim = lagent.Simulation(
        num_runs=10000,
        num_agents=30)
    sim.run()
