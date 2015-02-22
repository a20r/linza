
class DistributionModel(object):

    def __init__(self, num_bins=60):
        self.num_bins = num_bins
        self.func = dict()
        self.sec_per_day = 60
        self.alpha = 0.9
        self.beta = 1 - self.alpha
        self.large_number = 1000.0

    def get_bounding_box(self):
        return -2.8037, 56.3381, -2.7882, 56.3435

    def get_bin(self, time):
        bn = self.num_bins * (int(time) % self.sec_per_day) / self.sec_per_day
        return bn

    def update_distribution(self, time, node_id, value):
        value = float(value)
        if not node_id in self.func:
            self.func[node_id] = [None for _ in xrange(self.num_bins)]
        bn = self.get_bin(time)
        f_val = self.func[node_id][bn]
        if f_val:
            self.func[node_id][bn] = self.alpha * f_val + self.beta * value
        else:
            self.func[node_id][bn] = f_val
        return self

    def get_distribution(self, time, node_id):
        bn = self.get_bin(time)
        try:
            f_val = self.func[node_id][bn]
        except KeyError:
            return self.large_number

        if not f_val:
            return self.large_number
        return f_val


def make(**kwargs):
    return DistributionModel(**kwargs)
