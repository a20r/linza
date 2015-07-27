
import linza
import random


def init_rate_funcs(N):
    funcs = list()
    for _ in xrange(N):
        a = random.uniform(50, 200)
        b = random.uniform(0.1, 3)
        c = random.uniform(0.1, 0.5)
        funcs.append(linza.PositiveSine(a, b, c))
    return funcs


if __name__ == "__main__":
    N = 100
    a = range(10)
    k = 5
    G = linza.grid_graph(N, k)
    eps_time = 0.1
    horizon = 2
    speed = 0.01
    rate_funcs = init_rate_funcs(N)
    vis = linza.Visualizer(G, rate_funcs)
    vis = None
    es = [random.uniform(1, 5) for _ in xrange(N)]
    sim = linza.Linza(
        G,
        horizon=horizon,
        speed=speed,
        visualizer=vis,
        rate_funcs=rate_funcs,
        entropies=es,
        eps_time=eps_time,
        agents=a
    )

    print sim.run(1000)
