
import lagent

if __name__ == "__main__":
    sim = lagent.Simulation(
        num_runs=2000,
        num_agents=10)
    sim.run()
