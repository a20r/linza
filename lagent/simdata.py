
import numpy as np
import math
import random


class EnergyFunc(object):

    def __init__(self, noise_std):
        self.noise_std = noise_std

    def __call__(self, dist):
        return self.get(dist) + random.gauss(0, self.noise_std)

    def get(self, dist):
        return 3.14 * np.pow(dist, 2) + 0.1


class TimeFunc(object):

    def __init__(self, velocity, noise_std):
        self.velocity = float(velocity)
        self.noise_std = noise_std

    def __call__(self, dist):
        return self.get(dist) + random.gauss(0, self.noise_std)

    def get(self, dist):
        return dist / self.velocity


class InformationFunc(object):

    def __init__(self, num_sps):
        self.a = [random.gauss(0, 3) for k in xrange(num_sps)]
        self.b = [random.gauss(0, 0.2) for k in xrange(num_sps)]
        self.c = [random.gauss(0, 2) for k in xrange(num_sps)]
        self.d = [random.gauss(0, 1) for k in xrange(num_sps)]
        self.num_sps = num_sps

    def __call__(self, t):
        val = 0
        for i in xrange(self.num_sps):
            val += self.a[i] * math.sin(self.b[i] * t + self.c[i]) + self.d[i]

        if val < 0:
            val = 0

        return val