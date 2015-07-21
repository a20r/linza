
import linza
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    N = 100
    a = range(3)
    k = 4
    G = linza.nn_roadmap(N, k)
    caps = [100 for _ in xrange(N)]
    horizon = 3
    speed = 0.01
    res = [lambda t: t for _ in xrange(N)]
    vis = linza.Visualizer(G, res)
    sim = linza.Linza(
        G, capacities=caps,
        horizon=horizon,
        speed=speed,
        visualizer=vis,
        agents=a
    )

    sim.run(100)
