
import lagent
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    sim = lagent.Simulation(
        num_runs=100000,
        num_agents=30)

    xs, ys, it = sim.run()
    s_xs, s_ys, s_it = sim.run_stupid()
    plt.plot(xs, ys, 'g', label="Smart")
    plt.plot(s_xs, s_ys, 'r', label="Stupid")
    plt.xlabel("Time")
    plt.ylabel("Information")
    plt.title("Information gathered over time")
    plt.xlim(0, xs[-1])
    plt.legend()
    plt.show()

    ind = np.arange(sim.graph.number_of_nodes())
    width = 1

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, it.values(), width, color='g')
    rects2 = ax.bar(ind + width, s_it.values(), width, color='r')
    # add some text for labels, title and axes ticks
    ax.set_xticks(ind + width)
    plt.ylabel("Information")
    plt.title("Information gathered per node")
    plt.show()
