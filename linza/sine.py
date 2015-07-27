
import math


class PositiveSine(object):

    def __init__(self, a, b, c):
        self.call = lambda t: a * math.sin(b * t) + a + c
        self.it = lambda t: -a / b * math.cos(b * t) + (a + c) * t

    def __call__(self, t):
        return self.call(t)

    def integral(self, t0, t1):
        assert t1 >= t0
        return self.it(t1) - self.it(t0)
