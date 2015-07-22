
import linza

if __name__ == "__main__":
    N = 100
    a = range(10)
    k = 5
    G = linza.grid_graph(N, k)
    caps = [10 for _ in xrange(N)]
    horizon = 2
    speed = 0.01
    res = [lambda t: t if t < caps[i] else caps[i] for i in xrange(N)]
    vis = linza.Visualizer(G, res)
    # vis = None
    sim = linza.Linza(
        G, capacities=caps,
        horizon=horizon,
        speed=speed,
        visualizer=vis,
        agents=a
    )

    print sim.run(1000)
